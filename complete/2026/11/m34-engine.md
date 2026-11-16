M3.4 build A, the cockpit engine. Shipped as PyAutoBrain#647 (c55c4f457), merged 2026-11-16 on `ci-verdict` GREEN with Heart dev-ship GREEN. Issue PyAutoBrain#644. Design: `Science/scratch/m3_4_m3_5_design/DESIGN.md`. Human decisions all as recommended.

**Built:**
- A per-shift `events.jsonl`, written inside the tick lock with no network calls, crash-safe `seq` and dedup.
- `pyauto-brain batch watch --stream`.
- The watcher verbs `/cap`, `/add` (gated, refused within 30 min of review-at, one Mind fetch) and `/kill` (`claude stop` on the shift's own lease agent; re-dispatched once unless dropped).
- Needs-you comments, at most 5 + 1 per shift, no @, counted apart from pushes.
- Digest refusal classes for #641 and decision-taken.
- AUTONOMY items 1–3, dated 2026-11-16, and `batch/AGENTS.md` listing the seven verbs.

**Witness:**
- 70+ new tests, including a replay of the real `2026-11-14-pm3/tick.log`.
- Full suite: 2138 passed.
- The real CLI streams a 20-minute synthetic shift in order and exits 0 (`build_a_stream.txt`).

**Review:** independent Opus, FINDINGS (`/cap tokens 0` didn't stop close-outs, plus 5 follow-ups). Fixed, then CLEAN.
