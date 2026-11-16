# Shift briefs: default max-workers 4 and token-budget 5M

Type: maintenance
Target: PyAutoBrain
Repos:
- PyAutoBrain
- PyAutoMind
Difficulty: small
Autonomy: supervised
Priority: medium
Status: draft
Filed: 2026-11-16
Epic: autonomous-orchestrators
Consequence: glance
Lane: any

Start after shift 2026-11-16-pm ends (it runs on this Brain checkout).

The human asked (cockpit, 2026-11-16) for shifts to run 4 concurrent workers by default, not 2, and to get a 5,000,000 token budget by default, not 2,000,000.

1. `agents/conductors/batch/_brief.py:26`: `CAP_DEFAULTS["max-workers"]` 2 → 4. Consider `max-sessions` 6 → 8 so a 4-worker shift keeps room for re-dispatches (the 2026-11-16-pm brief was raised to 4 workers / 8 sessions / 5M tokens live).
2. Docs that say "default 2": Brain `agents/conductors/batch/AGENTS.md` (~263) and the brief template in Mind `batches/AGENTS.md` (~202, ~268). The template's example line is copied into briefs verbatim, so change it to `max-workers: 4` too; otherwise the code default never applies.
3. Update tests under `tests/` that assume the default of 2 (grep `max-workers`).
4. Token budget: `agents/conductors/batch/_batch.py` ~3276, `NEW_BRIEF_DEFAULTS["token-budget"]` "2000000" -> "5000000" (what `brief --new` writes). Update tests and docs that assume 2000000, and check the earlier-shift budget comparison in `_orchestrator.py` (~757-785) still reads sensibly.
5. `brief --new` writes no `max-workers:` line today, so the `CAP_DEFAULTS` change in item 1 is what new briefs get; check the `/batch` skill and planner text for any stated worker count or budget.
