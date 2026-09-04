# Active Tasks

## board-family-helper
- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/352
- issued: 2026-09-04
- prompt: active/board_family_footer_shared_helper.md
- status: library-dev
- worktree: ~/Code/PyAutoLabs-wt/board-family-helper
- repos:
  - PyAutoBrain: feature/board-family-helper
- summary: |
    board/_theme.py gains board_links(base_url, current) reading the canonical
    board: boards: block of config/policy.yaml (stdlib regex, no yaml import),
    so the sibling renderers stop carrying stale hard-coded BOARD_FAMILY
    tuples. bin/morning.sh also ticks and publishes the Heart dev-box board
    beside the Brain one, so the Heart Pages board stops rendering grey.

## heart-board-family-footer
- issue: https://github.com/PyAutoLabs/PyAutoHeart/issues/199
- issued: 2026-09-04
- status: library-dev
- worktree: ~/Code/PyAutoLabs-wt/heart-board-family-footer
- repos:
  - PyAutoHeart: feature/heart-board-family-footer
- summary: |
    heart/dashboard.py replaces its hard-coded BOARD_FAMILY tuple (no Cortex
    chip, wrong order) with the theme's board_links helper, keeping the legacy
    tuple only as a fallback for an older PyAutoBrain checkout. Touches
    heart/dashboard.py and tests/test_dashboard.py only — the concurrent
    heart-worktree-drift-hidden-dirs task owns heart/checks/worktree_drift.py.

## hands-board-family-footer
- issue: https://github.com/PyAutoLabs/PyAutoHands/issues/276
- issued: 2026-09-04
- status: library-dev
- worktree: ~/Code/PyAutoLabs-wt/hands-board-family-footer
- repos:
  - PyAutoHands: feature/hands-board-family-footer
- summary: |
    autohands/board.py replaces its hard-coded BOARD_FAMILY tuple with the
    theme's board_links helper, so the release board's footer carries Cortex
    and the canonical chip order.

## memory-board-family-footer
- issue: https://github.com/PyAutoLabs/PyAutoMemory/issues/87
- issued: 2026-09-04
- status: library-dev
- worktree: ~/Code/PyAutoLabs-wt/memory-board-family-footer
- repos:
  - PyAutoMemory: feature/memory-board-family-footer
- summary: |
    scripts/board.py replaces its hard-coded BOARD_FAMILY tuple with the
    theme's board_links helper, so the knowledge board's footer carries Cortex
    and the canonical chip order.
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
