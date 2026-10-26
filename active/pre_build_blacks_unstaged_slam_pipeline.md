# pre_build runs black on slam_pipeline/ for every workspace but stages it only for autolens_workspace — leaves a dirty canonical checkout each release

Issued: 2026-10-26
Type: bug
Target: pyautohands
Repos:
- PyAutoHands
Difficulty: easy
Autonomy: supervised
Priority: medium
Status: formalised
Consequence: glance
Witness: After `autohands pre_build <N>` on clean mains, `git -C lens/autolens_workspace_developer status --short` is empty (either its black-reformatted `slam_pipeline/` is committed with the rest, or black is not run on directories that will not be staged), and a test in PyAutoHands covers that the black dir set equals the staged dir set per workspace.
Filed: 2026-10-16

## Finding (health session 2026-10-16, release 2026.10.16.2 pre-build)

`pre_build.sh:170` runs black over `scripts` and `slam_pipeline` in every workspace, but `:196-197` adds `slam_pipeline` to `stage_dirs` only when `slam=true` (autolens_workspace). For autolens_workspace_developer, black reformatted `slam_pipeline/mgl_slam_batch.py` and then logged "No changes to commit", so the canonical checkout is left with an unstaged formatting diff. Heart reports that as worktree_drift (autolens_workspace_developer: 1 dirty) after every release. The same diff had been discarded earlier the same day; pre-build recreated it.

## Fix direction

Make the black set and the stage set the same: either stage `slam_pipeline` wherever black ran on it, or skip black on directories that will not be staged. Don't stage anything outside what the run produced (#126 leak class).

## Verified continuation — 2026-10-25 health session

Resume existing PR https://github.com/PyAutoLabs/PyAutoHands/pull/315, branch fix/pre-build-black-only-staged-dirs, head 0123d9b66cb4e4cb9c598494031817247b49c2f7. Do not create a duplicate task/PR. All three Python CI legs (3.12/3.13/3.14) failed the tenant-firewall step; Python 3.12 log reports 492 passed, 9 skipped before that step. Exact firewall mismatch: tests/test_pre_build_staging.py line 240 introduces instance fact autolens_workspace_developer in an unlisted file. Replace the explanatory docstring name with generic slam=false workspace wording, preserving the witness and firewall. Correct the invalid Python escape in the shell stub without changing its generated shell text.

A two-line patch is recoverably prepared in the health session checkout and report. Targeted 11 tests passed earlier. Full local suite has a process-reaping assertion that also fails on untouched head in this host (pgrep gives a PID not visible in /proc; ps fails lookup self). Do not waive the assertion or claim a source leak from that evidence; use supported-runner exact-head CI to decide. Check current claims and branch, preserve edits, run firewall plus full Python matrix, then human prm. No release or rehearsal.
