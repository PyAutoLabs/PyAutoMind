# Active Tasks

## remove-pulse-compat
- issue: https://github.com/PyAutoLabs/PyAutoHeart/issues/20
- session: codex
- status: awaiting merge of PyAutoBrain PR #13; all other repos already shipped
- worktree: none
- suggested-branch: feature/remove-pulse-compat
- repos:
  - PyAutoHeart
  - PyAutoBrain
  - PyAutoBuild
  - admin_jammy
- progress: |
    PyAutoHeart pyauto-pulse shim removed; PyAutoBuild autobuild CLI (#113)
    and library CI workflows (#573) migrated to pyauto-heart; admin_jammy
    has no pulse refs. Remaining: PyAutoBrain PR #13 (retire pyauto-agent
    shim + correct stale shim docs) —
    https://github.com/PyAutoLabs/PyAutoBrain/pull/13

## aggregator-output-contracts
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1324
- session: codex
- status: library-dev
- worktree: ~/Code/PyAutoLabs-wt/aggregator-output-contracts
- suggested-branch: feature/aggregator-output-contracts
- repos:
  - PyAutoFit: feature/aggregator-output-contracts
  - autogalaxy_workspace: feature/aggregator-output-contracts
  - autolens_workspace: feature/aggregator-output-contracts
  - autolens_workspace_test: feature/aggregator-output-contracts
