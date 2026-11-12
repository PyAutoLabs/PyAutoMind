# Heart unit-test trends: follow-ups from PyAutoHeart#338

Type: feature
Target: PyAutoHeart
Repos:
- PyAutoHeart
Difficulty: small
Autonomy: supervised
Priority: low
Status: draft
Filed: 2026-11-12
Epic: autonomous-orchestrators
Consequence: glance
Witness: a golden-HTML test pins the gate chart; a sub-second import series fills the chart height; the epoch filter and the plotted x agree
Review-minutes: 5
Unattended: ready
Lane: any

Source: independent review of PyAutoHeart#339 (2026-11-12).

1. `heart/timing_display.py:162`: `max(high-low, 1)` flattens sub-second series (PyAutoNerves import charts use 10–14% of the height).
2. `heart/timings.py:931` vs `:934`: the epoch filter reads `date` but the point is plotted on `at`.
3. `timing_display.py:224`: the label's date range counts None points, the axis does not.
4. "Last run of the day wins" picks between noisy runs (PyAutoArray 10-26: 100 s and 296 s); consider a median and a cache-state filter.
5. Pin "gate charts unchanged" with a golden-HTML test.
6. After the next daily heart-health run, confirm the charts on the live board.

<!-- filed 2026-11-12 by the programme lead session -->
