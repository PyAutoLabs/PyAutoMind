# Apply approved potential correction introduction and two-panel illustration
Repos: @autolens_workspace @PyAutoLens
Type: docs
Consequence: judge

## Original request
This is better. Apply the two-panel image and potential correction text to autolens_workspace, the main start_here.py and RTD. Open both PRs for review, don't merge yet.

## Plan
Apply approved v2 review text/image. Retain equations and teaching, clarify scientific uses and model-relative corrections. Add distinct Potential Correction overview after Sensitivity Mapping in main tour and RTD. Regenerate two notebooks/catalogues. Validate syntax, executable AST/notebook cell parity, approved text/image identity, links, navigation, size and focused docs build. Open linked review PRs, no merge.

## Detailed implementation
- scripts/imaging/features/advanced/potential_correction/start_here.py: approved v2 text, repository-relative image reference.
- start_here.py and docs/overview/overview_3_features.md: new Potential Correction section.
- images/features/potential_correction_illustration.png and RTD overview_3 counterpart: identical approved two-panel image plus provenance.
- Generate notebooks/catalogues with PyAutoHands; no manual notebook editing.
- No executable or API changes. Prior sensitivity-mapping CI is historical evidence, not fresh tests.

## Coordination
Reuse explicit same-session separate documentation worktree approval alongside magnification-maps-wiring. Branch feature/potential-correction-review; no new overlapping claim. Tier judge; no merge.


Issue: https://github.com/PyAutoLabs/autolens_workspace/issues/636
Issued: 2026-11-12

## Validation
Fresh checks passed: syntax, executable AST and generated notebook code-cell parity, approved feature-text parity (image path only), identical approved two-panel image assets, local image links, navigator/banner lint, search-memory check, script-size guard, whitespace and focused Sphinx build with warnings treated as errors. All eight narrative blocks and original unique headings retained; repeated Related Examples consolidated. No API or executable changes. Full numerical/smoke suites were not rerun for this prose/assets-only patch; preceding sensitivity-mapping PRs passed all 12 exact-head CI jobs, which are prior evidence rather than fresh tests.

Classifier API-risk/phasing heuristics overestimated this docs-only scope; inspection confirms no public API or numerical change.

## Shipping checkpoint
Heart RED 2026-11-12T15:25:16.865951+00:00: PyAutoLens: on branch feature/potential-correction-review (not main); PyAutoLens: 2 uncommitted source change(s). Override subsequently approved below; both review PRs now open. No merge.

## Development-only Heart RED override

Human authorization (2026-11-12): “I approve the development-only Heart RED override for #636. Commit, push and open both PRs for review, don't merge yet.”

Exact RED reasons (2026-11-12T15:25:16.865951+00:00):
- `PyAutoLens: on branch feature/potential-correction-review (not main)`
- `PyAutoLens: 2 uncommitted source change(s)`

Fresh checks passed: syntax, executable AST and generated notebook code-cell parity, approved feature-text parity (image path only), identical approved two-panel image assets, local image links, navigator/banner lint, search-memory check, script-size guard, whitespace and focused Sphinx build with warnings treated as errors. All eight narrative blocks and original unique headings retained; repeated Related Examples consolidated. No API or executable changes. Full numerical/smoke suites were not rerun for this prose/assets-only patch; preceding sensitivity-mapping PRs passed all 12 exact-head CI jobs, which are prior evidence rather than fresh tests.

Commit, push and PR-open only; no merge, release or CI bypass.

## Review PR handoff — 2026-11-12
- Workspace: https://github.com/PyAutoLabs/autolens_workspace/pull/637 — 18c58f3bd9c759440b223f5bc1ba4b0c532f4a39
- RTD: https://github.com/PyAutoLabs/PyAutoLens/pull/829 — 0c42bcc55b93784eb11b6ff9ac7cb1d6848913f9
- Both committed and pushed under the approved #636 development-only override. Open for human review; neither merged. CI not awaited. Next: human review, then separately authorized CI/freeze check and merge.

