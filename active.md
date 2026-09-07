# Active Tasks

## retire-gpu1-mig-exclusion
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/220
- workspace-pr: https://github.com/PyAutoLabs/autolens_profiling/pull/222
- heart-ack: 2026-09-05 in-session, single reason "release validation FAILED (stage integrate)" — organism-scope (PyAutoHeart Release Integrate run 33951278577); nothing in this branch is in the release chain
- issued: 2026-09-05
- session: claude --resume session_0117cr7VQNhHL2HzkGwQCDun
- status: awaiting-merge
- worktree: ~/Code/PyAutoLabs-wt/retire-gpu1-mig-exclusion
- repos:
  - autolens_profiling: feature/retire-gpu1-mig-exclusion
- parallel-claim: autolens_profiling also claimed by delaunay-nn-breakdown (#219); "file sets disjoint (hpc/batch_gpu submits, hpc/README.md, activate.sh vs _profile_cli.py + scripts/imaging/likelihood_breakdown/delaunay.py); prompt out-of-scope note says merge order does not matter; own worktree taken under --auto safe"

## lib-tests-compile-caches
- issue: https://github.com/PyAutoLabs/PyAutoHeart/issues/215
- library-pr: https://github.com/PyAutoLabs/PyAutoHeart/pull/217
- issued: 2026-09-06
- session: claude --resume session_01WYcmRnZf3cbC5Wth9bCkEg
- status: library-shipped, awaiting-merge
- repos:
  - PyAutoHeart: feature/lib-tests-compile-caches
- summary: |
    Census O1 widened: JAX + numba caches in lib-tests.yml, numba cache + content-stamped
    mtimes in smoke-tests.yml, cache state on every unit and script timing row. Web session,
    no task worktree (clone at /home/user/pyautoheart).

## defer-import-scipy-special-pyplot
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1565
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1566
- library-pr: https://github.com/PyAutoLabs/PyAutoLens/pull/729
- issued: 2026-09-06
- session: claude --resume session_01WYcmRnZf3cbC5Wth9bCkEg
- status: library-shipped, awaiting-merge
- repos:
  - PyAutoFit: feature/defer-import-scipy-special
  - PyAutoLens: feature/defer-import-pyplot
- summary: |
    Census O2 + O3: lazy TransformedMessage support so scipy.special leaves `import autofit`;
    function-local matplotlib imports in potential_correction/visualize.py so pyplot leaves
    `import autolens`. Two independent library PRs. Web session, no task worktree.

## smoke-fixed-overhead
- issue: https://github.com/PyAutoLabs/PyAutoHeart/issues/216
- library-pr: https://github.com/PyAutoLabs/PyAutoHeart/pull/218
- issued: 2026-09-06
- session: claude --resume session_01WYcmRnZf3cbC5Wth9bCkEg
- status: library-shipped, awaiting-merge (stacked on #217 — merge #217 first)
- repos:
  - PyAutoHeart: feature/smoke-fixed-overhead
- parallel-claim: PyAutoHeart also claimed by lib-tests-compile-caches (#215); both edit smoke-tests.yml, so this branch is stacked on feature/lib-tests-compile-caches and its PR opens against main once #215 merges (or rebases then). Same session, sequenced.
- summary: |
    Fixed per-leg overhead of the reusable smoke workflow: per-step measurement from the
    Actions API (clone 18-21 s + install 78-86 s per leg on autolens_workspace_test run
    34012149870), then depth-1 clones with the matching-branch fallback, a pip cache, and
    setup_s recorded as data. Web session, no task worktree.

