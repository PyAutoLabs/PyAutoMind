Programme **M2.3** plus the Brain callers for M2.1 and M2.4 (epic `autonomous-orchestrators`, phase 9). Shipped as PyAutoMind#564 (a61d6fb87) and PyAutoBrain#620 (dd84a8079), merged 2026-11-13. Issue PyAutoBrain#614.

**M2.3:**
- An absent Lane fails closed in unattended plans and watcher ticks.
- Intake refuses a draft with no Lane.
- queue.md is a validated ranked list: dead refs fail `lifecycle.py check`, `close` retires completed entries, and an empty list stops unattended backlog dips.
- Priority sorts before review-minutes.
- A `read_queue` bug is fixed: the Retired footer had overwritten the live entry.
- AUTONOMY.md gains "M2 rulings — 2026-11-12", recording all six M1-gate rulings with dates and revert conditions.
- **The first ranked queue.md** (12 entries) was written right after the merge, human-approved at the M2 gate.

**Callers:**
- Every dev-ship Heart gate uses the scoped `--dev --repos` verdict, including the watcher close-out.
- An empty scope, or a reply without the dev-ship gate, parks.
- With no Heart CLI, only a published GREEN under 6 h old passes.
- `heart_feed.py` treats a feed over 6 h old as never GREEN.
- `nightly.sh` takes `commit_shas` from `rehearsal.json`, and the same file feeds Stage 3 and Heart validate.
- The live dispatch carries `rehearsal_run_id`.
- The manual door forwards and cross-checks the run id.

**Witness:** Brain suite 1794 passed. Mind suite 781 passed. CI green.

**Review:** several rounds of FINDINGS, all fixed, then CLEAN:
- intake deviated from the ruling;
- queue retirement and the drift check;
- an empty scope fell back to the unscoped verdict;
- the web-session fallback;
- a run-id cross-check;
- the unscoped close-out.

**Heart:** RED at ship. The human gave an override plus the merge command at the M2 gate.
