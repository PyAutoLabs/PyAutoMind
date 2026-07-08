# Active Tasks

## psf-oversample-workspace
- issue: https://github.com/PyAutoLabs/autolens_workspace/issues/232
- session: claude --resume 4bcb5c3c-c067-4955-8bcd-8a7d93128ca7
- status: workspace-dev
- autonomy: supervised (--auto, launched 2026-07-08, no heart-ack)
- worktree: /home/jammy/Code/PyAutoLabs-wt/psf-oversample-workspace
- repos:
  - autolens_workspace: feature/psf-oversample-workspace
  - autolens_workspace_test: feature/psf-oversample-workspace

## ep-examples-tests
- issue: https://github.com/PyAutoLabs/autofit_workspace/issues/81
- session: claude --resume 3589268b-e5c9-4b32-b655-d07f732ea300
- status: workspace-dev
- autonomy: supervised (--auto, launched 2026-07-08, plan approved in-session, no heart-ack)
- worktree: /home/jammy/Code/PyAutoLabs-wt/ep-examples-tests
- repos:
  - autofit_workspace: feature/ep-examples-tests
  - autofit_workspace_test: feature/ep-examples-tests

  - PyAutoGalaxy: feature/psf-oversample-galaxy

## ep-graphical-docs
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1333
- session: claude --resume 3589268b-e5c9-4b32-b655-d07f732ea300
- status: library-shipped, awaiting-merge
- pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1334
- autonomy: supervised (--auto, launched 2026-07-08; heart YELLOW acked in-session at ship)
- worktree: /home/jammy/Code/PyAutoLabs-wt/ep-graphical-docs
- repos:
  - PyAutoFit: feature/ep-graphical-docs

## ep-priors-fable-reassess
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1330
- session: claude --resume 3589268b-e5c9-4b32-b655-d07f732ea300
- status: awaiting-input — phase 0 complete; decision hub PyAutoFit#1331 open for maintainer/contributor guidance (fix-batch + 5 decisions)
- question: https://github.com/PyAutoLabs/PyAutoFit/issues/1331
- worktree: none (read-only reassessment on PyAutoFit main @ 0f26ff2d8; verdicts land in PyAutoMind bug/priors)
- repos:

## ep-statistics-audit
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1332
- session: claude --resume 3589268b-e5c9-4b32-b655-d07f732ea300
- status: phase-1-complete — F1–F9 verdict table on #1332; EP wiki page shipped (PyAutoMemory methods_wiki); EP fix batch (F1+F2+F3+F4+F8) pends #1331 guidance; Phase 2 (docs) ready to start
- worktree: none (read-only audit on PyAutoFit main; findings land in PyAutoMind + issue #1332)
- repos:

  - PyAutoArray: feature/psf-oversample-inversion
  - PyAutoArray: feature/psf-oversample-core









## profiling-drift-check
- issue: https://github.com/PyAutoLabs/PyAutoHeart/issues/37
- status: awaiting-merge
- pr: https://github.com/PyAutoLabs/PyAutoHeart/pull/38
- autonomy: supervised (--auto, launched 2026-07-08, plan on issue)
- worktree: /home/jammy/Code/PyAutoLabs-wt/profiling-drift-check
- repos:
  - PyAutoHeart: feature/profiling-drift-check

## assistant-deep-audit
- issue: https://github.com/PyAutoLabs/autolens_assistant/issues/35
- status: awaiting-merge (all phases shipped: PRs #36, #37, #38 open as drafts)
- prs: https://github.com/PyAutoLabs/autolens_assistant/pulls (36 recipes, 37 tooling, 38 wiki)
- pr: https://github.com/PyAutoLabs/autolens_assistant/pull/36
- autonomy: supervised (--auto, launched 2026-07-08)
- worktree: /home/jammy/Code/PyAutoLabs/autolens_assistant (in-place)
- repos:
  - autolens_assistant: feature/assistant-deep-audit, feature/assistant-deep-audit-tooling, feature/assistant-deep-audit-wiki
