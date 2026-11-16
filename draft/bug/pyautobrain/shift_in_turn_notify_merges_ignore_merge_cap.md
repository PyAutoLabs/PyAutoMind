# Shift workers merge notify-tier PRs in-turn past the shift's merge-cap, and inconsistently

Type: bug
Target: PyAutoBrain
Repos:
- PyAutoBrain
Difficulty: small
Autonomy: supervised
Priority: high
Status: draft
Filed: 2026-11-16
Epic: autonomous-orchestrators
Consequence: judge
Lane: any

Seen in shift 2026-11-16-pm (brief `merge-cap: 1`). Events, from `~/Code/PyAutoLabs-wt/.orchestrator/2026-11-16-pm/events.jsonl`:
- 18:33Z `dashboard_recent_lists_planned_tasks_twice` opened PyAutoBrain#654 (notify): the watcher said "Not merging: tier notify — only glance merges unattended. Left for your /prm."
- 18:44Z `dashboard_md_epic_ledger_backticks_render_literally` merged PyAutoBrain#655 in-turn (notify), and `seed_samplers_for_byte_stable_rerenders` merged autofit_visualization#8 in-turn (notify), both as the human's login at 18:41Z.
- The next snapshot read "2 merged of merge-cap 1".

1. **Cap:** a worker's in-turn tiered merge (ship_* → /prm "Tiered merge", AUTONOMY.md "Merge authority follows Consequence") does not consult the shift's merge-cap. Inside a shift, every merge (in-turn or close-out) should take a merge slot from the watcher first, and refuse when none is left, leaving the PR for /prm.
2. **Consistency:** same tier, two outcomes (#654 left for /prm, #655 and #8 merged in-turn). Decide which is the rule for notify inside a shift (the watcher's "only glance merges unattended" or the worker's in-turn merge) and make the worker contract and the watcher agree; the digest should say which path each merge took.
3. **Close-out row match (seen in the /prm close-out after the shift):** `lifecycle.py close` found no `active.md` row to drop for `validation_wall_estimates_miss_eval_count_and_sampler_floor` and `dashboard_recent_lists_planned_tasks_twice`, because the row headings did not match the task slug; the rows were removed by hand. Make the match use the prompt path or issue URL, not only the slug.
4. Tests for each.
