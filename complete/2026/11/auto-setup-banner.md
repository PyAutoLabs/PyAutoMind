## auto-setup-banner
- issue: https://github.com/PyAutoLabs/PyAutoGalaxy/issues/754
- completed: 2026-11-25
- library-pr: https://github.com/PyAutoLabs/PyAutoNerves/pull/224
- library-pr: https://github.com/PyAutoLabs/PyAutoArray/pull/713
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1797
- library-pr: https://github.com/PyAutoLabs/PyAutoGalaxy/pull/755
- library-pr: https://github.com/PyAutoLabs/PyAutoLens/pull/889
- epic: likelihood-lifecycle (phase 5 follow-up; next 5F)

The automatic compute-setup choice is now visible and concise. A fit prints one header line saying this is the automatic CPU/GPU setup choice, then aligned, contiguous `Setup:` / `Parallel:` / `Estimate:` lines. When the setup acts outside modeling (a lazy sparse-operator build, or an aggregator reload reapplying setup.json), a one-line notice says so.

- **Format** approved by the human on 2026-11-25: "pretty much good, but maybe also have a header … and make sure such a message appears outside of modeling too so a user knows it happened".
- **The PRs**, all sharing the branch `feature/auto-setup-banner` so each repo's CI tested them together, merged in order:
  - Nerves#224 (3af6de8d): detect_gpu respects `JAX_PLATFORMS`.
  - Array#713 (5240c7e8): the lazy-build notice.
  - Fit#1797 (cc764bf7): `Parallel:` with the device; `log_fit_start` makes no JAX claim.
  - Galaxy#755 (9756fa9c): header + Setup line logged at the end of `modify_before_fit`; the not-set line; the aggregator notice; `resolve_setup(model, log_banner=...)`.
  - Lens#889 (0c617e7d): wall-first Estimate.
- **Bug found by the demo** (and the reason for the Nerves PR): once PyAutoFit's old fit-start line, which imported JAX by calling `jax.devices()`, was removed, `detect_gpu` fell back to `nvidia-smi` and auto picked `JAX · GPU · dense` on a laptop with `JAX_PLATFORMS=cpu`, so the fit ran a GPU setup on the CPU. Now a `JAX_PLATFORMS` / `JAX_PLATFORM_NAME` that names no `cuda`/`rocm`/`gpu` means no GPU.
- **PyAutoLens claim override:** human-approved. The `cluster-family-fit-figures` claim was stale (its PyAutoLens#884 was merged); its close-out stays with its owning session.
- **Gate:** suites 384 / 2614 / 4385 + 2 skipped + 1 xfailed / 1664 / 1155 + 1 xfailed; Heart GREEN; smoke 8/8 over the task root; all PR CI GREEN.
- **Trap:** an override of `resolve_setup(self, model)` needs `**kwargs` for the new `log_banner` keyword.

## Original prompt

# Likelihood lifecycle phase 5 follow-up: a concise automatic compute-setup banner at fit start, and notices when the setup acts outside modeling

Type: feature
Target: PyAutoGalaxy
Repos:
- PyAutoArray
- PyAutoFit
- PyAutoGalaxy
- PyAutoLens
Themes:
- hpc-gpu
- profiling
Difficulty: medium
Autonomy: supervised
Priority: high
Status: active
Issued: 2026-11-25
Issue: https://github.com/PyAutoLabs/PyAutoGalaxy/issues/754
Consequence: judge
Witness: A test-mode `al.AnalysisImaging(dataset, setup="auto")` + `af.Nautilus(number_of_cores="auto")` fit prints, with no contradicting line before it, one header line stating that this is the automatic CPU/GPU compute-setup choice, followed together by the aligned `Setup:`, `Parallel:` and `Estimate:` lines in the approved concise format. The stale "Starting non-linear search with JAX (CPU: cpu)." claim is gone, and the device is reported in `Parallel:` once known. Explicit and `PYAUTO_SETUP` setups get their own header wording; no setup gives one "not set (auto would choose …)" line. Outside modeling, a lazy sparse-operator build (`lazy_sparse_operator: auto`) and an aggregator reload that reapplies `setup.json` each print one concise notice in the same "compute setup" voice. All four suites are green, and smoke passes.
Review-minutes: 20
Unattended: no
Lane: any
Gate: 5A–5E MERGED. Human approved the format on 2026-11-25 ("pretty much good, but maybe also have a header … and make sure such a message appears outside of modeling too so a user knows it happened"). Ships before 5F, so the 5F `guides/advanced/auto_setup.py` guide shows the final output.
Epic: likelihood-lifecycle
Phase: 5
Parent: draft/research/autolens_profiling/likelihood_lifecycle_epic.md
Filed: 2026-11-25

## Context

- **Observed 2026-11-25** (a test-mode run from autolens_workspace):
  - PyAutoFit `log_fit_start` prints "Starting non-linear search with JAX (CPU: cpu)." before `modify_before_fit`; the setup then picked numba.
  - The Galaxy Setup line reads `numba/cpu/sparse/fp64 (8 CPU cores) · rule imaging-rectangular-standard-cpu-many-core · extrapolated (decision imaging-rectangular-standard-cpu-many-core) · override: PYAUTO_SETUP`, with the id repeated and no reason for "extrapolated".
  - Setup, Parallel and Estimate are split by warnings and other log lines.
- **Approved target format** (the timestamp/module prefix comes from the workspace `logging.yaml` and is unchanged). The label column is aligned and the lines are logged consecutively:

  ```
  Automatic compute setup (CPU/GPU choice from setup="auto"; override with PYAUTO_SETUP or setup=...):
  Setup:    numba · CPU · sparse operator · fp64   (rule imaging/rectangular · extrapolated: 8 cores, rules measured on ≥16-core nodes)
  Parallel: 8 workers (auto: detected cores)
  Estimate: ~6.4 min on this hardware   (283 ms/eval, euclid cell · Nautilus n_live=50 ≈ 4.6e3 evals, heuristic · η=0.55)
  ```

  - **Explicit setup:** header `Compute setup (set explicitly by setup=...):`. **PYAUTO_SETUP:** `Compute setup (set by PYAUTO_SETUP=<id>):`.
  - **No setup:** one line, `Compute setup: not set (auto would choose numba · CPU · sparse operator · fp64; pass setup="auto")`.
  - **JAX:** `Parallel: 1 worker (JAX on CPU)` / `(JAX on GPU: <name>)`.
- **Outside modeling:**
  - Array lazy build: `Automatic compute setup: built the numba sparse operator for this dataset (256 image pixels, 0.12 s; cached; lazy_sparse_operator: auto)`, or the interferometer w-tilde equivalent with visibilities and "chunked".
  - Galaxy aggregator reapply: `Compute setup: reapplied numba_cpu_sparse_fp64 from the search's setup.json`.
  - `apply_setup` itself stays silent, so modeling doesn't print twice.

## Out of scope

- The global log format (workspace `logging.yaml`).
- The 5F workspace guide and prose.
- The default flip (R6).
