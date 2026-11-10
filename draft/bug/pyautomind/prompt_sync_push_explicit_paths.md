# prompt_sync_push: commit only the paths it is given

Type: bug
Target: PyAutoMind
Repos:
- PyAutoMind
- PyAutoBrain
Difficulty: small
Autonomy: supervised
Priority: high
Status: draft
Filed: 2026-11-10
Consequence: glance
Witness: `grep -n "add -A" scripts/prompt_sync.sh` returns nothing; a test with a dirty file outside the given paths shows the helper refuses and commits nothing; a test with conflict markers in a staged file, and one with an unparseable `state.json`, both refuse; the skill files that call the helper pass explicit paths
Review-minutes: 5
Unattended: never
Lane: any

Source: the ecosystem review of 2026-11-10, findings FB-1 and MIND-1, both confirmed by an independent verifier. Report: https://claude.ai/artifact/4A94P1cevvkESoM22QoMWm (private) and `Science/scratch/ecosystem_review_2026-11/REPORT.md`, sections B3 and B6 and Appendix A.

**What was measured.** Twelve feedback memories from 2026-05-10 to 2026-11-05 record write hazards in the shared Mind checkout. About six of them are a commit that swept up files the session did not own, and four of those came after the commit guard of 2026-07-16, three through `prompt_sync_push`. The helper still runs `git add -A` at `scripts/prompt_sync.sh:104`, then commits and pushes with no pull, rebase, retry or lock. `PyAutoBrain/bin/mind_commit_guard.py` has no reference to the helper and cannot see a helper call. Ten checked-in skill files still tell sessions to call it; only `prm/reference.md` warns about the `add -A`.

Recorded damage with one human and a few sessions: conflict markers committed twice, live `active.md` entries dropped and restored by hand, other sessions' edits swept into commits, and six completion records stranded on unmerged branches.

**The change.**
1. `prompt_sync_push` takes explicit file paths and stages only those.
2. It refuses when the tree has changes outside those paths, when any staged file contains conflict markers, or when `state.json` does not parse.
3. Update the skill files that call it to pass their paths.

For autonomous shifts the one-Mind-writer rule is already enforced by a hook since 2026-11-03 (PyAutoBrain#560), so this fix is for every other session. The remote transport a cloud writer needs is a separate question and belongs in the cloud watcher design.

`Unattended: never` because this is the helper every session uses to write Mind; ship it with the human present.

<!-- filed 2026-11-10 by the ecosystem review (draft/research/pyautobrain/ecosystem_review_for_autonomous_runs.md); headers mirror intake's -->
