# Likelihood lifecycle phase 5D: PyAutoFit `number_of_cores="auto"`, a post-setup parallel banner, parallel metadata, and factor graphs that forward `modify_before_fit` with a setup-agreement check

Type: feature
Target: PyAutoFit
Repos:
- PyAutoFit
Themes:
- hpc-gpu
- profiling
Difficulty: large
Autonomy: supervised
Priority: high
Status: active
Issued: 2026-11-24
Issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1794
Consequence: judge
Witness: PyAutoFit main accepts `number_of_cores="auto"` on `SettingsSearch` and every search constructor, validating an int ≥ 1 or `"auto"`. The default stays 1 (R6). "auto" is resolved in `PoolFactory`, after `analysis.modify_before_fit`, to the detected cores (`SLURM_CPUS_PER_TASK` → CPU affinity → `cpu_count`), and to 1 for JAX analyses (the existing fork rule) and for EP factor searches. When the analysis supplies `resources_per_eval()` (cpus_per_eval, peak_rss_gb), the count is capped at min(cores / cpus_per_eval, available memory / peak_rss); otherwise there is no cap. One banner line after `modify_before_fit` reports the effective workers, the request, any cap reason and the setup_id; the stale `log_fit_start` JAX/cores claim is gone. The resolved count, cap reason and setup_id are written to `search.summary` and `files/parallel.json`. `FactorGraphModel.modify_before_fit` forwards to each factor's analysis (its own model and sub-paths, rebinding both analysis references), and a `check_setup_agreement` beside `check_backend_agreement` refuses graphs whose factors resolved different setups. Full test suite green; `pyauto-heart smoke --affected-by PyAutoFit` passes.
Review-minutes: 30
Unattended: no
Lane: any
Gate: 5C-3 MERGED (PyAutoGalaxy#753, PyAutoLens#886); 5C setup resolution in `modify_before_fit` is on Galaxy/Lens main. Plan and design calls approved by the human 2026-11-24.
Epic: likelihood-lifecycle
Phase: 5
Parent: draft/research/autolens_profiling/likelihood_lifecycle_epic.md
Filed: 2026-11-24

## Context

- **Report §3.5, PyAutoFit row:** `SettingsSearch(number_of_cores="auto")` → setup threads; the fork rule is unchanged; the banner is printed at fit start; the resolved setup is stored in the search metadata. The node-throughput amendment caps workers at min(cores / cpus_per_eval, memory / peak_rss).
- **Survey 2026-11-24:**
  - `number_of_cores` is unvalidated (settings.py:16; abstract_search.py:98, :168-169).
  - `warn_if_threads_unpinned` compares `<= 1` (runtime.py:103), so "auto" would raise in the constructor.
  - Fork rule: `effective_number_of_cores` (parallel/pool.py:60-90). `PoolFactory` (:137-230) is built in `start_resume_fit` (abstract_search.py:424) after `modify_before_fit`. `log_fit_start` (runtime.py:242-263) runs before it (:307 vs :317).
  - Metadata: `search.json` comes from `to_dict(search)` (paths/directory.py:382-401); `search.summary` from `run_summary_from` → `search._parallel_summary` (capabilities.py:281-287, abstract_search.py:425).
  - Factor graphs: `FactorGraphModel` inherits the no-op `modify_before_fit` (analysis.py:301-309). There are two analysis references, `AnalysisFactor.analysis` (factor/analysis.py:74) and `FactorCallable.analysis` (:21). Preflight runs `check_backend_agreement` (search/preflight.py:326-356; collection.py:111-142).
  - Phase 4 measured η only for imaging/rectangular numba (autolens_inference `scripts/misc/wall/model.py:99`: 1.0, 0.68, 0.62, 0.55, 0.36, 0.28 at 1–32 cores). Cores × η is monotone increasing, so throughput favours all cores.
  - `peak_rss_gb` exists only in autolens_profiling `runtime_estimates.yaml`, which no library reads until 5E. Nerves has total `ram_gb` but no available-memory probe.
- **Design calls (human-approved 2026-11-24):**
  1. No η-based cap in 5D. The one measured curve favours all cores; record η context in the metadata note.
  2. The memory cap applies only when the analysis supplies `resources_per_eval()`. It goes live when 5E ships `runtime_estimates.yaml`. Add an available-memory read: `MemAvailable`, cgroup-aware if simple, falling back to total.
  3. "auto" is accepted and validated everywhere; the thread warning is deferred to resolution.
  4. Factor-graph setup forwarding lands in PyAutoFit; Galaxy/Lens are untouched. The PyAutoLens `SetupException` guard stays for EP, which never calls `modify_before_fit`.

## Out of scope

- The runtime estimator and copying `runtime_estimates.yaml` into PyAutoLens (5E).
- Workspace prose (5F).
- Flipping the default to auto (R6).
- Slimming the Analysis setup to delegate numpy operators to `sparse_operator_for` (at the R6 flip).
