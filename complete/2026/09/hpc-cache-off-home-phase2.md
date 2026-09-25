Phase 2 of hpc-cache-off-home (autolens_profiling#310), PARTIAL: the autolens_profiling half shipped; the euclid_strong_lens_modeling_pipeline half was deliberately re-filed, not merged (human `/prm` choice "do 1", 2026-09-25).

Merged 2026-09-25 (human `/prm`; merge commit 76c73f87, head 0ed55f2 proven an ancestor of origin/main):
- PyAutoLabs/autolens_profiling#311 — phase 1's cache block in `activate.sh` (after the shared-venv `source`); every `NUMBA_CACHE_DIR`/`MPLCONFIGDIR=/tmp` export removed from 107 `hpc/` submits (199 lines; per-task `JAX_COMPILATION_CACHE_DIR` kept); `scripts/misc/test/test_fixed_light_s4.py` updated; `AGENTS.md` note.

Not shipped — re-filed: the euclid pipeline `activate.sh` block (local commit a7f0d0a, never pushed; passed `bash -n` + the fake-base witness) is `draft/maintenance/workspaces/hpc_cache_off_home_phase2_euclid.md`, with the patch embedded, Blocked-by `draft/bug/euclid/latent_total_source_flux_jax_vs_numpy_regression.md` (repo main "Tests" red since a89a468: `test_latent_euclid_variables_traces_under_jax_jit`, total_source_flux 3.511 jit vs 3.320 eager). a7f0d0a is kept on local branch `feature/hpc-cache-off-home-p2` in `lens/euclid_strong_lens_modeling_pipeline`.

Heart RED development override recorded (live "ok push it through", release validation FAILED (stage integrate); autonomy_log red-override row for autolens_profiling#311).

## Original prompt

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
Issued: 2026-09-25
Issue: https://github.com/PyAutoLabs/autolens_profiling/issues/310
Consequence: glance
Witness: same as phase 1 (`complete/2026/09/hpc-cache-off-home.md`, shipped as autolens_inference#14 / autolens_assistant#135 / autogalaxy_assistant#30 / autofit_assistant#51 — copy its block): each `activate.sh` HPC branch exports every cache under `${PYAUTO_HPC_CACHE:-$PYAUTO_HPC_BASE/../.cache}`; `git grep -E "(NUMBA_CACHE_DIR|MPLCONFIGDIR)=/tmp" -- hpc/` returns nothing in autolens_profiling (103 files on 2026-09-25) — keep any per-task `JAX_COMPILATION_CACHE_DIR` the profiling scripts set deliberately (fresh-cache autotune discipline).

Blocked on 2026-09-25: autolens_profiling claim `certified-solver-phase-c1-lane-rate` cleared 2026-09-25 (`complete/2026/09/certified-solver-phase-c1-lane-rate.md`); still blocked: euclid_strong_lens_modeling_pipeline claimed by `vis-lp-inspection-bundle` (`euclid-dr1-positions-gate`/`-finder` closed 2026-09-25). Apply phase 1's exact block once those merge. autolens_profiling's `activate.sh` sources the shared venv directly (no `.venv` branch) — put the block after that `source`.

Original request and background: see `complete/2026/09/hpc-cache-off-home.md`.
