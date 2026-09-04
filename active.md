# Active Tasks

## docs-followup-paid-plan-assistants
- issue: https://github.com/PyAutoLabs/autolens_assistant/issues/122
- prompt: active/docs_follow_up_to_human_readable_first.md
- issued: 2026-09-04
- session: local CLI (Fable architect, Opus execution) — claude --resume session_01Vwajqh36GQMzDcpTRoF5Qj
- status: library-dev
- worktree: ~/Code/PyAutoLabs-wt/docs-followup-paid-plan-assistants
- repos:
- heart-ack: 2026-09-04 PR-open only (never merge) under Heart RED; exact reasons from pyauto-heart readiness --json: "release validation FAILED (stage integrate)"; "PyAutoArray: open PR 12d old" — same reason set the human acknowledged for human-readable-first-docs (#120, merged 2026-09-04); docs-only follow-up unrelated to either reason; a further new reason at ship time re-blocks
- follow-up-to: human-readable-first-docs (complete/2026/09/human-readable-first-docs.md)

## cortex-checkin-p3-project-summary
- issue: https://github.com/PyAutoLabs/PyAutoCortex/issues/12
- prompt: active/cortex_checkin_p3_project_summary_prompts.md
- issued: 2026-09-03
- session: local CLI (Fable architect, Opus execution) — claude --resume session_013HsZA1ufn3msgPiDFxEXa6
- status: library-shipped, awaiting-merge (PRs open 2026-09-03; stacked on phases 1 and 2 — merge order PyAutoBrain#348 -> PyAutoCortex#10 -> PyAutoBrain#350 -> PyAutoCortex#11 -> PyAutoBrain#351 -> PyAutoCortex#13, retarget each phase's PRs to main as the phase below it merges; close-out via /prm)
- library-pr: https://github.com/PyAutoLabs/PyAutoBrain/pull/351
- library-pr: https://github.com/PyAutoLabs/PyAutoCortex/pull/13
- worktree: ~/Code/PyAutoLabs-wt/cortex-checkin-p3-project-summary
- repos:
  - PyAutoBrain: feature/cortex-checkin-p3-project-summary
  - PyAutoCortex: feature/cortex-checkin-p3-project-summary
- parallel-claim: p3 stacks on p2. Both repos are also claimed by cortex-checkin-p1-shed-review-slot (PRs PyAutoBrain#348 / PyAutoCortex#10) and cortex-checkin-p2-the-door (PyAutoBrain#350 / PyAutoCortex#11), both open and unmerged. This is the epic's own stacking, not a collision: p3 branches FROM `feature/cortex-checkin-p2-the-door` in both repos and its PRs target that branch, so p1's deletions and p2's door are already in p3's base. p1 and p2 are finished and awaiting merge; p3 is the only branch of the three still being written. Human-approved 2026-09-03 ("ok go" on the epic and its phases). `worktree_check_conflict` exits 1 by design here.
- heart: RED at ship time 2026-09-03, NOT acknowledged by a human. Exact reasons from `pyauto-heart readiness --json`: red "release validation FAILED (stage integrate)"; yellow "PyAutoArray: open PR 11d old". Both are release-chain facts about other repos; neither PyAutoBrain nor PyAutoCortex is in the release chain, and this branch is a conductor renderer, one `check` rule and docs. PRs were opened, nothing merged; the merge decision needs the human, and an ack (or a green Heart) before it.
- tests: Brain test_cortex_conductor 67 passed (13 new); full Brain suite 889 passed / 2 failed — both `test_branch_sweep` failures are pre-existing and reproduce unchanged on the phase-2 base (control-tested), not fixed here. PyAutoCortex test_cortex 95 passed (2 new); `cortex.py check` OK; `dashboard --check` current after regenerating the pages from inside the Cortex worktree with the Brain worktree's `_cortex.py`.
- ci: PyAutoBrain#351 green (pytest 3.12 + 3.13 pass; `docs / docs-build` is path-filtered and did not trigger — the diff touches no docs path). PyAutoCortex#13 `check` green, `refresh` red — the same Brain/Cortex skew phase 1 recorded on PyAutoCortex#10 and phase 2 on #11: that workflow renders through PyAutoBrain **main**, whose `_cortex.py` still calls the `MEMBER_RE` phase 1 deleted (traceback names `_refresh_index` on main, a function this branch does not have). It clears when PyAutoBrain#348 merges.
- epic: cortex-checkin (phase 3, last; ledger draft/maintenance/pyautocortex/cortex_checkin_epic.md). Merge order Brain before Cortex within each phase, p1 → p2 → p3; retarget each phase's PRs to main as the phase below it merges. The ledger now carries the full PR/issue map for all three phases.

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
- status: library-shipped, awaiting-merge (PRs open 2026-09-03; stacked on phase 1 — merge order PyAutoBrain#348 -> PyAutoCortex#10 -> PyAutoBrain#350 -> PyAutoCortex#11, retarget p2's PRs to main once p1 merges; close-out via /prm)
- library-pr: https://github.com/PyAutoLabs/PyAutoBrain/pull/350
- library-pr: https://github.com/PyAutoLabs/PyAutoCortex/pull/11
- worktree: ~/Code/PyAutoLabs-wt/cortex-checkin-p2-the-door
- repos:
  - PyAutoBrain: feature/cortex-checkin-p2-the-door
  - PyAutoCortex: feature/cortex-checkin-p2-the-door
- parallel-claim: both repos are also claimed by cortex-checkin-p1-shed-review-slot (PyAutoCortex#9, PRs PyAutoBrain#348 / PyAutoCortex#10 open, unmerged). This is the epic's own stacking, not a collision: p2 branches FROM `feature/cortex-checkin-p1-shed-review-slot` in both repos and its PRs target that branch, so p1's deletions are already in p2's base. File sets are disjoint from p1's remaining work — p2 adds the `checkin` door to `agents/conductors/cortex/_cortex.py`, rewrites `skills/cortex/*` + `skills/COMMANDS.md`, adds check-in tests, and touches PyAutoCortex docs only (README/AGENTS/REFERENCE) — while p1 is finished and awaiting merge. Human-approved 2026-09-03 ("ok go" on the epic and its phases). worktree_check_conflict exits 1 by design here; phase 3 will stack on p2's branches in turn.
- heart: RED at ship time 2026-09-03, NOT acknowledged by a human. Exact reasons from `pyauto-heart readiness --json`: red "release validation FAILED (stage integrate)"; yellow "PyAutoArray: open PR 11d old". Both are release-chain facts about other repos; neither PyAutoBrain nor PyAutoCortex is in the release chain, and this branch is a conductor verb plus docs. PRs were opened, nothing merged; the merge decision needs the human, and an ack (or a green Heart) before it.
- tests: Brain 874 passed / 3 failed — one (`test_gh_surface::test_every_gh_driving_skill_points_at_the_mapping`) was this branch's and is fixed; the two `test_branch_sweep` failures reproduce unchanged on the phase-1 base. Targeted re-run of test_cortex_conductor + test_skill_install + test_gh_surface: 68 passed. PyAutoCortex: `cortex.py check` OK, 115 passed, dashboard current.
- epic: cortex-checkin (phase 2; ledger draft/maintenance/pyautocortex/cortex_checkin_epic.md). Retarget both PRs to main when phase 1 merges. Phase 3 stacks on `feature/cortex-checkin-p2-the-door` in both repos — the remotes are left in place.
