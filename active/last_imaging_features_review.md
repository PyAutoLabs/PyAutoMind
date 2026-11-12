# Last three imaging feature introductions

Issue: https://github.com/PyAutoLabs/autolens_workspace/issues/654
Issued: 2026-11-12
Consequence: judge
Repos: @autolens_workspace @PyAutoLens
Branch: feature/last-imaging-features-review

## Original request

I like these. Apply all three texts and images to autolens_workspace, the main start_here.py and RTD, reusing the subhalo image. Open both PRs for review, don't merge yet.

## Coordination

Live reply: "Allow separate documentation worktree" to coexist with api-reference-polish and general-docs-refresh. Preserve their files and verify compatibility.

## Plan

- Apply approved v1 No Lens Light, Sky Background and Subhalo parent introductions, adapting only local image paths.
- Add No Lens Light to main tour and RTD, replace the sky summary, and add an overview route to the existing dark-matter subhalo section without duplicating or replacing its approved detection image.
- Copy two approved images/provenance into both repos; reuse existing approved subhalo image byte-for-byte.
- Regenerate the three feature notebooks, root notebook and navigation catalogues through PyAutoHands.
- Validate exact approved prose/images, unchanged executable code, notebook schemas and links, navigation/search-memory/size/whitespace, focused Sphinx rendering and compatibility with concurrent tasks.
- Open paired review PRs, library first, behind Heart shipping gate; no merge.

Tier: judge — merge mode: human /prm.

## Detailed scope

Workspace: scripts/imaging/features/no_lens_light/start_here.py, advanced/sky_background/start_here.py and advanced/subhalo/start_here.py; root start_here.py; notebook counterparts; llms-full.txt/workspace_index.json; images/features/{no_lens_light,sky_background}.png plus provenance. Existing images/features/subhalo_detection_illustration.png is reused, not edited.
Library: docs/overview/overview_3_features.md and docs/overview/images/overview_3/ matching new image/provenance assets. Preserve existing subhalo illustration.
Approved input: /mnt/c/Users/Jammy/Workspace/Science/scratch/last_three_imaging_review_20261112/v1/.
No runtime/API/config/simulator changes, including the noted sky prior boundary. Local numerical suites not repeated for documentation-only changes; CI required before any later merge.
Clean worktrees rooted at /home/jammy/Code/PyAutoLabs/.worktrees/last-imaging-features-review. Preserve unrelated canonical paper_jax/paper.md, dataset.fits and other tasks' dirty Mind state.

Classification disposition: bounded documentation-only batch, no API changes. Generic classifier design/core-API phasing is inapplicable; keep the two user-approved paired documentation PRs.
