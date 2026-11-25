## likelihood-lifecycle-p5e
- issue: https://github.com/PyAutoLabs/PyAutoLens/issues/887
- completed: 2026-11-24
- workspace-pr: https://github.com/PyAutoLabs/autolens_profiling/pull/535
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1796
- library-pr: https://github.com/PyAutoLabs/PyAutoLens/pull/888
- epic: likelihood-lifecycle (phase 5E; next 5F workspace prose)

Phase 5E, the runtime estimator, shipped as three PRs under one issue. A lens fit with a compute setup now logs an `Estimate:` line after PyAutoFit's `Parallel:` banner, and 5D's `number_of_cores="auto"` memory cap is live.

- **5E-1, autolens_profiling** (#535, 72939f36):
  - `runtime_estimates.yaml` v2: `n_pixels_masked` / `n_vis` / `source_pixels` read from each record's evidence JSON `configuration` (106/116 rows sized);
  - the measured η curve in the header (cited constant, with an ast-parsed equality test against autolens_inference `wall/model.py`);
  - `--copy-to <PyAutoLens>`.
- **5E-2, PyAutoFit** (#1796, dbdf4f9c): `resolve_fit_parallel(search, analysis, model=None)`; `runtime_estimate_line` calls the duck-typed `analysis.runtime_estimate(search, model, number_of_cores)`, logs it and records `estimate_line` in `parallel.json`. Raises and empty returns are ignored.
- **5E-3, PyAutoLens** (#888, 4dbe09e9):
  - `autolens/config/runtime_estimates.yaml` (v2);
  - `autolens/analysis/wall_model.py` (a port of the wall model);
  - `autolens/analysis/runtime_estimate.py`: cached v2 loader; `RuntimeEstimate`; match by decision_id + setup_id, otherwise setup_id + hardware_class + likelihood; nearest instrument by log size, otherwise a band; η only for numba; interferometer, weak and datacube uncalibrated; non-Nautilus searches get "no estimate";
  - the `AnalysisRuntimeEstimate` mixin first in `AnalysisDataset`, `AnalysisPoint` and `AnalysisWeak`;
  - exports `al.Setup`, `al.RuntimeEstimate`, `al.estimate_runtime`.
- **Design calls (human-approved 2026-11-24):**
  1. The estimator lives in PyAutoLens.
  2. Size matching, otherwise a band.
  3. Honest labels.
  4. `al.estimate_runtime` rather than `al.Setup.estimate`.
- **Gate:**
  - 5E-1: 1915 passed; ruff clean; `--check` current.
  - 5E-2: 4383 passed + 2 skipped + 1 xfailed; smoke 8/8.
  - 5E-3: 1154 passed + 1 xfailed; smoke 4/4.
  - Heart GREEN throughout.
  - PR CI GREEN. #888's first run failed only `test__hook__resolve_fit_parallel_logs_estimate` (`TypeError: resolve_fit_parallel() got an unexpected keyword argument 'model'`) until #1796 merged; the re-run was GREEN.
- **Traps:**
  - Library CI clones dependency repos at a *matching branch name*, otherwise main. Cross-repo PRs with different branch names must merge upstream first and then re-run the downstream CI.
  - Smoke uses the whole task root, so it sees in-progress sibling branches.
- **Caveats / follow-ups:**
  - The estimate is single-stage; there is no SLaM multi-stage pricing.
  - The euclid imaging/rectangular numba row has `peak_rss_gb` null, so no memory cap for fits matched to it.
  - `n_datasets` / `n_channels` multiplicity is not in the yaml.
  - autolens_profiling `reference_hosts.json` still declares η = 1.0 for the Pulse projection.
  - Interferometer and weak estimates read 2–5× low on held-out data (labelled uncalibrated).

## Original prompt

# Likelihood lifecycle phase 5E: runtime estimator: profiling exporter v2 with dataset sizes, a PyAutoFit estimate hook, and the PyAutoLens estimator, data file and memory cap

Type: feature
Target: PyAutoLens
Repos:
- autolens_profiling
- PyAutoFit
- PyAutoLens
Themes:
- hpc-gpu
- profiling
Difficulty: large
Autonomy: supervised
Priority: high
Status: active
Issued: 2026-11-24
Issue: https://github.com/PyAutoLabs/PyAutoLens/issues/887
Consequence: judge
Witness: autolens_profiling `runtime_estimates.yaml` v2 carries per-instrument size fields and the measured parallel-efficiency curve, and the exporter can copy it into PyAutoLens (`--copy-to`). PyAutoFit's `resolve_fit_parallel` calls a duck-typed `analysis.runtime_estimate(search, model, number_of_cores)` after the `Parallel:` line and logs its line without ever raising. PyAutoLens ships `autolens/config/runtime_estimates.yaml` with a cached, schema-checked loader, a `RuntimeEstimate` dataclass, the ported autolens_inference wall model, and public `al.estimate_runtime(dataset, model, search, setup, number_of_cores)` plus `al.Setup`. The lens analyses implement `runtime_estimate()` (the "Estimate:" line) and `resources_per_eval()` (5D's memory cap goes live). Rows are matched by `decision_id` + `setup_id` and the nearest instrument size, with a min–max band when unmatched. Lines are labelled "Nautilus heuristic", interferometer/weak are flagged "uncalibrated", and other samplers get "no estimate". Each repo's suite is green, and smoke passes at each ship.
Review-minutes: 30
Unattended: no
Lane: any
Gate: 5D MERGED (PyAutoFit#1795: `resolve_fit_parallel`, `resources_per_eval()` hook). Plan and design calls approved by the human 2026-11-24.
Epic: likelihood-lifecycle
Phase: 5
Parent: draft/research/autolens_profiling/likelihood_lifecycle_epic.md
Filed: 2026-11-24

## Context

- **Report §3.5, Estimator row:** a RuntimeEstimate (ms_per_eval, source record id, expected_evals labelled as the Nautilus heuristic until phase 7, parallel efficiency, wall); a data file `autolens/config/runtime_estimates.yaml` regenerated by an autolens_profiling exporter; the banner's "Estimate:" line.
- **Survey 2026-11-24:**
  - `lens/autolens_profiling/catalogue/runtime_estimates.yaml` (schema v1, tag 2026.10.25.1, 116 rows; fields likelihood, hardware_class, host_class, instrument, setup_id, role, decision_id, ms_per_eval, per_eval_source, cpus_per_eval, devices_per_eval, peak_rss_gb, workers_per_node, bound_by, calls_per_s_per_node, record_id).
  - There are no size fields, and the `parallel_efficiency` block is stale (1.0, "unmeasured").
  - The exporter is `scripts/misc/tooling/export_runtime_estimates.py --pulse ../PyAutoPulse [--check]` (stdlib; CI drift check in `.github/workflows/lint.yml:127-132`). Instrument sizes live in the profiling simulator summaries.
  - The wall model is `lens/autolens_inference/scripts/misc/wall/model.py` (stdlib): evals = 4.30 · n_live · d^1.637 · EVALS_FACTOR; a 0.014 s floor; 30 s startup; numba η {1:1.0, 2:.68, 4:.62, 8:.55, 16:.36, 32:.28}; per-call/per-eval overrides. It is Nautilus only; in-sample 0.56–1.59×; held-out interferometer 0.19–0.45× and weak 0.50–0.52× (uncalibrated).
  - Insight has no expected-evals table.
  - 5D `resolve_fit_parallel` (autofit `runtime.py`) has the search, the setup-resolved analysis and the `ParallelResolution`; it does not take the model yet.
  - `resources_per_eval()` expects `cpus_per_eval` and `peak_rss_gb`.
  - PyAutoLens ships `autolens/config/*` (pyproject package-data, MANIFEST.in). Follow PyAutoArray's direct-path loader precedent (`RULES_PATH`).
- **Design calls (human-approved 2026-11-24):**
  1. The estimator lives in PyAutoLens; Galaxy is untouched (no estimate line for Galaxy fits).
  2. Row matching: `decision_id` + `setup_id`, nearest instrument by size (masked pixels for imaging, n_vis for interferometer). Otherwise a min–max band, and the memory cap uses the largest `peak_rss_gb`.
  3. Honest labelling: "Nautilus heuristic"; interferometer/weak "uncalibrated (held-out 0.2–0.5×)"; other samplers "no estimate for <sampler>".
  4. The API is `al.estimate_runtime(...)`, not `al.Setup.estimate`, because `Setup` lives in PyAutoArray.
- **PRs, in order:** 5E-1 autolens_profiling (project repo; ship_workspace; no pending-release) → 5E-2 PyAutoFit (tiny) → 5E-3 PyAutoLens (medium).

## Out of scope

- Phase 7 sampler campaign and expected-evals tables.
- Workspace prose (5F) and assistant (5G).
- The default flip (R6).
- `ModelAnalysis` forwarding of `modify_before_fit` (separate follow-up).
