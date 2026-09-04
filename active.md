# Active Tasks

## heart-worktree-drift-hidden-dirs
- issue: https://github.com/PyAutoLabs/PyAutoHeart/issues/198
- issued: 2026-09-04
- status: library-shipped, awaiting-merge
- library-pr: https://github.com/PyAutoLabs/PyAutoHeart/pull/200
- worktree: ~/Code/PyAutoLabs-wt/heart-worktree-drift-hidden-dirs
- repos:
  - PyAutoHeart: feature/heart-worktree-drift-hidden-dirs
- summary: |
    worktree_drift.scan treats every directory under the wt root as a task
    worktree, so the user's JetBrains ~/Code/PyAutoLabs-wt/.idea is reported as
    a permanent orphan. Skip hidden dirs in the discovery sweep only (claimed
    paths keep going through note() unconditionally); extend
    tests/test_worktree_drift.py with a .idea-beside-a-real-orphan case.

## profiles-jit-powerlaw-exact-zero-atol
- issue: https://github.com/PyAutoLabs/autolens_workspace_test/issues/291
- issued: 2026-09-04
- status: awaiting-merge
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace_test/pull/292
- corrective-red:
  reason: release validation FAILED (stage integrate)
  authorization: https://github.com/PyAutoLabs/autolens_workspace_test/issues/291
- worktree: ~/Code/PyAutoLabs-wt/profiles-jit-powerlaw-exact-zero-atol
- repos:
  - autolens_workspace_test: feature/profiles-jit-powerlaw-exact-zero-atol
- summary: |
    Release Integrate run 33847995194 fails scripts/misc/profiles_jit.py on
    mp.PowerLaw deflections: numpy returns exactly 0.0 on-axis (PyAutoGalaxy#598
    exact unit-vector transform), JAX returns 1.2e-16, and the check is
    rtol-only. Add atol=1e-12 on the mp.PowerLaw checks, mirroring
    mp.ExternalPotential.

## board-family-helper
- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/352
- issued: 2026-09-04
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
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/slam-simultaneous-oversample-timeout
- repos:
  - autolens_workspace: feature/slam-simultaneous-oversample-timeout
- summary: |
    scripts/multi_dataset/features/slam/simultaneous.py timed out (1805s vs a
    366.9s baseline) in PyAutoHeart's Release Integrate run after #523 switched
    its source_pix_2 / light_lp / mass_total analyses to a non-uniform
    over_sample_size_pixelization map. Diagnose and bring the script back inside
    the 1800s per-script cap.
