# prompt_sync_push explicit paths: follow-ups outside PyAutoMind#554

Type: maintenance
Target: PyAutoMind
Repos:
- autolens_profiling
- PyAutoBrain
Difficulty: small
Autonomy: supervised
Priority: medium
Status: draft
Filed: 2026-11-12
Epic: autonomous-orchestrators
Consequence: glance
Witness: `grep -rn "prompt_sync_push \"[^\"]*\"$" <repos>` finds no one-argument call outside `complete/`; the shared-checkout route is documented where sessions first meet the helper
Review-minutes: 5
Unattended: ready
Lane: any

Source: the worker and the independent review of PyAutoMind#554 (programme M1.2, 2026-11-12).

1. `lens/autolens_profiling/skills/profile_likelihood/reference.md:141` still calls `prompt_sync_push` with only a message. Since #554 that refuses ("no paths"). Pass the files that step writes.
2. In the shared canonical Mind checkout, another session's dirty file now makes the helper refuse (intended). Document the temporary-worktree-on-origin/main route next to the helper's first mention in the skills (WORKFLOW.md / CONTEXT.md), so a refusal points sessions at the fix rather than at `git add -A`.
3. `tests/test_grouped_organ_consumers.py::test_hygiene_map_and_heart_board_find_grouped_checkouts` (PyAutoBrain) fails whenever `PYAUTO_MIND` is exported, as it is in every task worktree's `activate.sh`. Make the fixture clear the `PYAUTO_*` variables.

<!-- filed 2026-11-12 by the programme lead session from the #554 worker report and independent review -->
