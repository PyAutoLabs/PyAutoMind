- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/661
- prs: https://github.com/PyAutoLabs/PyAutoBrain/pull/665, https://github.com/PyAutoLabs/PyAutoMind/pull/583 (merged 2026-11-17)
- epic: autonomous-orchestrators, M3.6e
- heart-red-override: shipped under the live human's development override 2026-11-17 ("Override all three", for M3.6a #659, M3.6d #660, M3.6e #661); RED reason "PyAutoMind: Tenant Firewall Gate failure on main" (generated-hook drift from PyAutoMind#575, unrelated); merged by the human's separate /prm ("looks good prm") with every check green.
- what shipped: one merge-slot count per shift (`pyauto-brain merge-slot take|release|status <pr-url> --task <task>`: file-locked, fails closed, canonical PR URL only, a slot answers only to its own task); workers take a slot before a bare `gh pr merge` and release it if the merge fails; watcher close-outs take from the same count and now admit `notify` on R3 terms (refused without a `Witness:`); the digest labels merges from slot evidence and flags a merge with no slot (counted by `/cap`); `pyauto-brain merge-mode` prints the effective level and merge mode for `start_dev`; R3 written into AUTONOMY.md "Merge authority follows Consequence". Mind: `lifecycle.py close` matches rows by slug, prompt path, then issue (`--issue`), never a row naming another prompt.
- evidence: 7 Brain + 3 Mind witness tests and the review-round tests fail on base, pass; Brain 2218 (1 env failure also on main); Mind 1046; Fable 5.2 review FINDINGS (PR-key collision let two merges share a slot; wrong-row delete; release ignored the task) → fixed → CLEAN; CI green.
- follow-up: the `notify`-without-Witness close-out refusal is template text only (the watcher does not check it); a merge made outside the close-out still frees the watcher's slot (pre-existing).

## Original prompt

# M3.6e Shift workers merge notify-tier PRs in-turn past the shift's merge-cap, and inconsistently

Type: bug
Target: PyAutoBrain
Repos:
- PyAutoBrain
- PyAutoMind
Difficulty: small
Autonomy: supervised
Priority: high
Status: active
Issued: 2026-11-17
Issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/661
Filed: 2026-11-16
Epic: autonomous-orchestrators
Phase: 10
Consequence: judge
Witness: `python -m pytest tests/test_orchestrator_*.py tests/test_closeout_merge_slots.py -q` (PyAutoBrain) and `python -m pytest tests/test_lifecycle_close.py -q` (PyAutoMind, item 4) pass (amended 2026-11-17: the original `tests/test_closeout*.py` glob matched no file) with new tests that fail on today's main: (1) in a shift with `merge-cap: 1`, a second in-turn `notify` merge is refused and left for /prm (the fake `gh` logs one merge call); (2) under `--auto` a bug prompt with `Autonomy: safe`, `Consequence: notify` and a held witness merges in-turn and the snapshot shows "1 merged of merge-cap 1"; (3) `start_dev` prints one line "effective level: <level>; merge mode: <mode>" for that prompt; (4) `lifecycle.py close` finds the `active.md` row by prompt path or issue URL when the heading does not match the slug; and `grep -n "2026-11-17" AUTONOMY.md` shows the R3 ruling
Lane: any
Unattended: never

Seen in shift 2026-11-16-pm (brief `merge-cap: 1`). Events, from `~/Code/PyAutoLabs-wt/.orchestrator/2026-11-16-pm/events.jsonl`:
- 18:33Z `dashboard_recent_lists_planned_tasks_twice` opened PyAutoBrain#654 (notify): the watcher said "Not merging: tier notify — only glance merges unattended. Left for your /prm."
- 18:44Z `dashboard_md_epic_ledger_backticks_render_literally` merged PyAutoBrain#655 in-turn (notify), and `seed_samplers_for_byte_stable_rerenders` merged autofit_visualization#8 in-turn (notify), both as the human's login at 18:41Z.
- The next snapshot read "2 merged of merge-cap 1".

1. **Cap:** a worker's in-turn tiered merge (ship_* → /prm "Tiered merge", AUTONOMY.md "Merge authority follows Consequence") does not consult the shift's merge-cap. Inside a shift, every merge (in-turn or close-out) should take a merge slot from the watcher first, and refuse when none is left, leaving the PR for /prm.
2. **Consistency:** same tier, two outcomes (#654 left for /prm, #655 and #8 merged in-turn). Decide which is the rule for notify inside a shift (the watcher's "only glance merges unattended" or the worker's in-turn merge) and make the worker contract and the watcher agree; the digest should say which path each merge took.
3. **Close-out row match (seen in the /prm close-out after the shift):** `lifecycle.py close` found no `active.md` row to drop for `validation_wall_estimates_miss_eval_count_and_sampler_floor` and `dashboard_recent_lists_planned_tasks_twice`, because the row headings did not match the task slug; the rows were removed by hand. Make the match use the prompt path or issue URL, not only the slug.
4. Tests for each.

## Added 2026-11-17 (M3.6e, from the shift 2026-11-16-pm review)

This prompt is now milestone task M3.6e of the autonomous-orchestrators epic. The #654 worker
recorded why it did not merge: "effective level supervised (header safe, bug cap supervised)
→ `--auto` ship sign-off is decide-and-flag". The #655 worker, on the same `bug · safe ·
notify` header, merged. The doctrine did not say which was right.

**Human ruling R3 (2026-11-17):** the bug work-type cap does not stop a `notify` self-merge
under `--auto`. A `notify` bug with a held witness merges, and it counts against
`merge-cap`. That settles item 2: the worker's in-turn merge is the rule, and the watcher's
"only glance merges unattended" refusal for `notify` changes to match.

5. **`start_dev` prints the effective level and merge mode** in one line before work starts,
   so a worker and a reader see the same answer.
6. **Write R3 into AUTONOMY.md** with its date, beside "Merge authority follows Consequence",
   and make the worker contract and the watcher read it the same way.

Out of scope: the unattended `glance` grant itself (the M3 gate), and any change to which
tiers merge outside a shift.
