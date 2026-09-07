# Active Tasks

## quick-update-tolerates-invalid-instance
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1567
- issued: 2026-09-07
- session: claude --resume session_01P5K4AXFBYMCPhbNFYA24YX
- status: library-dev
- worktree: ~/Code/PyAutoLabs-wt/quick-update-tolerates-invalid-instance
- repos:
  - PyAutoFit: feature/quick-update-tolerates-invalid-instance
  - euclid_strong_lens_modeling_pipeline: feature/quick-update-tolerates-invalid-instance
- summary: |
    Both legs taken: PyAutoFit guards manage_quick_update instance construction (log + skip); pipeline bounds vis_lp source MGE ell_comps to [-0.7, 0.7]. Library PR first, pipeline PR gated. Cortex relaunch of RAL 342301 task 3 is a follow-up, not this task.

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
