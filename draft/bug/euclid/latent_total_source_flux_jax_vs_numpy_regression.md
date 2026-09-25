# test_latent_euclid_variables_traces_under_jax_jit went red on main: total_source_flux differs by 6% between jax.jit and NumPy

Type: bug
Target: euclid
Repos:
- euclid_strong_lens_modeling_pipeline
Themes:
- euclid
- jax
- latent
Difficulty: small
Autonomy: supervised
Priority: high
Status: draft
Consequence: glance
Witness: `pytest tests/test_compute_latent_variable.py::test_latent_euclid_variables_traces_under_jax_jit` passes (total_source_flux JAX == NumPy within rel 1e-3); today it fails with 3.5111 (jit) vs 3.3199 (NumPy)
Review-minutes: 5
Unattended: ready
Filed: 2026-09-25
Updated: 2026-09-25

## Observed
The unit workflow on euclid_strong_lens_modeling_pipeline main went red at a89a468 (the merge of #104) and on #106:

    FAILED tests/test_compute_latent_variable.py::test_latent_euclid_variables_traces_under_jax_jit - AssertionError: latent 'total_source_flux' traced to 3.511084702451523 under jax.jit but evaluates to 3.3198742328017294 eagerly on NumPy (rel=0.001)

The result is 1 failed and 285 passed on main, with the same failure on Python 3.12 and 3.13. #104's own unit legs passed on 2026-09-24 with the same pipeline code, so the change is in the installed PyAuto stack (the library mains or released wheels the CI installs), not in the positions work. The #106 merge used a human red override for this reason (recorded on #106 and #105).

## Suspect
The library mains that moved between 2026-09-24 17:50Z and 2026-09-25 15:16Z: PyAutoArray and PyAutoLens (the inversion solver work, a certified solver or PDIP policy change, or a JAX change). total_source_flux depends on the source reconstruction, so an inversion solver path that differs between jit and eager would produce exactly this.

## Where to start
Diff the pip freeze of the passing CI run on #104 (2026-09-24) against the failing run on main at a89a468, then bisect the library commit.

## Also blocking (2026-09-25)
`draft/maintenance/workspaces/hpc_cache_off_home_phase2_euclid.md` — the euclid half of
`hpc-cache-off-home-phase2` (record `complete/2026/09/hpc-cache-off-home-phase2.md`) —
is `Blocked-by` this bug: its one-file `activate.sh` patch was held because this test is red on
main 94f9244 locally and in main CI "Tests" (red since a89a468; last green 3130898,
2026-09-22). Treat the 6% `total_source_flux` gap as a correctness regression in a science
quantity, not a tolerance to loosen: the Witness needs the jit and eager values to agree at
rel 1e-3, ideally with the root cause named. If stack drift is ruled out, the pipeline-side
range is 3130898..94f9244 — its only source change on the latent path is `util.py`
(e9798c8, d89e9ae, bd3ce0e; tests cf91184); the rest is the positions gate/finder
(`git log --oneline 3130898..94f9244` in the canonical checkout: 23 commits, #104 + #106).

## Also (small, same repo)
`hpc/sync` ROOT_FILES does not include the new root module `positions_finder.py` (added by #104/#106), so `hpc/sync push` never uploads it. It was rsynced to RAL by hand on 2026-09-25. Separately, `hpc/batch_cpu/output/` (1.6 GB of SLURM logs) and `hpc/upload_rest/` (738 MB) sit inside the pushed `hpc/` code dir, which makes `hpc/sync push --no-data` stall at the laptop's ~95 KB/s upload speed. Exclude them from CODE_DIRS pushes.
