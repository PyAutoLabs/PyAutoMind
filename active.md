# Active Tasks

## slam-simultaneous-oversample-timeout
- issue: https://github.com/PyAutoLabs/autolens_workspace/issues/533
- issued: 2026-09-04
- status: awaiting-merge
- worktree: ~/Code/PyAutoLabs-wt/slam-simultaneous-oversample-timeout
- pr: https://github.com/PyAutoLabs/autolens_workspace/pull/534
- repos:
  - autolens_workspace: feature/slam-simultaneous-oversample-timeout
- summary: |
    scripts/multi_dataset/features/slam/simultaneous.py timed out (1805s vs a
    366.9s baseline) in PyAutoHeart's Release Integrate run after #523 switched
    its source_pix_2 / light_lp / mass_total analyses to a non-uniform
    over_sample_size_pixelization map. Diagnose and bring the script back inside
    the 1800s per-script cap.
