# Apply approved sensitivity mapping introduction and illustration
Repos: @autolens_workspace @PyAutoLens
Type: docs
Consequence: judge

## Original request
I like this. Apply the sensitivity mapping text and image to autolens_workspace, the main start_here.py and RTD. Open both PRs for review, don't merge yet.

## Plan
Apply the approved v1 narrative and image, keeping teaching detail and correcting the four-position fixed-injected-mass grid description. Add distinct sensitivity sections after subhalo detection in the main tour and RTD. Generate affected notebooks/catalogues. Validate syntax, unchanged executable AST/notebook code cells, exact approved draft, images and navigation, script sizes and focused docs rendering. Open linked review PRs only, no merge.

## Detailed implementation
- scripts/imaging/features/advanced/subhalo/sensitivity/start_here.py: approved v1; repository-relative image link.
- start_here.py and docs/overview/overview_3_features.md: new Sensitivity Mapping section immediately after Dark Matter Subhalos, preserving detection content.
- images/features/sensitivity_mapping_illustration.png and RTD overview_3 counterpart: identical approved image plus prompt provenance.
- Regenerate both notebooks and navigation catalogues using PyAutoHands.
- No API or executable changes. Fresh prose/assets checks; prior subhalo CI results are not fresh tests for this patch.

## Coordination
Reuse explicit same-session approval for separate documentation worktree alongside magnification-maps-wiring. No new conflicting claim. Branch feature/sensitivity-mapping-review; worktrees clean at start. Tier judge, no merge.


Issue: https://github.com/PyAutoLabs/autolens_workspace/issues/634
Issued: 2026-11-12

## Validation
Fresh checks passed: syntax, executable AST and generated notebook code-cell parity, approved feature text parity (image path and trailing-space cleanup only), image identity and local links, navigator/banner lint, search-memory check, script-size guard, whitespace and focused Sphinx build with warnings treated as errors. All 15 narrative blocks and original headings retained. No API or executable changes. Full numerical/smoke suites were not rerun for this prose/assets-only patch; the preceding subhalo PRs passed all 12 exact-head CI jobs, which are prior evidence rather than fresh tests.

Classifier API-risk/phasing heuristics overestimated this docs-only scope; inspection confirms no public API or numerical change.

## Shipping checkpoint
Heart RED 2026-11-12T14:24:33.416704+00:00: PyAutoLens: on branch feature/sensitivity-mapping-review (not main); PyAutoLens: 2 uncommitted source change(s). Await task-specific development-only override for #634 before source commit/push/PR. No merge.
