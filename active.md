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

## workspace-lp-sub-size-1-retire
- issue: https://github.com/PyAutoLabs/autolens_workspace_test/issues/311
- prompt: active/retire_lp_sub_size_1_radial_bins.md
- issued: 2026-09-08
- session: claude --resume session_01QUtSqZHfdCceS4Sxproayn
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/workspace-lp-sub-size-1-retire
- repos:
  - autolens_workspace_test: feature/workspace-lp-sub-size-1-retire
  - autolens_workspace_developer: feature/workspace-lp-sub-size-1-retire
- heart-ack: 2026-09-08 in-session (same reason set as #235), reasons "workspace validation not passing (5 failed, 2 timeout, cloud#34099198772 …)" and "release validation incomplete: no rehearsal for current source"

## profiling-post-235-followups
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/237
- prompt: active/breakdown_pixelization_stale_module_import.md
- issued: 2026-09-08
- session: claude --resume session_01QUtSqZHfdCceS4Sxproayn
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/profiling-post-235-followups
- repos:
  - autolens_profiling: feature/profiling-post-235-followups
- parallel-claim: autolens_profiling also claimed by retire-gpu1-mig-exclusion (#220, awaiting-merge, hpc/batch_gpu submits + activate.sh + hpc/README.md only); "file sets disjoint; own worktree approved by the human 2026-09-08"
- heart-ack: 2026-09-08 in-session (same reason set as #235), reasons "workspace validation not passing (5 failed, 2 timeout, cloud#34099198772 …)" and "release validation incomplete: no rehearsal for current source"
