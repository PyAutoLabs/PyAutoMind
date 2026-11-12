Programme task **M1.2** (epic `autonomous-orchestrators`, phase 8). Shipped as PyAutoMind#555 (7ae138d5f) and PyAutoBrain#605 (3dfe3707d), both merged 2026-11-12. Issue PyAutoMind#554, closed.

`prompt_sync_push <message> <path>...` now stages and commits only the given paths, with a pathspec-limited commit. It refuses, committing nothing, when:
- no paths are given;
- there are changes outside the paths (including untracked files, unmerged paths and rename sources);
- a staged file has both `<<<<<<< ` and `>>>>>>> ` lines;
- a changed `state.json` does not parse;
- a path lies outside the repo.

Other changes:
- `prompt_sync_new_prompts` commits only the new prompts.
- `lifecycle.py close` prints the exact push line for what it wrote, plus the dashboard files, instead of `git add -A` advice.
- Every caller in Mind and Brain passes the files its step writes. This includes `state.json` and `autonomy_log.md`, and the registries the close dry run names.

**Witness** (command and observed result):
- `grep -n "add -A" scripts/prompt_sync.sh` prints nothing.
- `pytest tests/test_prompt_sync_explicit_paths.py tests/test_prompt_sync_branch.py` gives 20 passed, later 21 with the bystander test. 9 of the new tests fail on the old script.
- Mind `pytest tests/`: 750 passed.
- CI green: Mind Lifecycle Drift and Spawn Drift (privacy; the conditional `drift` job was skipped), Brain pytest 3.12 and 3.13.
- This close-out was itself committed with the line `close` printed, through the new helper.

**Review:** an independent Opus review returned FINDINGS. The documented intake and prm calls left out `state.json`, `autonomy_log.md` and the registries, so they would have refused, and close still printed `git add -A` advice. These were fixed in b5e742128 and cf0339e, which also fixed 3 more call-site gaps the audit found. The re-review was CLEAN, with a scratch-clone glance close-out that committed cleanly.

**Heart:** RED at ship (PyAutoLens canonical checkout on a review branch and dirty; install check F; release integrate). The live human gave a development-only override plus the merge command, recorded in all four places.

**Follow-ups:** `draft/maintenance/pyautomind/prompt_sync_explicit_paths_followups.md` (the autolens_profiling caller, documenting the shared-checkout route, the `PYAUTO_MIND` test fixture, literal pathspecs).

There is no pending release: these are organs, not published libraries.

## Original prompt

# prompt_sync_push: commit only the paths it is given

Type: bug
Target: PyAutoMind
Repos:
- PyAutoMind
- PyAutoBrain
Difficulty: small
Autonomy: supervised
Priority: high
Status: issued
Filed: 2026-11-10
Issued: 2026-11-12
Epic: autonomous-orchestrators
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
