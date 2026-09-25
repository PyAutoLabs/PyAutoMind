# Keep caches off `$HOME` on HPC — phase 2: autolens_profiling + euclid pipeline

Type: maintenance
Target: autolens_profiling
Repos:
- autolens_profiling
- euclid_strong_lens_modeling_pipeline
Difficulty: small
Autonomy: supervised
Priority: medium
Status: formalised
Filed: 2026-09-25
Consequence: glance
Witness: same as phase 1 (`complete/2026/09/hpc-cache-off-home.md`, shipped as autolens_inference#14 / autolens_assistant#135 / autogalaxy_assistant#30 / autofit_assistant#51 — copy its block): each `activate.sh` HPC branch exports every cache under `${PYAUTO_HPC_CACHE:-$PYAUTO_HPC_BASE/../.cache}`; `git grep -E "(NUMBA_CACHE_DIR|MPLCONFIGDIR)=/tmp" -- hpc/` returns nothing in autolens_profiling (103 files on 2026-09-25) — keep any per-task `JAX_COMPILATION_CACHE_DIR` the profiling scripts set deliberately (fresh-cache autotune discipline).

Blocked on 2026-09-25: autolens_profiling claim `certified-solver-phase-c1-lane-rate` cleared 2026-09-25 (`complete/2026/09/certified-solver-phase-c1-lane-rate.md`); still blocked: euclid_strong_lens_modeling_pipeline claimed by `vis-lp-inspection-bundle` (`euclid-dr1-positions-gate`/`-finder` closed 2026-09-25). Apply phase 1's exact block once those merge. autolens_profiling's `activate.sh` sources the shared venv directly (no `.venv` branch) — put the block after that `source`.

Original request and background: see `complete/2026/09/hpc-cache-off-home.md`.
