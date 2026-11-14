# Shift chat cockpit: watch and steer a live shift from a Claude chat

Type: feature
Target: PyAutoBrain
Repos:
- PyAutoBrain
- PyAutoMind
Difficulty: medium
Autonomy: supervised
Consequence: judge
Priority: high
Status: draft
Filed: 2026-11-14
Epic: autonomous-orchestrators (programme M3.4)
Lane: any

## Why

Human, 2026-11-14, after the warm-up shift: the orchestrator should be "more live fed" to them.
A GitHub status comment and phone @mentions are "only one layer and less like a claude chat I'd
watch". The work so far built the engine: the deterministic watcher, which stays the engine
because a shift must survive a chat closing, compaction, usage windows and the laptop, and
because unattended-merge gates must be code, not prompt. The human-facing layer has lagged.
This task builds that layer on top of the engine, and never in place of it.

## What

1. **Event stream (engine side).** The watcher appends one line per key event to a per-shift
   event log: spawned, PR opened, CI red/green, merged, refused (reason class), worker crashed,
   re-dispatched, question for the human, budget or cap reached, steering acknowledged, shift
   ended. `pyauto-brain batch watch --stream <slot>` prints new lines and exits at shift end.
   Optionally the watcher also posts each key event as a short new comment on the shift issue,
   capped per shift, so the phone gets pushes with every chat closed. The human chooses the cap
   and noise level after the M3.1 shifts.
2. **Cockpit chat (view side).** In a Claude chat the human says "watch the shift". The session
   attaches to the stream (Claude Code `Monitor`) and posts one plain line per event. It sends a
   phone push only when something needs the human. It answers "why did X fail / what's running"
   from the stream, the status comment and the PRs.
3. **Steering in plain words.** The chat turns requests ("pause", "drop the PyAutoLens one",
   "kill that worker and retry", "merge #347") into the commands the watcher already obeys
   (`/pause`, `/resume`, `/drop`, `/stop`, `claude stop`, a human-commanded merge). New watcher
   verbs, each a small offline-tested change: `/add <prompt>` (named task joins the live
   shift, through the same premise/Lane/claim gates) and `/cap merges|workers|tokens <n>`
   (lower or raise within the brief's ceiling).
4. **Doctrine carve-out (human's word required).** `end_at_deliverable.md` and the PreToolUse
   hook allow a watch the human asks for, bounded by that shift's review-at plus the late-sweep
   window, with no re-arming after it ends. Everything else stays banned.

## Properties to keep

- The chat is never in the control loop: closing it changes nothing about the shift, and a new
  chat can attach mid-shift.
- Every steering act still lands as a comment from `mention_login` on the shift issue (one
  audit trail, whether typed on GitHub or said in chat).
- Token cost per event is small (cached context; plain lines); measure it on the first watched
  shift.

## Witness

- Offline: the stream prints the events of a replayed shift (2026-11-14-pm plus the M3.1
  dry-run harness) in order and exits at shift end; each new verb has a test that fails on the
  old code.
- Live: one watched shift where the human steers at least twice from the chat, and the digest
  shows both acts with the human's login.

## Order

After M3.1 (2026-11-14 evening shifts), before M5 scaling: at 5–20 workers a human cannot
follow a shift through one GitHub comment.
