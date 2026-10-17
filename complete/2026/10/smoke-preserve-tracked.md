# smoke-preserve-tracked

Completed: 2026-10-17
Issue: https://github.com/PyAutoLabs/PyAutoHeart/issues/302
PR: https://github.com/PyAutoLabs/PyAutoHeart/pull/306

Smoke cleanup preserves tracked output files and ancestors, does not follow symlinks, and fails closed if the git index cannot be read. Real-git regression confirms a clean working tree after wiping generated output.

## Verification and merge

User /prm authorized the merge. GitHub confirmed MERGED; git merge-base --is-ancestor proves the shipped head is in origin/main. Only PyAutoHeart has a claimed implementation branch; no sibling implementation remains. Both Python 3.12 and 3.13 jobs passed on the exact shipped head in https://github.com/PyAutoLabs/PyAutoHeart/actions/runs/39057215449, including the tenant firewall. No skipped test legs. Issue closed as completed.

Published Heart at shipping was STALE because source moved since release rehearsal; this development merge does not assert release readiness. Live weekly cloud sweep remains unverified where applicable.

## Close-out notes

Original task worktrees are absent from this session; no worktree or data was deleted.

Review-log classification remains unconfirmed: the human-action question was unanswered. The merged heads match the shipped heads; no shadow row or human confirmation is invented.

## Original prompt

# Heart smoke runner deletes the tracked output/.gitignore when wiping output/

Type: bug
Target: PyAutoHeart
Repos:
- PyAutoHeart
- autolens_workspace_test
Difficulty: small
Autonomy: safe
Priority: medium
Status: active
Issued: 2026-10-17
Consequence: glance
Witness: after the fix, running the smoke wipe against a workspace whose output/ holds a tracked .gitignore leaves `git status --short` empty; before the fix it shows ` D output/.gitignore`.
Review-minutes: 3
Unattended: ready

Observed 2026-09-16 during the config-priors-drift ship (PyAutoGalaxy#618): `pyauto-heart smoke autolens autogalaxy howtolens autolens_test --root ~/Code/PyAutoLabs-wt/<task>` ran green (136/136) but left `autolens_workspace_test` with ` D output/.gitignore` — the pre-run `output/*` wipe removed a TRACKED file (the `.gitignore` sentinel that keeps the empty `output/` folder in git). A ship step that does `git add -A` after smoke would commit that deletion into the workspace PR. The ship subagent restored it by hand with `git checkout -- output/.gitignore` before opening the PR.

Fix: the wipe in PyAutoHeart's smoke command (the step documented as "wipes stale output/* immediately before execution") must skip tracked paths — e.g. `git ls-files output/` to exclude, or delete only untracked/ignored entries (`git clean -fdX -- output` semantics) — and a regression test that a tracked file under output/ survives a wipe. Check the same for `test-results/`.

Witness: after the fix, running the smoke wipe against a workspace whose output/ holds a tracked .gitignore leaves `git status --short` empty; before the fix it shows ` D output/.gitignore`.

<!-- formalised by the Intake (Conception) Agent on 2026-09-16 from user-intake -->

## Reconciliation — 2026-10-01

Keep open — source confirms the defect. Heart origin/main `ff7003f`, `heart/smoke.py:540-548`, iterates every output child and unlinks files or recursively removes directories, with no tracked-file exemption. No destructive smoke run was performed during this audit. The reconciler's referenced tenant-firewall completion is a different defect and is not completion evidence for this task.
