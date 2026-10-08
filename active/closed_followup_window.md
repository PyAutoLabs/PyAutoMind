# Limit closed-thread follow-up attention to 30 days

@PyAutoEars
Type: feature
Issued: 2026-10-08
Issue: https://github.com/PyAutoLabs/PyAutoEars/issues/25

## Original request (verbatim)

Most of the "Needs your atention" are really old and a result of us doing the comments after closed thing. These do not need my attention they are clearly defunct. Maybe that rule needs a time limit?

## Approval (verbatim)

do it

## Approved plan

- Apply a 30-day limit only to follow-ups on closed issues or closed/answered Discussions.
- Use the latest external human comment after settlement and the last maintainer response, not issue creation or generic update time.
- Keep aged follow-ups in Community activity, labelled historical; a new external comment restores attention.
- Preserve genuinely open issues and incomplete/unknown evidence handling.
- Verify exact cutoff, old threads with fresh replies, bot/maintainer activity, legacy snapshots, Brain adapter compatibility and board rendering.

Tier: undeclared — merge mode: human /prm.

## Detailed implementation plan

1. `ears/collect.py`: apply the cutoff against the collection timestamp after complete post-settlement activity establishes an unresolved follow-up; calculate newest pending external activity, keeping existing nested follow_up fields compatible. Persist optional `historical_follow_up_at` only for aged-out observations, mirror inactive follow-up response fields, and retain these closed issue rows instead of dropping them as quiet.
2. Extend snapshot validation for the optional historical timestamp, requiring a settled thread, complete coverage, inactive follow-up and an age older than 30 days relative to generation. Unknown metadata never proves expiry.
3. `ears/presentation.py` and `ears/board.py`: show Historical follow-up and its latest external activity date instead of needs-review prose for expired rows. Keep aged items in Community activity and out of attention/feed counts. No render-time fabrication from legacy timestamps.
4. `REFERENCE.md`: document the policy, exact boundary (30 days is still recent), metadata and backward compatibility. Preserve Brain's existing strict nested follow_up contract; verify its real adapter accepts historical rows and excludes them from awaiting-response counts.
5. Extend existing follow-up tests with deterministic collection time; test old/latest pending comments, exact cutoff, later external replies, bots, maintainer response, incomplete coverage, open issues and historical board placement. Run the Ears suite, Brain adapter tests, state validation and targeted browser smoke.

## Branch survey

- PyAutoEars: canonical clean main; no active task claim.
- PyAutoMind: canonical clean main; no matching active task.
- Proposed branch: `feature/ears-followup-window`.
- Worktree: `/home/jammy/Code/PyAutoLabs/.worktrees/ears-followup-window`.
- Scope is Ears only; Brain is a read-only compatibility consumer.
