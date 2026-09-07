# Active Tasks

## quick-update-tolerates-invalid-instance
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1567
- issued: 2026-09-07
- session: claude --resume session_01P5K4AXFBYMCPhbNFYA24YX
- status: library-dev, ship-blocked-heart-red
- worktree: ~/Code/PyAutoLabs-wt/quick-update-tolerates-invalid-instance
- repos:
  - PyAutoFit: feature/quick-update-tolerates-invalid-instance
  - euclid_strong_lens_modeling_pipeline: feature/quick-update-tolerates-invalid-instance
- summary: |
    Both legs implemented UNCOMMITTED in the worktree (2026-09-07): PyAutoFit fitness.py guard + test_quick_update_invalid_instance.py (non_linear: 803 passed, 1 skipped; regression test fails on main); pipeline initial_lens_model.py source MGE ell_comps -> [-0.7, 0.7] (verified 20 gaussians, 1 shared pair). Drafted commit/PR text in the session scratchpad; recreate from issue #1567 if lost. Ship blocked: Heart RED ("release validation FAILED (stage integrate)"; "workspace validation not passing ... cloud#34099198772") - neither reason is repaired by this branch, corrective-PR exception does not apply. Next: when Heart clears, /ship_library (PyAutoFit) then /ship_workspace (pipeline). Cortex relaunch of RAL 342301 task 3 is a follow-up, not this task.

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
