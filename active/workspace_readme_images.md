# Workspace README guide images

Issued: 2026-11-12
Issue: https://github.com/PyAutoLabs/autolens_workspace/issues/658
Type: docs
Targets: @autolens_workspace @autogalaxy_workspace
Branch: feature/workspace-readme-images
Tier: undeclared — merge mode: human /prm

## Original request

we made some images in RTD new user guide to show scale and dataset types, I think they should be also on the autolens_workspace and autogalaxy_Workspace README files

keep the text in the style of the rest, concise and snappy

## Approval and clarification

Yes, go ahead. Keep the captions concise and in the same style as the READMEs. maybe slihtly more text so they understand these images pair to packages they go to in the workspace

## Approved plan

- Reuse the four canonical RTD illustrations under Find Your Examples, before the existing tables.
- Add concise captions linking scales and dataset types to workspace example folders.
- Retain short illustration attribution and links to the full new user guides.
- Verify image URLs, folder targets and README formatting.

## Implementation

Only README.md changes in each workspace. Reference the images in the respective library's docs/overview/images/overview_2/ directory on main. Use relative scripts/ links for the examples and preserve existing navigation tables. No runtime or notebook changes.

Worktree: /home/jammy/Code/PyAutoLabs/.worktrees/workspace-readme-images
Validation: four remote PNGs return HTTP 200/image/png; all twelve added folder links contain start_here.py. Read the Docs rejects automated requests with HTTP 403; guide paths match the existing documentation sources.

## Checkpoint

Both READMEs edited locally and GFM rendering verified with pandoc. git diff --check passed. No runtime tests needed for README-only changes. No source commits, pushes or PRs: ship_workspace readiness returned RED. Preview: /mnt/c/Users/Jammy/Workspace/Science/scratch/workspace_readme_images_2026-11-12/. Next: human review of previews; development-only Heart override or recovered readiness before shipping.

### Exact Heart RED reasons

- PyAutoNerves: 2 commit(s) behind origin
- PyAutoArray: 2 commit(s) behind origin
- PyAutoGalaxy: 14 commit(s) behind origin
- PyAutoLens: on branch feature/non-imaging-features-review (not main)
- PyAutoLens: 4 uncommitted source change(s)
- PyAutoCTI: 2 commit(s) behind origin
- install verification FAILED (testpypi; checks F)
- release validation FAILED (stage integrate)
