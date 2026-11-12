# Shapelets feature review
Repos: @autolens_workspace @PyAutoLens
Type: docs
Consequence: judge

## Original request
I like this. Apply the shapelets text and image to autolens_workspace, the main start_here.py and RTD. Keep the existing basis grid as a teaching figure. Open both PRs for review, don't merge yet.

## Coordination authorization
Yes, proceed with the shapelets changes in a separate documentation worktree alongside three-autos-public-framing. Open both PRs for review, don't merge yet.

## Plan
Apply the approved shapelets draft and minimal-text illustration. Lead with source science and preserve basis, solver, interpretation and fitting detail. Retain the existing basis grid as a teaching figure. Update main tour and RTD, correcting obsolete navigation. Generate notebooks/catalogues and validate before opening two linked review PRs. No merge.

## Detailed implementation
- scripts/imaging/features/advanced/shapelets/start_here.py: approved draft with repository-relative image references.
- start_here.py and docs/overview/overview_3_features.md: science-first Shapelets section, new illustration, existing basis grid retained below explanatory text.
- images/features/shapelets_illustration.png and shapelets_basis.png; RTD overview_3/shapelets_illustration.png and existing shapelets.png. Preserve the original grid byte-for-byte.
- Add image prompt/provenance; regenerate root and feature notebooks plus catalogues via PyAutoHands.
- Check syntax, unchanged executable AST/notebook code, approved text/image parity, local links, navigator/banner, search-memory, size, whitespace and focused Sphinx build.
- No API or numerical changes. Prior CI evidence distinguished from fresh documentation checks.

Branch: feature/shapelets-review
Worktree: /home/jammy/Code/PyAutoLabs/.worktrees/shapelets-review
Tier: judge — review PRs only; no merge.
Approved preview: /mnt/c/Users/Jammy/Workspace/Science/scratch/shapelets_individual_review_20261112/v1/


Issue: https://github.com/PyAutoLabs/autolens_workspace/issues/642
Issued: 2026-11-12
Classifier API/phasing heuristics overestimate the docs-only scope; inspection confirms no API/numerical change.
