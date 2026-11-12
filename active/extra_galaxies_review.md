# Extra Galaxies feature review

Issue: https://github.com/PyAutoLabs/autolens_workspace/issues/648
Issued: 2026-11-12
Consequence: judge
Repos: @autolens_workspace @PyAutoLens
Branch: feature/extra-galaxies-review

## Original request

This is better. Apply the revised Extra Galaxies image and text to autolens_workspace, the main start_here.py and RTD. Open both PRs for review, don't merge yet.

## Coordination approval

Yes, proceed with extra_galaxies in a separate documentation worktree alongside both tasks. Preserve their changes and check merge compatibility. Open both PRs for review, don't merge yet.

## Plan

- Apply approved feature text and v2 image titled Extra Galaxies, preserving scientific use cases and teaching detail.
- Add an Extra Galaxies overview beside the group section in the root workspace tour and RTD feature page, using identical assets.
- Regenerate affected notebooks and catalogues with PyAutoHands.
- Validate approved prose/image parity, executable AST and notebook code-cell invariance, image references, notebook schemas, focused Sphinx render, navigation/search-memory/size/whitespace checks.
- Check compatibility with new-user-guide-visuals and start-here-plot-ai without editing their worktrees.
- Open paired PRs, library first, behind the Heart gate. Do not merge.

Tier: judge — merge mode: human /prm.

## Detailed scope

Primary autolens_workspace: scripts/imaging/features/extra_galaxies/start_here.py, root start_here.py, notebook counterparts, generated catalogue files, images/features/extra_galaxies.png and provenance.
PyAutoLens: docs/overview/overview_3_features.md, docs/overview/images/overview_3/extra_galaxies.png and provenance.
Approved input: /mnt/c/Users/Jammy/Workspace/Science/scratch/extra_galaxies_individual_review_20261112/v2/.
Adapt only the feature's relative image path. No changes to simulators, runtime, APIs, configuration or dataset-level introductions. Numerical suites not rerun for prose-only scope; required CI gates any future merge.

## Survey

Clean separate worktrees from origin/main. Canonical PyAutoLens main is behind with unrelated paper_jax/paper.md edits; canonical workspace main behind with untracked dataset.fits; preserved. User explicitly authorizes coexistence with new-user-guide-visuals (both repos) and start-here-plot-ai (workspace). Their in-progress changes will be checked via patch compatibility. Heart entry YELLOW permits development; shipping gate remains separate.

Brain classification combined library/workspace accepted. Generic large/API-risk phased recommendation is inapplicable to this bounded approved prose/image-only task; no API changes.
