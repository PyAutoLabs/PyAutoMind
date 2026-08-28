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
- status: awaiting-merge
- worktree: ~/Code/PyAutoLabs-wt/nautilus-test-mode-degenerate-corner
- repos:
  - PyAutoFit: feature/nautilus-test-mode-degenerate-corner
- note: Heart RED 2026-08-28 — Nautilus/Dynesty TEST_MODE=1 gives ESS=1; corner_cornerpy guard becomes ESS-based. Workspace script untouched.
- pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1542

## repin-rectangular-mge-after-490
- issue: https://github.com/PyAutoLabs/autolens_workspace_test/issues/286
- prompt: active/rectangular_mge_jax_vmap_likelihood_pins_are.md
- issued: 2026-08-28
- status: awaiting-merge
- worktree: ~/Code/PyAutoLabs-wt/repin-rectangular-mge-after-490
- repos:
  - autolens_workspace_test: feature/repin-rectangular-mge-after-490
- note: Heart RED 2026-08-28 — bisected to PyAutoArray #490 (verified correctness fix); stale pins skipped by f0ef8f2. Re-pin only.
- pr: https://github.com/PyAutoLabs/autolens_workspace_test/pull/288

## requarantine-delaunay-and-keep-abort-stack
- issue: https://github.com/PyAutoLabs/autolens_workspace_test/issues/287
- prompt: active/multi_dataset_jax_likelihood_delaunay_py_exceeds.md
- issued: 2026-08-28
- status: awaiting-merge
- worktree: ~/Code/PyAutoLabs-wt/requarantine-delaunay-and-keep-abort-stack
- repos:
  - autolens_workspace_test: feature/requarantine-delaunay-and-keep-abort-stack
  - PyAutoHands: feature/requarantine-delaunay-and-keep-abort-stack
- parallel-claim: autolens_workspace_test also claimed by repin-rectangular-mge-after-490 (#286); file sets disjoint (config/build/no_run.yaml vs scripts/imaging/jax_likelihood/rectangular_mge*.py); own worktree + own branch per the standing parallel-worktree practice.
- note: Heart RED 2026-08-28 — delaunay.py 1805s timeout is the XLA FftThunk/Eigen-pool deadlock (epic), not a library or profile bug; re-quarantine + make build_util keep the faulthandler stack.
- pr: https://github.com/PyAutoLabs/autolens_workspace_test/pull/289 + https://github.com/PyAutoLabs/PyAutoHands/pull/271

## numba-hst-curvature-matrix-speedup
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/505
- prompt: active/numba_cpu_hst_curvature_matrix_speedup.md
- issued: 2026-08-28
- session: claude --resume session_01SqrSVGPrFcUB1vvDsoTw3n
- status: library-dev
- worktree: ~/Code/PyAutoLabs-wt/numba-hst-curvature-matrix-speedup
- parallel-claim: autolens_profiling is also claimed by `nuts-warm-start-driver-and-a100-probe`; file sets are disjoint (this task: `scripts/imaging/likelihood_breakdown/`, `results/breakdown/imaging/`, `results/notes/`; NUTS: `scripts/misc/searches/`, `scripts/imaging/searches/nuts/`, `results/notes/inference/`). Human approved an own parallel worktree 2026-08-28. COMMIT DISCIPLINE: explicit pathspecs only in autolens_profiling, never `git add -A`.
- repos:
  - PyAutoArray: feature/numba-hst-curvature-matrix-speedup
  - autolens_profiling: feature/numba-hst-curvature-matrix-speedup
- note: Phase 1 of the F speed-up on the numba CPU path at HST: instrument F's sub-blocks, remove
  redundant passes, FFT the dense mapper×linear-func convolution if the split confirms it; >=2x on F,
  pins unchanged.

## nautilus-plotter-real-search-cap
- issue: https://github.com/PyAutoLabs/autofit_workspace/issues/149
- prompt: active/nautilus_plotter_py_corner_cornerpy_raises_value.md
- issued: 2026-08-28
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/nautilus-plotter-real-search-cap
- repos:
  - autofit_workspace: feature/nautilus-plotter-real-search-cap
- note: workspace half of nautilus-test-mode-degenerate-corner (PyAutoFit#1542) after the human declined a global test-mode budget change — ENV: real_search + explicit n_like_max in nautilus_plotter.py.