## Completed — 2026-11-12
User explicitly authorized merging if CI green and freeze clear. All 12 exact-head jobs passed (4 PyAutoLens, 8 workspace), no skipped legs, both PRs CLEAN. Heart: not frozen.
Library PR #829 merged first: 94ad9bd9718904e4853c5e534c488e3154ea589f. Workspace PR #637 then merged: 3d6d7e396f7aff6326cd25b06978fc6d387aeed8. Both branch tips proved ancestors of origin/main after fetch. Issue #636 closed. Approved science-first text and two-panel illustration applied across feature, main tour and RTD; technical teaching retained. No numerical changes.

## Original prompt

# Apply approved potential correction introduction and two-panel illustration
Repos: @autolens_workspace @PyAutoLens
Type: docs
Consequence: judge

## Original request
This is better. Apply the two-panel image and potential correction text to autolens_workspace, the main start_here.py and RTD. Open both PRs for review, don't merge yet.

## Plan
Apply approved v2 review text/image. Retain equations and teaching, clarify scientific uses and model-relative corrections. Add distinct Potential Correction overview after Sensitivity Mapping in main tour and RTD. Regenerate two notebooks/catalogues. Validate syntax, executable AST/notebook cell parity, approved text/image identity, links, navigation, size and focused docs build. Open linked review PRs, no merge.

## Detailed implementation
- scripts/imaging/features/advanced/potential_correction/start_here.py: approved v2 text, repository-relative image reference.
- start_here.py and docs/overview/overview_3_features.md: new Potential Correction section.
- images/features/potential_correction_illustration.png and RTD overview_3 counterpart: identical approved two-panel image plus provenance.
- Generate notebooks/catalogues with PyAutoHands; no manual notebook editing.
- No executable or API changes. Prior sensitivity-mapping CI is historical evidence, not fresh tests.

## Coordination
Reuse explicit same-session separate documentation worktree approval alongside magnification-maps-wiring. Branch feature/potential-correction-review; no new overlapping claim. Tier judge; no merge.


Issue: https://github.com/PyAutoLabs/autolens_workspace/issues/636
Issued: 2026-11-12

## Validation
Fresh checks passed: syntax, executable AST and generated notebook code-cell parity, approved feature-text parity (image path only), identical approved two-panel image assets, local image links, navigator/banner lint, search-memory check, script-size guard, whitespace and focused Sphinx build with warnings treated as errors. All eight narrative blocks and original unique headings retained; repeated Related Examples consolidated. No API or executable changes. Full numerical/smoke suites were not rerun for this prose/assets-only patch; preceding sensitivity-mapping PRs passed all 12 exact-head CI jobs, which are prior evidence rather than fresh tests.

Classifier API-risk/phasing heuristics overestimated this docs-only scope; inspection confirms no public API or numerical change.

## Shipping checkpoint
Heart RED 2026-11-12T15:25:16.865951+00:00: PyAutoLens: on branch feature/potential-correction-review (not main); PyAutoLens: 2 uncommitted source change(s). Override subsequently approved below; both review PRs now open. No merge.

## Development-only Heart RED override

Human authorization (2026-11-12): “I approve the development-only Heart RED override for #636. Commit, push and open both PRs for review, don't merge yet.”

Exact RED reasons (2026-11-12T15:25:16.865951+00:00):
- `PyAutoLens: on branch feature/potential-correction-review (not main)`
- `PyAutoLens: 2 uncommitted source change(s)`

Fresh checks passed: syntax, executable AST and generated notebook code-cell parity, approved feature-text parity (image path only), identical approved two-panel image assets, local image links, navigator/banner lint, search-memory check, script-size guard, whitespace and focused Sphinx build with warnings treated as errors. All eight narrative blocks and original unique headings retained; repeated Related Examples consolidated. No API or executable changes. Full numerical/smoke suites were not rerun for this prose/assets-only patch; preceding sensitivity-mapping PRs passed all 12 exact-head CI jobs, which are prior evidence rather than fresh tests.

Commit, push and PR-open only; no merge, release or CI bypass.

## Review PR handoff — 2026-11-12
- Workspace: https://github.com/PyAutoLabs/autolens_workspace/pull/637 — 18c58f3bd9c759440b223f5bc1ba4b0c532f4a39
- RTD: https://github.com/PyAutoLabs/PyAutoLens/pull/829 — 0c42bcc55b93784eb11b6ff9ac7cb1d6848913f9
- Both committed and pushed under the approved #636 development-only override. Open for human review; neither merged. CI not awaited. Next: human review, then separately authorized CI/freeze check and merge.
