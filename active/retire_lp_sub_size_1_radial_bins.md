# Retire lp over-sampling sub-size 1 in the test and developer workspaces

Type: refactor
Target: workspaces
Repos:
- @autolens_workspace_test
- @autolens_workspace_developer
Difficulty: easy
Autonomy: safe
Priority: normal
Status: formalised
Consequence: glance
Witness: no `sub_size_list` containing 1 and no `over_sample_size_lp=1` remains under autolens_workspace_test/scripts or autolens_workspace_developer; the regenerated autolens_workspace markdown/ pages no longer show `[4, 2, 1]`.
Review-minutes: 2
Unattended: ready
Issued: 2026-09-08
Issue: https://github.com/PyAutoLabs/autolens_workspace_test/issues/311
Filed: 2026-09-08

Original request (verbatim, from the profiling-production-representative session): "This should now be lp radial bins [4,2,2], as sub size of 1 causes gradient issues, so update this and make sure there is no where else through the porjects still using 1."

Context: autolens_profiling, euclid_strong_lens_modeling_pipeline and the subhalo_validation science project are swept to `[4,2,2]` under autolens_profiling#235. autolens_workspace/scripts already uses `[4,2,2]` everywhere (100 sites); only its rendered `markdown/` pages (imaging/start_here, imaging/modeling, group/start_here, group/modeling, multi_dataset/start_here) still show `[4, 2, 1]` and need a regeneration. Remaining live sites on 2026-09-08:

- autolens_workspace_test: scripts/imaging/jax_likelihood/rectangular.py, scripts/imaging/jax_likelihood/mge.py.
- autolens_workspace_developer (~35 files): source_science/ (fit_helpers.py, extract_mge_truth.py, results/**/make_diagnostics.py, fit_compare.py, make_*_plot.py), slam_pipeline/light_dark_mge.py, searches_minimal/_setup.py, plotting_alignment/*.py, jax_profiling/{jit,gradient,misc}/imaging/*.py, basis_regularization/*.py, mgl_slam_batch.py.

Scope: `[4,2,1]` → `[4,2,2]` (and `[16,4,1]` → `[16,4,2]`), `over_sample_size_lp=1` → 2; re-pin any expected-value constants that shift with a dated comment; regenerate the autolens_workspace markdown pages.
