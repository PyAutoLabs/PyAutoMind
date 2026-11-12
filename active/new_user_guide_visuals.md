# New User Guide visuals

Issue: https://github.com/PyAutoLabs/PyAutoLens/issues/838
Status: human-review. No PRs authorized.

## User request

> Looks good, apply this version to the PyAutoLens New User Guide. Then draft the equivalent PyAutoGalaxy guide with suitable images and show me a preview before applying it. Don't raise PRs yet.

> Make sure these images and updates all make their way into the start here notebook too

## Checkpoint — 2026-11-12

Approved Lens v3 applied to RTD New User Guide and workspace start_here.py, regenerated start_here.ipynb and markdown/start_here.md. Both AI illustrations and prompt/provenance files included in each repo. Workspace assets explicitly staged because images directories are ignored. API walkthrough code and later feature prose preserved.

Worktree: /home/jammy/Code/PyAutoLabs/.worktrees/new-user-guide-visuals
Repos: PyAutoLens and autolens_workspace, both feature/new-user-guide-visuals.

Validation: focused Sphinx build with warnings as errors; notebook schema/code/metadata parity; unchanged API code and later feature prose; image parity; git diff --check. Galaxy example destinations checked at pinned release.

Lens applied preview: /mnt/c/Users/Jammy/Workspace/Science/scratch/new_user_guide_lens_20261112/applied/index.html
Galaxy draft preview: /mnt/c/Users/Jammy/Workspace/Science/scratch/new_user_guide_galaxy_20261112/v1/index.html

Galaxy draft includes three-panel galaxy-system and dataset illustrations, proposed notebook section and source preview. No Galaxy repository edits. Await human review before applying Galaxy; no PRs or merges.

## Galaxy approval and application — 2026-11-12

> Looks good, apply the PyAutoGalaxy version to the RTD guide and start_here notebook too, including the images. Don't raise PRs yet.

Applied approved Galaxy v1 to PyAutoGalaxy/docs/overview/overview_2_new_user_guide.md and autogalaxy_workspace/start_here.py, regenerated start_here.ipynb and updated markdown/start_here.md. Both images, original prompts and provenance included in each repository. Added PyAutoGalaxy and autogalaxy_workspace to the existing worktree bundle on feature/new-user-guide-visuals. Earlier draft-only status is superseded by this approval.

Validation passed: focused Sphinx build with warnings as errors, notebook schema and code/metadata parity, preserved API walkthrough and later features, identical image bytes across repositories, pinned notebook destinations and diff whitespace checks.

Applied preview: /mnt/c/Users/Jammy/Workspace/Science/scratch/new_user_guide_galaxy_20261112/applied/index.html
No PRs raised. Library/workspace changes remain uncommitted for review.
