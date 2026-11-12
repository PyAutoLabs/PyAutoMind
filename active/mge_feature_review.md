# Apply approved MGE introduction and illustration
Repos: @autolens_workspace @PyAutoLens
Type: docs
Consequence: judge

## Original request
I like this, apply the MGE text and image to autolens_workspace and use the image in the main start_here.py and RTD too. Open a PR for review, dont merge yet.

## Approved plan
Use the approved 2026-11-12/v1 preview. Replace imaging/features/multi_gaussian_expansion/start_here.py, preserve all substantive teaching, add the illustration and provenance, update the workspace main start_here.py MGE block, regenerate affected notebooks and catalogues. Update the PyAutoLens RTD overview MGE block and image after repository-claim coordination approval. Validate syntax/AST preservation, generated notebook code parity, links, catalogue, smoke and applicable docs checks. Two linked review PRs; no merge.

## Branch survey
Canonical autolens_workspace main with pre-existing untracked dataset.fits; PyAutoLens main clean but claimed by magnification-maps-wiring (#818). Separate feature/mge-feature-review workspace/Mind worktrees created from origin/main. Library docs claim permission requested, pending.

Issue: https://github.com/PyAutoLabs/autolens_workspace/issues/628
Issued: 2026-11-12
Coordination approval: human "Allow separate documentation worktree"; only MGE overview text and image assets in PyAutoLens.
