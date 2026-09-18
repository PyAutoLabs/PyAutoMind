# Heart smoke runner deletes the tracked output/.gitignore when wiping output/

Type: bug
Target: PyAutoHeart
Repos:
- PyAutoHeart
- autolens_workspace_test
Difficulty: small
Autonomy: safe
Priority: medium
Status: formalised
Consequence: glance
Witness: after the fix, running the smoke wipe against a workspace whose output/ holds a tracked .gitignore leaves `git status --short` empty; before the fix it shows ` D output/.gitignore`.
Review-minutes: 3
Unattended: ready

Observed 2026-09-16 during the config-priors-drift ship (PyAutoGalaxy#618): `pyauto-heart smoke autolens autogalaxy howtolens autolens_test --root ~/Code/PyAutoLabs-wt/<task>` ran green (136/136) but left `autolens_workspace_test` with ` D output/.gitignore` — the pre-run `output/*` wipe removed a TRACKED file (the `.gitignore` sentinel that keeps the empty `output/` folder in git). A ship step that does `git add -A` after smoke would commit that deletion into the workspace PR. The ship subagent restored it by hand with `git checkout -- output/.gitignore` before opening the PR.

Fix: the wipe in PyAutoHeart's smoke command (the step documented as "wipes stale output/* immediately before execution") must skip tracked paths — e.g. `git ls-files output/` to exclude, or delete only untracked/ignored entries (`git clean -fdX -- output` semantics) — and a regression test that a tracked file under output/ survives a wipe. Check the same for `test-results/`.

Witness: after the fix, running the smoke wipe against a workspace whose output/ holds a tracked .gitignore leaves `git status --short` empty; before the fix it shows ` D output/.gitignore`.

<!-- formalised by the Intake (Conception) Agent on 2026-09-16 from user-intake -->
