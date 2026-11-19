# Shift: two workers on one library when their files are disjoint

Type: feature
Target: PyAutoBrain
Repos:
- PyAutoBrain
Difficulty: medium
Autonomy: supervised
Priority: low
Status: draft
Filed: 2026-11-19
Epic: autonomous-orchestrators
Phase: 10
Consequence: judge
Blocked-by: decide after M3.7a to M3.7e have run in a shift (epic "M3.7 Shift speed", "Later, not filed")
Lane: any
Unattended: never

## Request (verbatim)

Human, 2026-11-19, in chat: "do all the still open". The epic's M3.7 section: "Two workers on one library on disjoint files; decide after M3.7 has run in a shift."

## Why

A shift holds a library for starting while a worker on it is live (M3.6j), so a second task on the same library waits even when the two would touch different files. With M3.7's faster close-outs (S5, S6) the library hold is now the main serial step in a library-heavy shift.

## Questions for the human before planning

- How to predict a task's files before it starts (the prompt's named paths, a sizing estimate, or none: start, then park on overlap).
- Whether S6's overlap rule (branch update only on shared files) is enough protection at merge, or a second worker needs its own guard.
- The evidence to look at first: how often a shift's picks queued behind a library hold in the first shifts after M3.7.
