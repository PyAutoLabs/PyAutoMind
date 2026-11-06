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
| 2026-11-06-pm | live | 30 | ? | 0 | 0 | 0 | ? | 0 | 0 | 233215 | 0 |
