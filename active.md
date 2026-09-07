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

## cortex-tasks-not-phases
- issue: https://github.com/PyAutoLabs/PyAutoCortex/issues/20
- library-pr: https://github.com/PyAutoLabs/PyAutoCortex/pull/21
- library-pr: https://github.com/PyAutoLabs/PyAutoBrain/pull/361
- issued: 2026-09-07
- session: claude --resume session_01EpM4gQikgEtCqpBJ3hzgct
- status: library-shipped, awaiting-merge
- worktree: ~/Code/PyAutoLabs-wt/cortex-tasks-not-phases
- repos:
  - PyAutoCortex: feature/cortex-tasks-not-phases
  - PyAutoBrain: feature/cortex-tasks-not-phases
