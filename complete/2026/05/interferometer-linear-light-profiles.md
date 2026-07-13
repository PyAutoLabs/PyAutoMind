## interferometer-linear-light-profiles
- issue: https://github.com/PyAutoLabs/autolens_workspace/issues/162
- completed: 2026-05-16
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace/pull/163
- workspace-pr: https://github.com/PyAutoLabs/autogalaxy_workspace/pull/75
- notes: Built scripts/interferometer/features/linear_light_profiles/ in both autolens_workspace (modeling, fit, likelihood_function, slam + README + __init__) and autogalaxy_workspace (modeling, fit, likelihood_function + README + __init__; no slam — SLaM is autolens-only). All use TransformerNUFFT (nufftax) for the per-iteration NUFFT of each linear basis component inside the JAX jit/vmap pipeline. Lens light omitted per interferometer convention (autolens); autogalaxy uses linear Sersic bulge + linear Exponential disk. autolens slam.py mirrors interferometer/features/pixelization/slam.py (SOURCE LP → SOURCE PIX 1 → SOURCE PIX 2 → MASS TOTAL) with the SOURCE LP source bulge swapped from MGE to linear SersicCore; SOURCE LP runs on TransformerNUFFT and pixelized stages switch to TransformerDFT + sparse operator. Phase 1 sanity sweep of the imaging linear_light_profiles/ scripts in both workspaces bundled into the same PRs: rewrote stale Basis/5-Gaussians sections to match actual model (Sersic+SersicCore for autolens, Sersic+Exponential for autogalaxy), fixed bulge/disk-vs-lens/source wording confusion in autolens likelihood_function.py (renamed image_2d_bulge/_disk → image_2d_lens_bulge/_source_bulge, fixed the two print(image_2d_bulge.slim) sites, removed misleading "this will raise an exception" block that no longer raised), fixed n_live=300 vs prose-says-75 mismatch in autogalaxy modeling.py (n_live now 75, prose now consistent), assorted typos (Althought, algabra, non-negligable, start.here.py, RectnagularMapper, autoogalaxy_workspace, lens galaxly's, Disadvatanges, lp_Linear). likelihood_function.py walkthroughs reproduce FitInterferometer.figure_of_merit to 4-5 decimal places; autogalaxy 2-component case nicely demonstrates positive-only solver (positive-negative returns bulge intensity ~-0.17 unphysical, positive-only correctly returns 0). Workspace conflict resolution: group-mass-stellar-dark also held autolens_workspace; cleared via file-level coexistence (this task: scripts/interferometer/...; that task: scripts/group/...) — same precedent as knn-barycentric + ag-interferometer-kwargs. worktree_check_conflict bypassed, worktree_create called directly. SLaM smoke ran all 4 stages in ~35s under PYAUTO_TEST_MODE=2. Notebook regeneration deferred to /generate_and_merge post-merge. z_features tracker: 2 shipped / 7 outstanding (interferometer-no-lens-light was removed during the audit since all interferometer scripts already assume no lens light).

## Original prompt

The imaging `features/linear_light_profiles` example needs reviewing before adapting to interferometer.

Once the imaging version is in good shape, adapt it to the interferometer context in
`scripts/interferometer/features/linear_light_profiles/` for **both** `autolens_workspace` and
`autogalaxy_workspace`.

Linear light profiles solve for intensity normalizations analytically given the model parameters,
which previously was prohibitively slow against visibilities because every iteration had to compute
the Fourier transform of every basis component. With nufftax (a JAX-friendly NUFFT — point to its
GitHub and credit it), the linear inversion is now fast in the visibility domain, so this feature
finally becomes practical for interferometer modeling. The script should describe this transition
explicitly and explain why older comments calling light profile fits "slow" no longer apply.
