# prompt_sync_push: an explicit push target from a detached HEAD

Type: bug
Target: PyAutoMind
Repos:
- PyAutoMind
Difficulty: small
Autonomy: supervised
Priority: high
Status: issued
Filed: 2026-11-12
Issued: 2026-11-12
Epic: autonomous-orchestrators
Consequence: glance
Witness: from a detached HEAD on origin/main, `PROMPT_SYNC_PUSH_TO=main prompt_sync_push "<msg>" <path>` commits the path and fast-forwards the remote's main (test with a bare remote); without the variable it still refuses (existing `test_detached_head_is_refused` passes) and the refusal names the variable; a non-fast-forward push is refused and never forced; a named-branch checkout ignores nothing and pushes its own branch as before
Review-minutes: 5
Unattended: never
Lane: any

Source: observed 2026-11-12 in the programme M1.2 close-out, carved from item 2 of `draft/maintenance/pyautomind/prompt_sync_explicit_paths_followups.md`; human asked for the fix ("fix the detached-HEAD push in prompt_sync").

Doctrine says Mind writes go through a temporary worktree detached on `origin/main`, never the shared checkout. Since 7354a32d7 the helper pushes the current branch and refuses a detached HEAD, so on that route it commits and then cannot push. The refusal guards a real hazard (a branch-scoped session pushing to `main` by accident), so it stays the default.

Change: `_prompt_sync_push_current` (used by `prompt_sync_push` and `prompt_sync_new_prompts`) accepts an explicit, per-call target `PROMPT_SYNC_PUSH_TO=<branch>`. On a detached HEAD with the variable set it runs `git push origin HEAD:<branch>` (no `-u`, no force); a rejection is reported and returns nonzero. Without it, the refusal names the variable. On a named branch the variable is not needed. Decide (and test) whether a named branch with the variable set and different from the current branch refuses (recommended: refuse, to keep one rule per call). Document the route in REFERENCE.md beside the helper, and in the follow-up draft mark item 2's detached-HEAD half done.
