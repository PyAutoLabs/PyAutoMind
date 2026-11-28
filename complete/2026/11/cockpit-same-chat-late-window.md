Merged PyAutoBrain#729 (human /prm, 2026-11-27). M3.6g.

- **Same-chat handover:** the batch launch chat hands over to the `cockpit` skill in the same chat when the human asks to watch.
- **Watch end:** the cockpit's watch ends only when the event stream exits (after `shift-end`, `stopped`, STOP, or `Watch window over` at `review-at:` + 45 min), never on an event line. So a PR that opens after the digest is reported, unlike PyAutoGalaxy#720 on 2026-11-16-pm.
- **`batch collect`:** it was retired on 2026-11-22. On a brief-form record it now prints the digest, otherwise it points to `batch digest --record`. It never prints "0 members".
- **Doctrine and code:** no doctrine change. `_watch.py` is unchanged.

Tests: the collect tests fail on origin/main. Full suite 2579 passed. Independent Opus review CLEAN. CI was RED once, on the skill line budget (the cockpit was 205 of 200 lines); fixed in bb0daa8.

## Original prompt

# M3.6g Cockpit: hand over in the kick-off chat, watch to the end of the late window, `collect` on a brief shift

Type: feature
Target: PyAutoBrain
Repos:
- PyAutoBrain
Difficulty: small
Autonomy: supervised
Priority: normal
Status: draft
Filed: 2026-11-17
Issued: 2026-11-27
Epic: autonomous-orchestrators
Phase: 10
Consequence: glance
Witness: (1) `grep -n "cockpit" skills/batch/batch.md` shows step 5 handing over to the cockpit skill in the same chat when the human asks to watch; (2) `grep -n "review-at" skills/cockpit/cockpit.md` shows the watch ending at the stream's own end (`review-at:` + 45 min), not at `shift-end`; (3) a test runs `batch collect --slot 2026-11-16-pm` on the record fixture and its output contains the digest (or "the digest is the review surface") and never "0 members"
Lane: any
Unattended: ready

## Why

In shift 2026-11-16-pm:

- The kick-off chat told the human to open a fresh chat for the live feed.
- The cockpit chat stopped its watch at the digest, six minutes before PyAutoGalaxy#720
  opened (19:24:59Z). That PR is green and nobody has looked at it.
- `batch collect --slot 2026-11-16-pm` returns "0 members, delivered 0/0". A shift run from a
  brief has no `members:` block, so collect has nothing to score; the digest is the review
  surface.

**No doctrine change is needed.** `policy/shift_cockpit_watch.md` allows the watch when the
human asked for it in this session and the session is running the `cockpit` skill. It does
not require a new chat, and its window already runs to `review-at:` + 45 min.

## What

1. `skills/batch/batch.md` step 5 ("Confirm what was dispatched, and stop") gains: if the
   human asks to watch, load the cockpit skill here, in this chat.
2. `skills/cockpit/cockpit.md` keeps the watch until the stream's own end (`review-at:` +
   45 min), not the `shift-end` event, so late arrivals are reported.
3. `batch collect` on a brief-form record prints the digest, or says the digest is the review
   surface, instead of "0 members".

## Out of scope

- Any change to `policy/shift_cockpit_watch.md` or `end_at_deliverable.md`.
- The decisions block at the end of the digest (M3.3 slice 2).
