# Detect follow-ups on closed and answered community threads

- issue: https://github.com/PyAutoLabs/PyAutoEars/issues/19
- completed: 2026-10-07
- workspace-pr: https://github.com/PyAutoLabs/PyAutoBrain/pull/489
- workspace-pr: https://github.com/PyAutoLabs/PyAutoEars/pull/20
- summary: New external comments after closure or an accepted answer return a thread to Community review without requiring contributors to reopen it. Ears records activity evidence and source links; Community judges actionability and checks the acting account's permission.

## Merge evidence

Human-authorized `/prm`; Brain #489 merged first at 76c832cacec84b6b6105ee52af4fab47adcb5ab9, then Ears #20 at c290ffd8215dca92668b7788ac6784938b5ebfef. Both feature tips are ancestors of origin/main in full local clones.

All runs and jobs on both exact feature heads were completed/success: Brain run 37598552428 (Python 3.12/3.13), Ears run 37598621790 (Python 3.12/3.13 and browser), five jobs total. Both PRs were CLEAN/MERGEABLE before merge.

## Validation and boundaries

97 local Ears tests and 66 targeted Brain tests passed; generated state validates. Chromium passed at 390/1280 widths and in light/dark themes, including copy fallback and the follow-up link. Live read-only collection detects Discussion #13 with complete coverage despite its closed/answered state. Jammy2211 can reopen that Discussion; this does not establish any contributor's rights.

Collection is bounded by pagination and surfaces incomplete coverage. Quiet closed issue history is skipped; closed PRs are excluded. New activity is a review candidate, not automatic semantic classification or permission to reopen. Direct bounded triage retains unknown response state when it cannot establish complete post-settlement coverage. Source bodies are never published. Reopening, unlocking, clearing an answer and posting replies are separate authorized actions.

The exact Heart YELLOW reasons were acknowledged before PR creation: generated shared-standards drift (2 mismatches) and stale release validation for PyAutoNerves/PyAutoFit/PyAutoArray/PyAutoGalaxy/PyAutoLens. This was development-only authorization, not a release. No library release obligations exist for this organ-only change.

Task worktrees contain only source plus disposable test caches, synthetic browser output, logs and the temporary browser environment; no irreplaceable science data. Close-out releases the claim and removes the task worktree.

## Original prompt

# Detect actionable follow-ups on settled community threads

Issue: https://github.com/PyAutoLabs/PyAutoEars/issues/19
Issued: 2026-10-07
Type: bug
Priority: high
Difficulty: medium
Consequence: judge

## Original request

The following issue was not actioned by PyAutoEars because the user posted comments wihtout reopening the issue, I told them to reopen from now on but can PyAutoEars have a check for this behaviour so we dont miss stuff going forward (e.g. has the user asked for something actionable which should reopen the issue?). https://github.com/orgs/PyAutoLabs/discussions/13#discussioncomment-18676930

## Scope and evidence

Targets: @PyAutoEars and @PyAutoBrain. Organ/workspace development; no scientific library changes.

The example is a closed, answered Discussion with subsequent external comments. Ears `ears/collect.py:conversation` unconditionally clears awaiting_response for answered/closed Discussions. `collect` requests only open issues and skips closed entries. Brain's direct Discussion triage also suppresses awaiting_response for answered threads. Existing settlement policy deliberately specified this behavior; update producer, consumer and documentation together.

## High-level plan (approved 2026-10-07)

1. Detect external follow-up activity after a thread was answered/closed, including nested Discussion replies and closed issue comments.
2. Surface those threads as needing follow-up review, with source links and accurate closed/answered labels.
3. Have Community inspect the actual new comments and distinguish acknowledgements, actionable requests, and ambiguous cases; recommend reopening or a linked new task when appropriate.
4. Preserve read-only collection, unknown/partial coverage and separate delivery tracking. Verify with offline regression fixtures based on Discussion #13 and false-positive cases.

Tier: judge — merge mode: human /prm.

## Detailed implementation plan

