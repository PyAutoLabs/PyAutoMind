# pre_build runs black on slam_pipeline/ for every workspace but stages it only for autolens_workspace — leaves a dirty canonical checkout each release

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
