# PyAutoHeart — import_time observation leg (hygiene follow-up)

Type: feature
Target: PyAutoHeart
Repos:
- PyAutoHeart
Difficulty: medium
Autonomy: supervised
Priority: low
Status: formalised

Deferred optional follow-up from the hygiene conductor epic (PyAutoBrain#88/#90/#92,
complete). The hygiene `perf` mode currently times library import cost itself in a
subprocess (a cheap on-demand pre-scan) and reads slow-test/slow-script signals
from Heart's existing `script_timing` / `test_run` legs. This task **promotes the
import-cost pre-scan to a standing, tracked PyAutoHeart signal** so import-time
*regressions* are observed over time rather than only spot-checked — closing the
"measurement lives in Heart; hygiene acts" loop for imports.

**Build a `heart/checks/import_time.py` leg**, mirroring `heart/checks/script_timing.py`:
- measure the import cost of the PyAuto libraries (top-level `autolens` pulls the
  whole stack; consider per-package `autoconf`/`autofit`/`autoarray`/`autogalaxy`/
  `autolens` if a per-lib breakdown is wanted), each in a **subprocess** with a
  timeout, so Heart's own process never imports the science/JAX stack.
- keep a **baseline** and flag a regression when import time grows beyond a
  tolerance (the `script_timing` baseline/threshold pattern), surfaced through
  `readiness.py` / `dashboard.py` like the other timing legs.

**Respect the <30s tick budget (`docs/internals.md`) — the crux.** A cold import
of the full stack can be several seconds; importing all five packages could blow
the routine tick. Options to weigh in the plan: (a) time only one representative
import (`autolens`) per tick; (b) put `import_time` on a **slower cadence / opt-in
tier** rather than every tick; (c) cache and re-measure only when the installed
version changes. Pick the one that keeps routine ticks within budget — do not
make every tick pay a multi-second import.

**Then wire the hygiene `perf` mode to consult this leg** (PyAutoBrain):
`agents/conductors/hygiene/hygiene.sh` — when the `import_time` leg is present in
Heart's state, `perf` surfaces the tracked value + regression flag (as it already
does conceptually for `script_timing`/`test_run`) rather than only its own
subprocess timing. Keep the subprocess pre-scan as the fallback when Heart has no
reading (e.g. no venv / leg absent).

**Optional sibling — a `cli_noise` leg** was mentioned in the same deferred note;
it is heavier (runs pytest + scripts) and almost certainly *cannot* fit the tick
budget, so treat it as out-of-scope here unless the plan shows a cheap signal.

**Done when:** `import_time` is a real Heart leg with a baseline + regression flag
that stays within the tick budget (or is explicitly a slower/opt-in tier), it
shows in the readiness dashboard, PyAutoHeart tests cover it, and the hygiene
`perf` mode reads it when present. This is a **standalone follow-up** — the
hygiene conductor is already complete without it.

<!-- filed 2026-07-11 from the hygiene-conductor epic close-out (complete.md
     "hygiene-agent"). Low priority; the conductor works without it. -->
