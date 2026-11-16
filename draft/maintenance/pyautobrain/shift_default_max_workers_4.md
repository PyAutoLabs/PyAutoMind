# Shift briefs: default max-workers 4

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

The human asked (cockpit, 2026-11-16) for shifts to run 4 concurrent workers by default, not 2.

1. `agents/conductors/batch/_brief.py:26`: `CAP_DEFAULTS["max-workers"]` 2 → 4. Consider `max-sessions` 6 → 8 so a 4-worker shift keeps room for re-dispatches (the 2026-11-16-pm brief was raised to 4 workers / 8 sessions / 5M tokens live).
2. Docs that say "default 2": Brain `agents/conductors/batch/AGENTS.md` (~263) and the brief template in Mind `batches/AGENTS.md` (~202, ~268). The template's example line is copied into briefs verbatim, so change it to `max-workers: 4` too; otherwise the code default never applies.
3. Update tests under `tests/` that assume the default of 2 (grep `max-workers`).
4. Check the `/batch` composer and any planner text that states a worker count.
