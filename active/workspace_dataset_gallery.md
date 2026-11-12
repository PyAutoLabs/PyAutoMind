# Workspace dataset gallery

Issued: 2026-11-12
Issue: https://github.com/PyAutoLabs/autolens_workspace/issues/666
Type: docs
Targets: @autolens_workspace @PyAutoLens
Branch: feature/workspace-dataset-gallery
Worktree: /home/jammy/Code/PyAutoLabs/.worktrees/workspace-dataset-gallery
Status: PRs open; CI pending
Consequence: judge

## Request

I thin I anted us to chekc if theres better images for datasets now made in the new user guide on RTD?

## Approved proposal

Replace the compact PyAutoLens README dataset strip with a two-column gallery reusing the newer interferometry, multi-wavelength, data-cube and point-source illustrations. Each gets a short caption linking to its workspace folder. Keep a direct imaging link. Insert the existing multi_wavelength.png into the RTD multi-band card. User approval: "yep thats good".

## Result and validation

- autolens_workspace/README.md: four-image gallery with linked captions; existing scale and weak-lensing sections retained.
- PyAutoLens/docs/overview/overview_2_new_user_guide.md: two-line insertion for the missing multi-band image.
- All nine distinct added/preserved relative folder links resolve to start_here.py; six used assets exist. GFM render, git diff --check and focused Sphinx/MyST/Furo build with warnings as errors pass.
- Preview: /mnt/c/Users/Jammy/Workspace/Science/scratch/workspace_dataset_gallery_2026-11-12/autolens_workspace.html
- RTD preview: same folder, rtd/overview_2_new_user_guide.html
- Other chat's new-user-guide-rebalance worktree edits this RTD file's prose; preserve those edits when combining. This change inserts only the image into the existing multi-band card. No edits made to that other worktree.
- Follow-up to completed autolens_workspace#658; no commits, PRs or merge for this new gallery yet. Prior task's shipping/merge authorization is not reused.

## Imaging tile follow-up

User: "I thikn we need an imafge for imaging? beyond that i like it a lot".

Added a standalone imaging.png (built-in image_gen, prompt/provenance beside the asset) to a centered Imaging tile above the four-image gallery and to the RTD Imaging card. Caption links to scripts/imaging. Refreshed both previews; folder/image checks, GFM rendering, strict focused Sphinx build and diff whitespace checks pass. Still local and unpublished.

## Shipping checkpoint

Looks good, open PRs for the gallery and RTD changes, then merge RTD first once CI is green. I'm happy with the documentation-only smoke skips. Close out the task after.

RTD: https://github.com/PyAutoLabs/PyAutoLens/pull/857 (2c5d4e13f). Gallery: https://github.com/PyAutoLabs/autolens_workspace/pull/667 (799fe3f2). Merge RTD first; current-turn human merge authority.
