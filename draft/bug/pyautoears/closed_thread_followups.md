# Detect actionable follow-ups on settled community threads

Type: bug
Priority: high
Difficulty: medium
Consequence: judge

## Original request

The following issue was not actioned by PyAutoEars because the user posted comments wihtout reopening the issue, I told them to reopen from now on but can PyAutoEars have a check for this behaviour so we dont miss stuff going forward (e.g. has the user asked for something actionable which should reopen the issue?). https://github.com/orgs/PyAutoLabs/discussions/13#discussioncomment-18676930

## Scope and evidence

Targets: @PyAutoEars and @PyAutoBrain. Organ/workspace development; no scientific library changes.

The example is a closed, answered Discussion with subsequent external comments. Ears `ears/collect.py:conversation` unconditionally clears awaiting_response for answered/closed Discussions. `collect` requests only open issues and skips closed entries. Brain's direct Discussion triage also suppresses awaiting_response for answered threads. Existing settlement policy deliberately specified this behavior; update producer, consumer and documentation together.

## High-level plan (pending approval)

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

Plan approval pending; no source edits or worktree created. Proposed branch: `feature/closed-thread-followups`.
Heart entry verdict: STALE (release stale; monitoring red), planning permitted under start_dev step 0a. Full observed reasons saved locally in `heart-ears-check.log` at workspace root.
