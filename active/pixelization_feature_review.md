# Apply approved pixelization introduction and illustration
Repos: @autolens_workspace @PyAutoLens
Type: docs
Consequence: judge

## Original request
Yes, add that near the top and apply the pixelization text and image to autolens_workspace, the main start_here.py and RTD. Open PRs for review, don't merge yet.

## Approved scope
Use pixelization_individual_review_20261112/v1, adding the approved source-science paragraph and source_science.py link immediately after the opening paragraph. Preserve existing teaching. Apply the illustration in feature, main tour and RTD. Retain RTD technical model diagram. Regenerate two notebooks/catalogues. Validate content, executable-code parity, notebook parity, images, navigation, smoke, library suite and RTD build. Open linked PRs only, no merge.

## Coordination
Human: "Allow separate documentation worktree" alongside jax-floor-0-12 and magnification-maps-wiring. Only overview text and image assets in PyAutoLens.

Issue: https://github.com/PyAutoLabs/autolens_workspace/issues/630
Issued: 2026-11-12

## Implementation and validation
Fresh checks: original teaching retained; early source-science link; narrative execution; executable AST and notebook code-cell parity; approved image identity and local links; navigator, size and whitespace checks. Focused Sphinx build of the exact edited pixelization section passed with warnings treated as errors. Full numerical tests/smoke were not rerun for this prose/assets-only change; preceding MGE validation passed 1021 tests (1 expected failure), 42 script and 2 notebook smoke checks, and all 12 PR CI jobs. No numerical code changes in this patch.

Both patches committed, pushed and opened for review. Heart RED 2026-11-12T11:24:54.298644+00:00: PyAutoLens: on branch feature/pixelization-feature-review (not main); PyAutoLens: 2 uncommitted source change(s). Human granted task-specific development-only override for #630: Yes, I approve the development-only Heart RED override for #630. Commit, push and open both PRs for review, but don't merge yet. No merge.

## Review handoff
Workspace: https://github.com/PyAutoLabs/autolens_workspace/pull/631 (e9b4b81a44867612d26befee76bb77f0ea8553bd)
RTD: https://github.com/PyAutoLabs/PyAutoLens/pull/826 (6ac85c8ec1e2c82732584302eaa9cc84c35d5ffc)
Both source worktrees clean. No merge. CI not awaited.
