# Dev orchestrator pilot — one row per shift

The measurement ledger of the autonomous-orchestrators pilot (epic phase 4,
`draft/feature/pyautobrain/autonomous_orchestrators_epic.md` "What the pilot
measures"). It lives in a subfolder because every `batches/*.md` is read as a
batch record.

**Who writes what.** The shift watcher appends one row at the first tick after
`review-at:`, in the same commit as the record's `## Digest`. `mode` is
`shadow` for a `shadow: yes` brief (the baseline: the orchestrator proposes,
the human works as today) and `live` otherwise. The two cells marked `?` are
the **human's**, filled at check-in: `review-minutes-actual` (the minutes the
review really took — also the record's `review-minutes-actual:`) and
`overrules` (orchestrator picks or proposals the human would not have made).
Every other cell is the digest's counter of the same name.

**Shadow rows measure the human, not the orchestrator** (corrected
2026-11-04 after shift 1, PyAutoBrain#579). A shadow shift merges nothing, so
its `review-minutes-actual` is the minutes the human spent reviewing **their
own** work in the window (PRs, `/prm`, results; not the digest), and its
`merges` (also `?`) is the human's own merges in the window. That is the
baseline the live rows are measured against.

The target metric is verified merges (plus accepted drafts and packets) per
`review-minutes-actual`, against the shadow rows as the baseline.

| slot | mode | review-minutes-planned | review-minutes-actual | merges | glance-auto-merges | reverts | overrules | pushes | drafts-filed | tokens | workers-crashed |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 2026-11-05-am | shadow | 30 | 5 | 11 | 0 | 0 | 6 | 0 | 0 | 0 | 0 |
| 2026-11-05-pm | shadow | 20 | 1 | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 2026-11-06-am | live | 30 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 2026-11-06-pm | live | 30 | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 233215 | 0 |
| 2026-11-13-am | shadow | 20 | ? | ? | 0 | 0 | ? | 0 | 0 | 0 | 0 |
| 2026-11-14-pm | live | 15 | ? | 1 | 1 | 0 | ? | 0 | 0 | 568626 | 0 |
| 2026-11-14-pm2 | live | 30 | ? | 1 | 1 | 0 | ? | 2 | 0 | 778498 | 1 |
| 2026-11-14-pm3 | live | 20 | ? | 0 | 0 | 0 | ? | 2 | 0 | 498380 | 1 |
| 2026-11-16-pm | live | 45 | ? | 2 | 0 | 0 | ? | 0 | 0 | 2657915 | 0 |
| 2026-11-18-pm | live | 45 | ? | 2 | 1 | 0 | ? | 0 | 0 | 1097204 | 0 |
| 2026-11-18-pm2 | live | 45 | ? | 0 | 0 | 0 | ? | 0 | 0 | 878300 | 0 |
| 2026-11-19-pm | live | 45 | ? | 0 | 0 | 0 | ? | 0 | 0 | 1094448 | 0 |
| 2026-11-19-pm2 | live | 45 | ? | 2 | 0 | 0 | ? | 0 | 0 | 1134807 | 0 |
| 2026-11-20-am | live | 45 | ? | 1 | 0 | 0 | ? | 0 | 0 | 755794 | 0 |
| 2026-11-23-am2 | live | 5 | ? | 0 | 0 | 0 | ? | 0 | 0 | 166804 | 0 |
| 2026-11-23-am3 | live | 55 | ? | 0 | 0 | 0 | ? | 0 | 0 | 1027420 | 0 |
| 2026-11-24-am | live | 100 | ? | 1 | 0 | 0 | ? | 0 | 0 | unmeasured | 0 |
| 2026-11-26-pm | live | 45 | ? | 6 | 3 | 0 | ? | 0 | 0 | 2025671 | 0 |
