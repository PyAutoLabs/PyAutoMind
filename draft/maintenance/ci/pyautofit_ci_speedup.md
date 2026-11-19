# CI speed: PyAutoFit's 10-minute PR CI is the floor of a shift merge

Type: maintenance
Target: PyAutoFit
Repos:
- PyAutoFit
Difficulty: medium
Autonomy: supervised
Priority: medium
Status: draft
Filed: 2026-11-19
Epic: autonomous-orchestrators
Phase: 10
Consequence: judge
Lane: any
Unattended: never

## Request (verbatim)

Human, 2026-11-19, in chat: "do all the still open". The epic's M3.7 section: "PR CI is the remaining floor (PyAutoFit 10 minutes): a `/ci_speedup` task."

## Why

Since M3.7b a shift's close-out waits in-turn for PR CI and merges on green. Galaxy's PR CI takes about 4 minutes and PyAutoFit's about 10, so PyAutoFit's CI is now the longest wait between PR-open and merge.

## Shape

Run `/ci_speedup` on PyAutoFit: find the slowest parts of its PR CI (unit tests, legs, setup) on the Heart board, then plan the speed-ups through the dev flow. Never weaken a test to make it faster.
