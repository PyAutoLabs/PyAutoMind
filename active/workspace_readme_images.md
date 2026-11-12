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

## Follow-up: multi-band and weak lensing (2026-11-12)

User approved: "Yes, add the multi-band imaging panel and the weak lensing image, with concise text linking to multi_dataset/ and weak/. Update the preview so I can see them." Also: "and put thee on RTD where suitable too".

- Attached PyAutoLens on feature/workspace-readme-images, base b24eabe2e, for docs-only changes.
- Used built-in image_gen to extend docs/overview/images/overview_2/dataset_types.png with a separate multi-band panel; saved multiband_image_edit_prompt.txt and provenance alongside it.
- Updated autolens_workspace/README.md with multi_dataset and weak links, reusing overview_3/strong_weak_lensing.png.
- Updated PyAutoLens/docs/overview/overview_2_new_user_guide.md with the five-panel strip, multi-band card and weak-lensing section. Existing weak illustration stays on the features page too.
- Added folder/start_here links and git diff --check pass. Focused Sphinx/MyST + sphinx_design + Furo page build passes with warnings as errors; no numerical tests for prose/assets.
- Preview root: /mnt/c/Users/Jammy/Workspace/Science/scratch/workspace_readme_images_2026-11-12/ ; RTD: rtd/overview_2_new_user_guide.html. README embeds local assets so changes are visible before merge.
- Build log: .worktrees/workspace-readme-images/tmp/rtd-build.log (workspace-relative).
- Still local/unpublished: ship PyAutoLens docs before workspace PRs so the canonical image URL displays the updated strip. Heart RED shipping block remains; no override requested or implied.

## PR-open checkpoint (2026-11-12)

Live authorization: "Looks good, go ahead and open PRs for the README and RTD changes."

- PyAutoLens#854: e3a171ee29d1dd090eaca5b72bde21090221e638; RTD guide, dataset image, provenance and prompt.
- autolens_workspace#662: f92aa7dd; README only.
- autogalaxy_workspace#279: f538c3e; README only.
- Same isolated worktree and feature/workspace-readme-images branches. Applicable checks and human visual review passed; no source changes since reviewed preview.
- Development-only Heart RED authorization, exact current reasons and validation recorded on issue, all PR bodies, active.md and first autonomy_log table.
- Deliverable reached: three open PRs, no merge or release. Human /prm next; merge PyAutoLens#854 before autolens_workspace#662. CI must pass before merge.
