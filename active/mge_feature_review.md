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

## Development-only Heart RED override — 2026-11-12

Human (verbatim): Yes, I approve the development-only Heart RED override for #628. Commit, push and open both PRs for review, but don't merge yet.

Exact RED reasons (2026-11-12T10:38:39.599379+00:00):
- PyAutoNerves: 2 commit(s) behind origin
- PyAutoFit: 2 commit(s) behind origin
- PyAutoLens: on branch feature/mge-feature-review (not main)
- PyAutoLens: 2 uncommitted source change(s)

1021 PyAutoLens tests passed, 1 expected failure; 42 script and 2 notebook smoke checks passed; Sphinx HTML build passed (96 warnings, none for edited MGE page); AST/notebook parity, image identity/paths, navigator, size and whitespace checks passed. Human approved content; in-session diff review complete.

Commit/push/open both PRs only; no merge, release or failed-check bypass.

## PRs opened — 2026-11-12

RTD: https://github.com/PyAutoLabs/PyAutoLens/pull/825 at b677447ab. Workspace: https://github.com/PyAutoLabs/autolens_workspace/pull/629 at 621f8a67. Both pushed and open; no merge. Local validation passed; GitHub CI pending separate review.
