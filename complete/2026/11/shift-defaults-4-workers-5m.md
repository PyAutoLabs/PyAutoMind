## shift-defaults-4-workers-5m

- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/656
- completed: 2026-11-16
- library-pr: https://github.com/PyAutoLabs/PyAutoBrain/pull/657
- merge: f2081c78c89e8a45e6a1f48be60ec04defab1742 (CI green, human /prm)
- epic: autonomous-orchestrators

Shifts now default to 4 concurrent workers and 8 sessions (was 2 / 6), and
`batch brief --new` writes `token-budget: 5000000` (was 2000000).

- Brain `_brief.py` `CAP_DEFAULTS = {"max-workers": 4, "max-sessions": 8}`;
  `_batch.py` `NEW_BRIEF_DEFAULTS["token-budget"] = "5000000"`; batch
  `AGENTS.md` watcher section updated.
- Mind `batches/AGENTS.md` brief template and caps paragraph were updated
  direct to Mind main (5e769d792), so the template no longer pins 2 workers.
- Tests that relied on the old default now state their caps in the brief;
  new witness tests cover "no caps -> 4 spawn" and "`brief --new` writes 5M".
- `worker_token_estimate` only uses earlier shifts within 2x of the budget, so
  a 5M shift skips the old 2M shifts; judged sensible, left unchanged.
- One pre-existing Brain test failure
  (`test_grouped_organ_consumers.py::test_hygiene_map_and_heart_board_find_grouped_checkouts`)
  comes from the task worktree's `activate.sh` environment and passes in a
  clean one; not caused by this change.

## Original prompt

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
Issued: 2026-11-16
Epic: autonomous-orchestrators
Consequence: glance
Witness: `batch brief --new` output carries `token-budget: 5000000`; a brief with no `max-workers:` spawns 4; Brain test suite passes
Lane: any

Start after shift 2026-11-16-pm ends (it runs on this Brain checkout).

The human asked (cockpit, 2026-11-16) for shifts to run 4 concurrent workers by default, not 2, and to get a 5,000,000 token budget by default, not 2,000,000.

1. `agents/conductors/batch/_brief.py:26`: `CAP_DEFAULTS["max-workers"]` 2 → 4. Consider `max-sessions` 6 → 8 so a 4-worker shift keeps room for re-dispatches (the 2026-11-16-pm brief was raised to 4 workers / 8 sessions / 5M tokens live).
2. Docs that say "default 2": Brain `agents/conductors/batch/AGENTS.md` (~263) and the brief template in Mind `batches/AGENTS.md` (~202, ~268). The template's example line is copied into briefs verbatim, so change it to `max-workers: 4` too; otherwise the code default never applies.
3. Update tests under `tests/` that assume the default of 2 (grep `max-workers`).
4. Token budget: `agents/conductors/batch/_batch.py` ~3276, `NEW_BRIEF_DEFAULTS["token-budget"]` "2000000" -> "5000000" (what `brief --new` writes). Update tests and docs that assume 2000000, and check the earlier-shift budget comparison in `_orchestrator.py` (~757-785) still reads sensibly.
5. `brief --new` writes no `max-workers:` line today, so the `CAP_DEFAULTS` change in item 1 is what new briefs get; check the `/batch` skill and planner text for any stated worker count or budget.
