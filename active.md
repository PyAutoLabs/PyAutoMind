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

## mgl-slam-batch-home
- issue: https://github.com/PyAutoLabs/autolens_workspace_developer/issues/135
- prompt: active/give_the_orphan_mgl_slam_batch_py.md
- issued: 2026-09-08
- session: claude --resume session_01BRfNgqR6AmVv99rvuoK3Gj
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/mgl-slam-batch-home
- repos:
  - autolens_workspace_developer: feature/mgl-slam-batch-home
- heart-ack: 2026-09-08 in-session YELLOW, reasons "workspace validation not passing (5 failed, 2 timeout, cloud#34099198772)", "release validation incomplete: no rehearsal evidence for v2026.9.8.1.dev75701" and "profiling drift on 3 pinned results"; none of them touch autolens_workspace_developer
