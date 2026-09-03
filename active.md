# Active Tasks

## human-readable-first-docs
- issue: https://github.com/PyAutoLabs/autolens_assistant/issues/120
- prompt: active/swap_docs_back_to_human_readable_first.md
- issued: 2026-09-03
- session: claude --resume session_01TRKarVxARKJ6VJN5Qc3521
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/human-readable-first-docs
- repos:
  - autolens_assistant: feature/human-readable-first-docs
  - autogalaxy_assistant: feature/human-readable-first-docs
  - PyAutoLens: feature/human-readable-first-docs
  - PyAutoGalaxy: feature/human-readable-first-docs
  - autolens_workspace: feature/human-readable-first-docs
  - autogalaxy_workspace: feature/human-readable-first-docs
- parallel-claim: autolens_workspace also claimed by gaussian-precompute-p3 (#528); file sets disjoint (that task touches only scripts/**/mass_stellar_dark/slam.py + its notebook; this task touches README.md, start_here.py + its notebook/markdown twins) — separate worktree per the disjoint-files rule, launched 2026-09-03 under the user's "do intake and then do work" instruction; second to merge rebases.
- heart-ack: 2026-09-03 PR-open only (never merge) under Heart RED; exact reasons from pyauto-heart readiness --json: "release validation FAILED (stage integrate)"; "PyAutoArray: open PR 11d old" — the same reason set the human acknowledged for gaussian-precompute-p3 earlier today; docs-only change unrelated to either reason; a further new reason at ship time re-blocks

## gaussian-precompute-p3
- issue: https://github.com/PyAutoLabs/autolens_workspace/issues/528
- prompt: active/gaussian_precompute_p3_downstream_sweep.md
- issued: 2026-09-03
- session: claude --resume session_01XhnA4pFN2NycuKc8Ni6s2R
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/gaussian-precompute-p3
- repos:
  - autolens_workspace: feature/gaussian-precompute-p3
- parallel-claim: autolens_workspace also claimed by image-source-mappings-p3 (#525); file sets disjoint (that branch touches features/pixelization/*, smoke_tests.txt, workspace_index.json, tutorials; this task touches only scripts/**/mass_stellar_dark/slam.py + its notebook) — human-approved 2026-09-03; second to merge rebases. RESOLVED at worktree time: image-source-mappings-p3 had already closed out — its active.md entry is retired, its worktree removed, and feature/image-source-mappings-p3 is merged into origin/main (#526, 31a7b6e4). worktree_check_conflict fired no conflict; this task is the sole live claim on autolens_workspace.
- heart-ack: 2026-09-03 human-acknowledged Heart RED for PR-open (never merge), exact reasons from pyauto-heart readiness --json: "release validation FAILED (stage integrate)"; "PyAutoArray: open PR 11d old"; "PyAutoLens: CI failure" (cleared on main by PyAutoLens#722, snapshot may lag) — a further new reason at ship time re-blocks
- epic: gaussian-deflections-precompute (phase 3; ledger draft/feature/autogalaxy/precompute_fixed_geometry_gaussian_deflections.md)

## cortex-checkin-p1-shed-review-slot
- issue: https://github.com/PyAutoLabs/PyAutoCortex/issues/9
- prompt: active/cortex_checkin_p1_shed_review_slot.md
- issued: 2026-09-03
- session: claude --resume session_013HsZA1ufn3msgPiDFxEXa6
- status: library-shipped, awaiting-merge (PRs open 2026-09-03; merge order PyAutoBrain -> PyAutoCortex; close-out via /prm)
- library-pr: https://github.com/PyAutoLabs/PyAutoCortex/pull/10
- library-pr: https://github.com/PyAutoLabs/PyAutoBrain/pull/348
- worktree: ~/Code/PyAutoLabs-wt/cortex-checkin-p1-shed-review-slot
- repos:
  - PyAutoCortex: feature/cortex-checkin-p1-shed-review-slot
  - PyAutoBrain: feature/cortex-checkin-p1-shed-review-slot
- heart: RED at ship time 2026-09-03, NOT acknowledged by a human. Exact reasons from `pyauto-heart readiness --json`: "release validation FAILED (stage integrate)"; "PyAutoArray: open PR 11d old". Both are release-chain facts about other repos; neither PyAutoCortex nor PyAutoBrain is in the release chain. PRs were opened, nothing merged; the merge decision needs the human, and an ack (or a green Heart) before it.
- ci: PyAutoBrain#348 green; PyAutoCortex#10 `check` green, `refresh` red until #348 merges (that workflow renders through PyAutoBrain **main**, which still calls the deleted `MEMBER_RE`) — a Brain/Cortex skew the workflow's own comment names
- epic: cortex-checkin (phase 1; ledger draft/maintenance/pyautocortex/cortex_checkin_epic.md). Phases 2 and 3 stack on branch `feature/cortex-checkin-p1-shed-review-slot` in both repos until it merges.

## cortex-checkin-p2-the-door
- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/349
- prompt: active/cortex_checkin_p2_the_door.md
- issued: 2026-09-03
- session: local CLI (Fable architect, Opus execution) — claude --resume session_013HsZA1ufn3msgPiDFxEXa6
- status: library-dev
- worktree: ~/Code/PyAutoLabs-wt/cortex-checkin-p2-the-door
- repos:
  - PyAutoBrain: feature/cortex-checkin-p2-the-door
  - PyAutoCortex: feature/cortex-checkin-p2-the-door
- parallel-claim: both repos are also claimed by cortex-checkin-p1-shed-review-slot (PyAutoCortex#9, PRs PyAutoBrain#348 / PyAutoCortex#10 open, unmerged). This is the epic's own stacking, not a collision: p2 branches FROM `feature/cortex-checkin-p1-shed-review-slot` in both repos and its PRs target that branch, so p1's deletions are already in p2's base. File sets are disjoint from p1's remaining work — p2 adds the `checkin` door to `agents/conductors/cortex/_cortex.py`, rewrites `skills/cortex/*` + `skills/COMMANDS.md`, adds check-in tests, and touches PyAutoCortex docs only (README/AGENTS/REFERENCE) — while p1 is finished and awaiting merge. Human-approved 2026-09-03 ("ok go" on the epic and its phases). worktree_check_conflict exits 1 by design here; phase 3 will stack on p2's branches in turn.
- epic: cortex-checkin (phase 2; ledger draft/maintenance/pyautocortex/cortex_checkin_epic.md). Retarget both PRs to main when phase 1 merges.
