# Launch a shift from the phone: the idle watcher never sees a brief pushed from elsewhere

Type: feature
Target: PyAutoBrain
Repos:
- PyAutoBrain
Difficulty: medium
Autonomy: supervised
Priority: medium
Status: draft
Filed: 2026-11-17
Epic: autonomous-orchestrators
Consequence: judge
Lane: local-dev
Unattended: never

Source: the human, 2026-11-17 (chat, M3.6 sitting). Filed, not built; not part of M3.6b.

## Why

Launching a shift from the phone does not work yet. A brief pushed to Mind `main` from a
phone (or any machine other than the laptop) is never picked up by the laptop watcher:

1. **Discovery reads a ref the idle watcher never moves.** `find_briefs` →
   `shift_briefs(mind, ref="origin/main")` (`agents/conductors/batch/_orchestrator.py`)
   lists `batches/` with local `git ls-tree` / `git show` only — "never a fetch: only a
   pushed brief opens". That holds on the laptop, where the push itself moves the local
   `origin/main`; a push from elsewhere does not.
2. **The one fetch happens too late.** `_fetch_once` runs once per shift, before its first
   plan (it is called from inside `tick`, via the questions inbox and `origin_claims`). An
   idle watcher has no shift, so it never fetches, so it never finds the brief that would
   start one.
3. **The tick reads the brief from the working tree.** `find_briefs` ticks a brief "from
   Mind's working tree; one pushed but missing there is named, not ticked", and `tick`
   parses `brief_path.read_text()`. The watcher never pulls the shared checkout, so even
   after a fetch the brief is not on disk.

## Overlap

This overlaps **M4.3** (one network write path to Mind `main`, MIND-1): both are about the
watcher reading the shared Mind checkout instead of one owned read/write path to `main`
(the epic's "For the infrastructure review" list names it too). Decide whether this is a
slice of M4.3 or a small fix before it (for example, an idle-watcher fetch on a bounded
cadence that respects AUTONOMY.md "The watcher's network surface", and ticking the brief
from `origin/main` content rather than the working tree) before building.

## Witness (to settle at planning)

A test where the brief exists only on a remote's `main` (pushed from a second clone) and an
idle watcher, with no shift running, finds and ticks it within one bounded fetch interval,
without pulling or dirtying the shared checkout.
