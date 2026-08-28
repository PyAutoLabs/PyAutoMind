# Active Tasks

## nuts-warm-start-driver-and-a100-probe
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/187
- prompt: active/nuts_warm_start_driver_and_a100_probe.md
- issued: 2026-08-28
- status: pr-open
- pr: https://github.com/PyAutoLabs/autolens_profiling/pull/188
- worktree: ~/Code/PyAutoLabs-wt/nuts-warm-start-driver-and-a100-probe
- repos:
  - autolens_profiling: feature/nuts-warm-start-driver-and-a100-probe
- note: registers `af.BlackJAXNUTS` as a first-class `nuts` searches sampler with PR#1522 warm-start,
  adds the imaging/mge/hst leaf + A100 probe submit (cold vs warm), and settles whether the parked
  SMC prototype (wsdev#113 / RAL 331058) can be resubmitted as a research row. RAL is put on this
  feature branch to run the probe and MUST return to main after merge.

## nautilus-test-mode-degenerate-corner
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1541
- prompt: active/nautilus_plotter_py_corner_cornerpy_raises_value.md
- issued: 2026-08-28
- status: library-dev
- worktree: ~/Code/PyAutoLabs-wt/nautilus-test-mode-degenerate-corner
- repos:
  - PyAutoFit: feature/nautilus-test-mode-degenerate-corner
- note: Heart RED 2026-08-28 — Nautilus/Dynesty TEST_MODE=1 gives ESS=1; corner_cornerpy guard becomes ESS-based. Workspace script untouched.

## repin-rectangular-mge-after-490
- issue: https://github.com/PyAutoLabs/autolens_workspace_test/issues/286
- prompt: active/rectangular_mge_jax_vmap_likelihood_pins_are.md
- issued: 2026-08-28
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/repin-rectangular-mge-after-490
- repos:
  - autolens_workspace_test: feature/repin-rectangular-mge-after-490
- note: Heart RED 2026-08-28 — bisected to PyAutoArray #490 (verified correctness fix); stale pins skipped by f0ef8f2. Re-pin only.

## interferometer-adapt-density-mesh
- issue: https://github.com/PyAutoLabs/autogalaxy_workspace/issues/230
- issued: 2026-08-28
- prompt: active/interferometer_adapt_density_mesh.md
- session: claude --resume b766a19b-260c-4b56-8d19-072fa9a34b28
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/interferometer-adapt-density-mesh
- repos:
  - autogalaxy_workspace: feature/interferometer-adapt-density-mesh
- note: mesh switch in modeling.py + galaxy_reconstruction.py only; fit.py / likelihood_function.py keep RectangularUniform by design.

## requarantine-delaunay-and-keep-abort-stack
- issue: https://github.com/PyAutoLabs/autolens_workspace_test/issues/287
- prompt: active/multi_dataset_jax_likelihood_delaunay_py_exceeds.md
- issued: 2026-08-28
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/requarantine-delaunay-and-keep-abort-stack
- repos:
  - autolens_workspace_test: feature/requarantine-delaunay-and-keep-abort-stack
  - PyAutoHands: feature/requarantine-delaunay-and-keep-abort-stack
- parallel-claim: autolens_workspace_test also claimed by repin-rectangular-mge-after-490 (#286); file sets disjoint (config/build/no_run.yaml vs scripts/imaging/jax_likelihood/rectangular_mge*.py); own worktree + own branch per the standing parallel-worktree practice.
- note: Heart RED 2026-08-28 — delaunay.py 1805s timeout is the XLA FftThunk/Eigen-pool deadlock (epic), not a library or profile bug; re-quarantine + make build_util keep the faulthandler stack.
