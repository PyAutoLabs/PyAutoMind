Shift task from the warm-up live shift `2026-11-14-pm` (PyAutoMind#569). Shipped as PyAutoHeart#347 (3260cde95), merged 2026-11-14 in-turn by the programme lead on `ci-verdict` GREEN. Issue PyAutoHeart#346.

**Built (shift worker):** the unit-test trend follow-ups from PyAutoHeart#338: chart fixes in `heart/timing_display.py` and `heart/timings.py` (per-day medians over cache-hit runs, missing values drawn as gaps), plus a golden-HTML pin.

**Close-out:** the watcher refused the unattended merge because CI was red: the tenant firewall caught a literal repo name in a `unit_history` docstring (`heart/timings.py:921`). The lead reworded that one line (cf94aca). Heart suite 1459 passed, firewall OK, CI 2/2 GREEN, dev-ship GREEN. Recorded as merged-after-substantive-change because the worker's PR was not mergeable as shipped.

**Follow-up:** workers now run the firewall before an organ push (PyAutoBrain#634).

## Original prompt

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
Verified: 2026-11-14 052c239f (PyAutoHeart)
Lane: any

Source: independent review of PyAutoHeart#339 (2026-11-12).

1. `heart/timing_display.py:162`: `max(high-low, 1)` flattens sub-second series (PyAutoNerves import charts use 10–14% of the height).
2. `heart/timings.py:931` vs `:934`: the epoch filter reads `date` but the point is plotted on `at`.
3. `timing_display.py:224`: the label's date range counts None points, the axis does not.
4. "Last run of the day wins" picks between noisy runs (PyAutoArray 10-26: 100 s and 296 s); consider a median and a cache-state filter.
5. Pin "gate charts unchanged" with a golden-HTML test.
6. After the next daily heart-health run, confirm the charts on the live board.

<!-- filed 2026-11-12 by the programme lead session -->
