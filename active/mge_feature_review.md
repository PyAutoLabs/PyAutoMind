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

## Implementation complete, shipping gate pending

1021 PyAutoLens tests passed, 1 xfailed; 42 script + 2 notebook smoke checks passed; Sphinx HTML build succeeded (96 warnings, none for edited MGE page); executable AST/notebook code parity, image identity and relative paths, navigator, size guard and whitespace checks passed.

Approved text/image applied in feature, main tour and RTD. Two notebooks and workspace catalogues regenerated. Both source diffs staged; no source commit/push/PR. Heart RED 2026-11-12T10:38:39.599379+00:00: PyAutoNerves: 2 commit(s) behind origin; PyAutoFit: 2 commit(s) behind origin; PyAutoLens: on branch feature/mge-feature-review (not main); PyAutoLens: 2 uncommitted source change(s). A new task-specific development-only override is required for #628. Earlier #626 override does not apply.
