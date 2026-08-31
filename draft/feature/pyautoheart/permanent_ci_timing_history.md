# Permanent CI timing history stored in PyAutoHeart

Type: feature
Target: PyAutoHeart
Repos:
- PyAutoHeart
Difficulty: medium
Autonomy: safe
Priority: high
Status: formalised
Consequence: judge
Review-minutes: 20
Unattended: ready
Epic: ci-timing-fast-tests
Phase: 2

Permanent CI timing history stored in PyAutoHeart (replace the 30-day self-carried window).

Today the only "history" is the performance block's rolled-forward window: the aggregate
step re-reads the previously published Pages `board.json` (`heart/checks/ci_timing.sh:64-79`)
and caps at 30 entries (`history_cap: 30`) — a publish gap loses it and nothing is ever
committed to the repo. The user's intent: run-time information on all CI tests tracked with
the nightly run and stored in PyAutoHeart as a PERMANENT record, with the dashboard showing
the most recent times but having access to all history.

Build the durable record: the daily heart-health run appends the day's observations (the
workflow-level gates from ci_timing AND the per-script rows from the phase-1 ingester) to
committed history files in the PyAutoHeart repo (e.g. under `state/` or a dedicated
`timings/` tree — append-only, compact JSON/JSONL per repo, committed by the workflow the
way `state/devbox_board.json` already is). The board keeps rendering the recent window but
links/reads from the committed record; the 30-day Pages self-carry becomes a cache, not the
source of truth. Design reference: Plane C ("durable baselines") of
`PyAutoMind/docs/pyautoheart/test_performance_board_assessment.md`.

Mind the file-growth shape: daily append across ~26 gates + a few hundred script rows must
stay reviewable (one commit/day, stable ordering, no churn of past lines).
