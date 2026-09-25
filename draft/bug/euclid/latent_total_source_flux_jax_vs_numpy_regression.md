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

## Observed
The unit workflow on euclid_strong_lens_modeling_pipeline main went red at a89a468 (the merge of #104) and on #106:

    FAILED tests/test_compute_latent_variable.py::test_latent_euclid_variables_traces_under_jax_jit - AssertionError: latent 'total_source_flux' traced to 3.511084702451523 under jax.jit but evaluates to 3.3198742328017294 eagerly on NumPy (rel=0.001)

The result is 1 failed and 285 passed on main, with the same failure on Python 3.12 and 3.13. #104's own unit legs passed on 2026-09-24 with the same pipeline code, so the change is in the installed PyAuto stack (the library mains or released wheels the CI installs), not in the positions work. The #106 merge used a human red override for this reason (recorded on #106 and #105).

## Suspect
The library mains that moved between 2026-09-24 17:50Z and 2026-09-25 15:16Z: PyAutoArray and PyAutoLens (the inversion solver work, a certified solver or PDIP policy change, or a JAX change). total_source_flux depends on the source reconstruction, so an inversion solver path that differs between jit and eager would produce exactly this.

## Where to start
Diff the pip freeze of the passing CI run on #104 (2026-09-24) against the failing run on main at a89a468, then bisect the library commit.

## Also (small, same repo)
`hpc/sync` ROOT_FILES does not include the new root module `positions_finder.py` (added by #104/#106), so `hpc/sync push` never uploads it. It was rsynced to RAL by hand on 2026-09-25. Separately, `hpc/batch_cpu/output/` (1.6 GB of SLURM logs) and `hpc/upload_rest/` (738 MB) sit inside the pushed `hpc/` code dir, which makes `hpc/sync push --no-data` stall at the laptop's ~95 KB/s upload speed. Exclude them from CODE_DIRS pushes.
