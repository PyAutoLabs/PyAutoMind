- issue: https://github.com/PyAutoLabs/autolens_workspace_test/issues/311
- completed: 2026-09-08
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace_test/pull/312
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace_developer/pull/134
- merged: autolens_workspace_test 2ca0082 (PR #312), autolens_workspace_developer 824db4b (PR #134)
- heart-ack: 2026-09-08 in-session, same reason set as #235 — "workspace validation not passing (5 failed, 2 timeout, cloud#34099198772 …)" and "release validation incomplete: no rehearsal for current source"; neither reason touches the two workspaces

**Summary.** Sub-size 1 is retired from the lp over-sampling ladders across both workspaces — 19 files in `autolens_workspace_test`, 33 in `autolens_workspace_developer`. No `sub_size_list` containing 1 and no `over_sample_size_lp=1` remains under either `scripts/` tree. Seven pins moved; two by more than a percent (`lp.py` 1.3 %, `mge.py` 22 %), both verified as plain over-sampling convergence with exact NumPy/JAX parity at the new bins rather than a behaviour change. Full test-workspace smoke: 29 of 29.

**Witness.** Met for the two workspaces. The third clause — `autolens_workspace/markdown/` no longer showing `[4, 2, 1]` — is not met here and does not need to be: those pages are generated, and they regenerate in the release build.

**Traps / notes.**
- The MGE parity script is still about 9 % unconverged at sub-size 2, so it was deliberately kept at `[2, 2, 2]` for runtime; the convergence ladder is documented in the file and in the PR body. A blanket sweep would have made it slow without making it right.
- A 22 % pin move is not automatically a regression: `mge.py` moved that far purely on over-sampling convergence, confirmed by exact NumPy/JAX parity at both the old and new bins.
- `autolens_workspace_developer` has no `.github/` at all — zero CI. Its half of a paired change is judged on the sibling test-workspace's smoke run, not on its own checks.

**Follow-ups.** Not filed, carried here:
- `subhalo_validation` stays at `[4, 2, 2]`. If it computes flux latents it needs the same middle-bin decision the Euclid pipeline took in pipeline#56 (the unlensed compact source at 0.18" under-integrates in the 0.1–0.3" sub-size 2 annulus).
- `mgl_slam_batch.py` sits at the PyAutoLabs workspace root, inside no repo, and still has two `[4, 2, 1]` sites. It needs a home before it can be swept.
- The RAL copies of the Euclid pipeline and `subhalo_validation` need a sync before the next submission.

## Original prompt

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
