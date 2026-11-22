# The same manifest-drift reason is acknowledged by hand on every shift brief

Type: bug
Target: PyAutoHeart
Repos:
- PyAutoHeart
- PyAutoMind
Difficulty: small
Autonomy: supervised
Priority: medium
Status: draft
Consequence: judge
Review-minutes: 10
Unattended: never
Lane: local-dev

## Finding

Three shift briefs in a row carry the same `heart-ack:` line, each typed by the human at launch
(`batches/2026-11-19-pm.md`, `batches/2026-11-19-pm2.md`, `batches/2026-11-20-am.md`):

    manifest drift: end-at-deliverable blocks (generated) — 46 mismatch(es) vs PyAutoMind/repos.yaml
    manifest drift: generated hooks (session-start + end-at-deliverable) — 2 mismatch(es) vs PyAutoMind/repos.yaml

Both are local-checkout reasons under rule `manifest`, which the record itself calls "report only"
("the leg reads checkouts on disk, other sessions' worktrees included"). The counts have not moved
across the three shifts, so the acknowledgement no longer tells the human anything: it is the same
sentence accepted each time, and a new reason arriving beside it would be easy to wave through.

## Ask

reproduce before fixing: on the laptop, `python3 PyAutoMind/scripts/repos_sync.py --check` reports the two drift legs with 46 and 2 mismatches, and `pyauto-heart readiness` shows them as YELLOW local-checkout reasons.

Two parts. The first is mechanical; the second needs the human's ruling and is why this is
`Unattended: never`.

1. Find what the 46 + 2 mismatches are. If they are generated blocks that are stale in checkouts
   or in other sessions' worktrees, regenerate them so the leg reads clean, and say in the PR
   which checkouts were stale and why they went stale.
2. Ask the human whether a `report only` local-checkout reason should need a per-brief
   acknowledgement at all. Options to put to them: (a) keep the ack as it is once part 1 has
   cleared the drift; (b) a report-only reason is shown in the brief's Heart block but needs no
   ack; (c) an ack of an identical reason list carries over to the next brief until the list
   changes. Do not implement (b) or (c) without their answer: the YELLOW acknowledgement is bound
   to the exact reason list at launch (PyAutoBrain `AUTONOMY.md`, autonomous-ship gate leg 4).

## Provenance

[from: orchestrator review 2026-11-22 of shifts 2026-11-19-pm, 2026-11-19-pm2 and 2026-11-20-am]
