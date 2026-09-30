# Heart clarity PR C: readable import, unit-test and CI timings

Type: feature
Target: PyAutoHeart
Difficulty: medium
Autonomy: human-required
Status: blocked
Blocked-by: heart_dashboard_clarity_p2
Priority: medium

@PyAutoHeart. Parent intent, findings, design and the Fable review with its numbered amendments: `heart_dashboard_clarity.md` in this directory. Human approved the amended plan on 2026-09-30; await PR B delivery.

Scope (parent detailed step 3, applicable step 5 validation):

- Import timing: package, bold current seconds, labelled baseline/change, source and coverage; preserve unavailable/failed imports and baseline-building states. Fix the false green at `heart/dashboard.py:774-781` (OK “0 imports within baseline” while 4 packages have no baseline and 1 is unavailable) with a regression test (amendment 6).
- Unit timing: suite wall-clock, Python leg, counts, top three bottlenecks by default, rest under disclosure; never sum parallel legs; separate absolute slowness from measured regression.
- CI: median, max, run count and window first; accessible labelled inline SVG with text fallback; keep `performance.gates[].spark` intact for the Brain; never present missing samples as zero.
- Fixtures: the local snapshot has empty timing slices, so validate against the published `board.json`, a `heart-health` artifact or fixtures (amendment 10).

Preserve verdict/score, the `performance` block's own schema and the Brain/hygiene reads of `performance`. Dispatch `heart-health.yml` after merge.

Proposed branch `feature/heart-dashboard-timings`. Follow start-dev → start-library → ship-library. Implementation approved on 2026-09-30; existing dependency and shipping gates still apply.
