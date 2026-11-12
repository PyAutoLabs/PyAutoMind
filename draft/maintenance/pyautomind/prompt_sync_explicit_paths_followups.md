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
2. In the shared canonical Mind checkout, another session's dirty file now makes the helper refuse (intended). Document the temporary-worktree-on-origin/main route next to the helper's first mention in the skills (WORKFLOW.md / CONTEXT.md), so a refusal points sessions at the fix rather than at `git add -A`. Observed 2026-11-12 (M1.2 close-out): in a temporary worktree detached on origin/main the helper commits correctly but refuses to push ("refusing to push from a detached HEAD"), so the documented route must create a named branch tracking origin/main (or the helper must accept an explicit push target). **Detached-HEAD half DONE (PyAutoMind#556):** the helper now takes `PROMPT_SYNC_PUSH_TO=<branch>` per call and pushes `HEAD:<branch>` (never forced) from a detached HEAD; the route is documented in REFERENCE.md beside the helper. Still open: documenting the route at the helper's first mention in the skills (WORKFLOW.md / CONTEXT.md).
3. `tests/test_grouped_organ_consumers.py::test_hygiene_map_and_heart_board_find_grouped_checkouts` (PyAutoBrain) fails whenever `PYAUTO_MIND` is exported, as it is in every task worktree's `activate.sh`. Make the fixture clear the `PYAUTO_*` variables.
4. `scripts/prompt_sync.sh` commit uses `git commit --only <paths>`, which treats pathspecs as globs and commits worktree content; a name containing `*` or `[` could pick up a sibling in the race window. Prefix `:(literal)` or pass `--literal-pathspecs`.

<!-- filed 2026-11-12 by the programme lead session from the #554 worker report and independent review -->