- Ears `ears/collect.py`: preserve settlement timestamps and activity ordering transiently; derive post-settlement external activity independently of the existing settled response state. Add a backward-compatible optional follow-up observation with candidate comment URL/time, nullable review-needed state and coverage. A pre-settlement comment must not become a new follow-up merely because a thread is closed. Later maintainer handling clears the observed response obligation; new external activity restores it. Incomplete settlement/activity evidence stays unknown.
- Collect closed issues using bounded, updated-first pagination (without importing closed PR history); inspect external comments even on maintainer-authored issues. Retain public-source and bot filters. Report limits/failures explicitly in coverage receipts rather than implying that every historical thread was checked.
- Ears `ears/presentation.py`, `ears/board.py` and `REFERENCE.md`: add follow-up attention and a portable Community review prompt; keep closed/answered status and delivery progress distinct. Ears records activity evidence, not semantic actionability or task state.
- Brain `agents/conductors/community/_ears_feed.py`, `_community.py` and `AGENTS.md`: accept older snapshots, validate the optional observation, include follow-up candidates in Community review, keep open counts accurate, and align direct triage with snapshot triage. Review the new comment in context; explain actionable vs acknowledgement vs uncertain; recommend reopening the existing thread or linking a separate task. No automatic reopening, posting, or clearing accepted answers.
- Tests: Ears collector/listening/presentation and Brain community adapter/triage. Cover answered and closed Discussions, nested replies, closed external/maintainer-authored issues, pre-settlement activity, thank-you-only review disposition, bot activity, later maintainer response, renewed follow-up, missing timestamps, truncated pagination, stale snapshots, and legacy snapshots. Run Ears suite and Brain targeted suites; validate generated state with Brain `board/_state.py`.
- Ship compatible Brain reader support before the Ears producer extension, using linked scoped PRs if required by repository workflow. No unrelated source changes or automatic GitHub conversation mutations.

## Planning state

Plan approved by the user on 2026-10-07: "work that in and continue". Proposed branch: `feature/closed-thread-followups`.
Heart entry verdict: STALE (release stale; monitoring red), planning permitted under start_dev step 0a. Full observed reasons saved locally in `heart-ears-check.log` at workspace root.

## Permission refinement (approved)

Original follow-up: Actually not sure I have permission   maybe other people cant reopen it too?   work that in and continue

Detection must not depend on the commenter being able to reopen. GitHub viewerCanReopen confirms Jammy2211 can reopen Discussion #13; this says nothing about another commenter. Community must check the acting account capability when proposing a reopen, route to a maintainer if unavailable or unknown, and never tell contributors they must reopen for their request to count. Keep reopening, unlocking and clearing an accepted answer distinct; no automatic mutations. Add permission-aware prompt and triage tests.

## Implementation and validation — 2026-10-07

Implemented in `.worktrees/closed-thread-followups/{PyAutoEars,PyAutoBrain}` on
`feature/closed-thread-followups`; staged, not yet pushed. The optional
`follow_up` evidence links the oldest pending post-settlement comment. Closed
issue scans are updated-first and skip quiet history; incomplete history is
explicitly partial. Community accepts legacy snapshots and checks acting-viewer
reopen permission. Direct bounded triage remains unknown when it cannot prove
complete post-settlement coverage; the session must read full relevant comments.

Validation: 97 Ears tests, 66 Brain tests; generated state schema valid; Chromium
at 390/1280 widths in light/dark, clipboard success/failure, comment link and
permission-aware text all pass. A read-only live check detects Discussion #13
as closed/answered with pending follow-up and complete coverage.

Review artifacts in the worktree root: `ears.patch`, `brain.patch`, `ears-pr.md`,
`brain-pr.md`, `review-board/`, test logs. Merge Brain reader before Ears producer.

Shipping waits for explicit acknowledgement under ship_workspace step 3:
- manifest drift: shared-standards blocks (generated) — 2 mismatch(es) vs PyAutoMind/repos.yaml
- release validation stale: source moved since rehearsal (PyAutoNerves, PyAutoFit, PyAutoArray, PyAutoGalaxy, PyAutoLens)

PR creation only after acknowledgement; merge remains human /prm.

## PRs opened — 2026-10-07

The user explicitly answered "Acknowledge and open PRs" to both exact Heart
YELLOW reasons recorded above. Permission covers pushing and opening PRs, not
merging or release. No conversation was reopened or replied to.

- Brain: https://github.com/PyAutoLabs/PyAutoBrain/pull/489 (`c0bcca2`).
- Ears: https://github.com/PyAutoLabs/PyAutoEars/pull/20 (`7d7b8bd`).
- Both carry `pending-release`; source worktrees are clean.
- Local evidence: 97 Ears + 66 Brain tests, schema validation, Chromium smoke,
  and the live read-only Discussion #13 check all pass. CI running at handoff.
- Next: human /prm after CI; merge Brain #489 before Ears #20, then close task.
