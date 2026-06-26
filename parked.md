# Parked tasks

Tasks that were started or scoped but are not currently in flight. Listed
here so they remain visible across machines instead of disappearing into
unindexed worktrees or stashes. Move an entry back to `active.md` (or to
`planned.md` if re-scoping is needed) when work resumes; move to
`complete.md` once shipped.

## kaplinghat-sidm-cored-nfw
- issue: https://github.com/PyAutoLabs/PyAutoLens/issues/564
- parked: 2026-06-09
- status: parked-outside-current-release
- library-pr:
  - https://github.com/PyAutoLabs/PyAutoGalaxy/pull/471
  - https://github.com/PyAutoLabs/PyAutoLens/pull/567
- workspace-pr:
  - https://github.com/PyAutoLabs/autolens_workspace_test/pull/139
- worktree: ~/Code/PyAutoLabs-wt/kaplinghat-sidm-cored-nfw
- suggested-branch: feature/kaplinghat-sidm-cored-nfw
- classification: library
- affected-repos:
  - PyAutoGalaxy
  - PyAutoLens
  - autolens_workspace_test
- notes: |
    Parked outside the current release train per user instruction that
    Kaplinghat should not be included in this release. Removed `pending-release`
    from PyAutoGalaxy#471, PyAutoLens#567, and autolens_workspace_test#139.
    Worktree remains on disk for later resume, but active repo claims were
    released so current release-failure fixes can use autolens_workspace_test.

## psf-oversampling
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/299 (OPEN)
- parked: 2026-05-06
- classification: library (then workspace follow-up)
- suggested-branch: feature/psf-oversampling
- repos when resumed: PyAutoArray (primary), PyAutoGalaxy, autolens_workspace_test, autolens_workspace
- resume command: /start_library
- notes: |
    Parked — no resources claimed. Task worktree was created during /start_library
    but removed without edits; local feature/psf-oversampling branches deleted
    from PyAutoArray and PyAutoGalaxy. Both repos are free for other tasks.
    Restart with /start_library; it will recreate the worktree and the
    feature/psf-oversampling branches off origin/main.

    Phasing (smaller tasks, agreed mid-session):
      1. over_sample_util: Mask2D upscale-by-N + fine->native sum-reduce helpers + tests
      2. Convolver: add convolve_over_sample_size kwarg (default 1, no behaviour change) + test
      3. Convolver: bin-down branch in all four conv paths, gated > 1 + brute-force test
      4. Imaging dataset: kwargs + 2 construction-time guards (adaptive over-sample, sparse)
      5. GridsDataset: expose oversampled grids when > 1
      6. OperateImage + FitImaging caller threading (PyAutoGalaxy)
      7. Inversion mapping audit + assertion (mapping.py / abstract.py)
      8. End-to-end library integration test
      (workspace) extend convolution.py + new convolution_oversampled.py + simulator.py

## rectangular-spline-cdf
- parked: 2026-05-08
- classification: library (PyAutoArray)
- location: PyAutoArray stash@{0} ("On rectangular-spline-cdf: ... 727-line rectangular.py refactor + tests, parked 2026-05-08 from worktree before worktree_remove")
- notes: |
    727-line refactor of autoarray/inversion/mesh/interpolator/rectangular.py + 51
    lines of test updates, parked as a git stash on canonical PyAutoArray when its
    worktree was removed. To resume, create a feature branch off main and
    `git stash apply` (do NOT pop — keep the stash until merged). The refactor
    splits forward/reverse spline interpolation into jax-friendly variants and
    consolidates numpy fallbacks; quick-look diff before applying.

## lens-config-robustness
- parked: 2026-05-19 (worktree last touched)
- classification: workspace (autolens_workspace_developer)
- location: orphan worktree at ~/Code/PyAutoLabs-wt/lens-config-robustness/
- branch: feature/lens-config-robustness (canonical local copy deleted post-merge audit;
  remote upstream gone)
- notes: |
    Orphan worktree found during 2026-05-28 repo hygiene. Holds untracked
    `dataset/imaging/config_0_{1,2,3,4}_*/` synthetic-truth datasets and
    `source_science/{extract_mge_lens_truth,fit_helpers,lens_configs,
    run_all_tests,sim_helpers}.py`. The shipped branch was merged via a prior
    /ship_workspace but this worktree was never cleaned up.
    Action: inspect the untracked files; if any are wanted, commit them onto
    a fresh branch via /start_workspace then `worktree_remove
    lens-config-robustness`. Otherwise just `worktree_remove`.

## pyauto-update-digest
- parked: 2026-05-17 (worktree last touched)
- classification: workflow (PyAutoMind)
- location: orphan worktree at ~/Code/PyAutoLabs-wt/pyauto-update-digest/
- branch: feature/pyauto-update-digest (clean, no changes)
- notes: |
    Orphan worktree containing only a clean PyAutoMind checkout on the
    branch. No staged or unstaged changes. Action: `worktree_remove
    pyauto-update-digest`.

## strip-non-jit-noise-add-alma-high-res
- parked: 2026-05-18 (worktree last touched)
- classification: developer-tooling (autolens_profiling + autolens_workspace_developer)
- location: orphan worktree at ~/Code/PyAutoLabs-wt/strip-non-jit-noise-add-alma-high-res/
- branch: feature/strip-non-jit-noise-add-alma-high-res (merged to origin/main, upstream gone)
- notes: |
    Orphan worktree found during 2026-05-28 repo hygiene. Holds modifications
    to 9 likelihood scripts in autolens_profiling and 1 file in
    autolens_workspace_developer plus untracked alma_high_res datasets.
    The branch was merged (origin/main is ahead by 19) but this worktree
    kept evolving after the merge.
    Action: review the diffs; if the post-merge edits are wanted, commit on
    a new branch; otherwise `worktree_remove strip-non-jit-noise-add-alma-high-res`.
