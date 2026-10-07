# Active Tasks

## scribbler-wave2-radial-panels-regrid
- discussion: https://github.com/orgs/PyAutoLabs/discussions/23
- user-facing: true
- author: @samlange04 (external)
- issued: 2026-10-07
- session: Claude CLI (Fable 5.1, /community); session ID unavailable
- status: library-shipped, awaiting-merge
- repos:
  - PyAutoGalaxy: samlange04:feature/scribbler-radial-panels-regrid (PR #641, maintainer fixups pushed c0a9a387, CI 4/4 green)
  - PyAutoLens: feature/scribbler-regrid-reexport (DRAFT PR #770, red until #641 merges — CI clones autogalaxy main)
  - autolens_workspace: samlange04:feature/scribbler-radial-panels-regrid (DRAFT PR #583, fixup f81a3577)
  - autogalaxy_workspace: samlange04:feature/scribbler-radial-panels-regrid (DRAFT PR #254, no changes needed)
- library-pr: https://github.com/PyAutoLabs/PyAutoGalaxy/pull/641
- library-pr: https://github.com/PyAutoLabs/PyAutoLens/pull/770
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace/pull/583
- workspace-pr: https://github.com/PyAutoLabs/autogalaxy_workspace/pull/254
- summary: Wave 2 of the Scribbler proposal (radial-subtracted side-by-side panels, cross-grid mask regrid, white/black brushes, arcsinh default). Wave 1 (#635, docs #579/#251) is released in autogalaxy 2026.10.2.1.
- resume: Merge order is PyAutoGalaxy#641 → PyAutoLens#770 (mark ready, re-run CI) → release carrying both → approve fork CI on #583/#254, mark ready, merge. Workspace prose describes white/black brushes, so #583/#254 must not merge before the release. Human /prm for all merges.

## dashboard-freshness
- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/486
- issued: 2026-10-07
- prompt: active/dashboard_freshness.md
- session: Codex local; session ID unavailable
- status: library-dev
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/dashboard-freshness
- repos:
  - PyAutoBrain: feature/dashboard-freshness
  - PyAutoEars: feature/dashboard-freshness
  - PyAutoHeart: feature/dashboard-freshness
  - PyAutoHands: feature/dashboard-freshness
  - PyAutoMemory: feature/dashboard-freshness
  - PyAutoPulse: feature/dashboard-freshness
  - PyAutoInsight: feature/dashboard-freshness
  - PyAutoNerves: feature/dashboard-freshness
  - PyAutoGut: feature/dashboard-freshness
  - PyAutoEyes: feature/dashboard-freshness
  - PyAutoScientist: feature/dashboard-freshness
- summary: User approved shared freshness footer; <1h green, <24h yellow, otherwise red, unknown grey; exact timestamp and real owner Update link. Shared core then thirteen-board adoption. Merge human /prm.

## fork-context-darwin-test
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1661
- issued: 2026-10-07
- prompt: active/pyautofit_add_a_regression_test_for_fork.md
- session: Claude CLI (Opus 5.5 worker under Fable 5.1 /community); session ID unavailable
- status: library-dev
- worktree: ~/Code/PyAutoLabs-wt/fork-context-darwin-test
- repos:
  - PyAutoFit: feature/fork-context-darwin-test

## padded-single-image-recovery
- issue: https://github.com/PyAutoLabs/PyAutoLens/issues/771
- issued: 2026-10-07
- prompt: active/pyautolens_single_image_recovery_in_result_image.md
- session: Claude CLI (Opus 5.5 worker under Fable 5.1 /community); session ID unavailable
- status: library-dev
- worktree: ~/Code/PyAutoLabs-wt/padded-single-image-recovery
- repos:
  - PyAutoLens: feature/padded-single-image-recovery
- conflict-override: PyAutoLens also claimed by scribbler-wave2-radial-panels-regrid (#770, __init__.py re-export only; no file overlap) — orchestrator decision 2026-10-07
