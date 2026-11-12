# New User Guide visuals — complete

Issue: https://github.com/PyAutoLabs/PyAutoLens/issues/838

Shortened PyAutoLens and PyAutoGalaxy RTD guides and updated both start_here Python sources, regenerated notebooks and Markdown. Included system and dataset illustrations, original prompts and provenance. Lens illustrations carry indicative Einstein radii.

## Merged PRs
- https://github.com/PyAutoLabs/PyAutoLens/pull/839 — 7bf409646fdb07c826fcb3f34f0ef594c0002b4d
- https://github.com/PyAutoLabs/PyAutoGalaxy/pull/705 — 8c9260da18ac46c0206d944d793b2bad650a9b90
- https://github.com/PyAutoLabs/autolens_workspace/pull/649 — 4ee301ecccad4883da83b2f6424c2cdaf0ec7097
- https://github.com/PyAutoLabs/autogalaxy_workspace/pull/275 — 5816d73363e3410771746e935028c58fd266bf33

Libraries merged first, followed by workspaces, on explicit live user instruction. All library docs and Python 3.12/3.13/no-JAX CI legs passed. Workspace navigator and size checks passed; smoke matrix intentionally skipped because no smoke-relevant paths changed. Exact-head runs inspected. Heart freeze clear; prior RED shipping override recorded; no release performed.

Previews retained in C:\Users\Jammy\Workspace\Science\scratch\new_user_guide_lens_20261112\applied and new_user_guide_galaxy_20261112\applied.

## Original prompt

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

## Heart RED development override — #838

> Yes, override Heart RED for #838 and go ahead with the commits, pushes and all four PRs, including the images and start_here notebooks. Don't merge yet.

Current RED reasons:
- PyAutoNerves: 2 commit(s) behind origin
- PyAutoArray: 2 commit(s) behind origin
- PyAutoGalaxy: 4 commit(s) behind origin
- PyAutoLens: on branch feature/los-halos-review (not main)
- PyAutoLens: 2 uncommitted source change(s)
- PyAutoCTI: 2 commit(s) behind origin
- install verification FAILED (testpypi; checks F)
- release validation FAILED (stage integrate)

Validation: Focused Sphinx builds pass; notebook schema, code and metadata parity pass; image parity and diff checks pass; human editorial review approved. No runtime code changed; workspace smoke paths excluded by no_smoke_relevant_changes. Full numerical suites not run locally.

Authorized: commits, pushes and four PRs. No merge or release.

## PR-open checkpoint

- https://github.com/PyAutoLabs/PyAutoLens/pull/839
- https://github.com/PyAutoLabs/PyAutoGalaxy/pull/705
- https://github.com/PyAutoLabs/autolens_workspace/pull/649
- https://github.com/PyAutoLabs/autogalaxy_workspace/pull/275

All four pushed and open; two PNG assets verified in each remote PR. Workspace source, generated notebook and Markdown verified. No merge performed. Await separate human instruction.
