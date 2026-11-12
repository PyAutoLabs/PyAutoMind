# Apply approved subhalo detection introduction and illustration
Repos: @autolens_workspace @PyAutoLens
Type: docs
Consequence: judge

## Original request
I like this. Apply the subhalo detection text and image to autolens_workspace, the main start_here.py and RTD. Open both PRs for review, don't merge yet.

## Plan
Apply the approved v1 introduction and corrected illustration. Preserve teaching and executable code. Update main tour and RTD with scientific use cases and sensitivity mapping early. Regenerate two notebooks and catalogues. Validate code/notebook parity, headings, image references, navigator, size and docs rendering. Open two linked PRs, no merge.

## Detailed implementation
- scripts/imaging/features/advanced/subhalo/detect/start_here.py: approved v1 narrative, repository-relative image path.
- start_here.py and docs/overview/overview_3_features.md: only Dark Matter Subhalos section.
- images/features/subhalo_detection_illustration.png and RTD overview_3 equivalent: identical approved image and prompt provenance.
- Generate corresponding notebooks with PyAutoHands, never hand edit.
- No numerical/API changes. Prior pixelization exact-head CI passed all 12 jobs; fresh checks cover this prose/assets delta, prior results are not new tests.

## Coordination
Same PyAutoLens claims as pixelization: jax-floor-0-12 and magnification-maps-wiring. Reuse explicit same-session approval for a separate documentation worktree; scope remains overview text/image assets.

Issue: https://github.com/PyAutoLabs/autolens_workspace/issues/632
Issued: 2026-11-12

## Validation
Fresh checks passed: syntax, executable AST and generated notebook code-cell parity, exact approved feature text (apart from image path), identical approved image assets, local image links, navigator/banner lint, search-memory check, size guard, whitespace and focused Sphinx build with warnings treated as errors. Full numerical/smoke suites were not rerun for this prose/assets-only patch; the preceding pixelization PRs passed all 12 exact-head CI jobs. No API or numerical changes.

Feature classifier heuristics overestimated API/architectural risk from repo names; inspection confirms documentation-only scope. No public API changes or phasing required.

## Shipping checkpoint
Heart RED 2026-11-12T11:54:58.076217+00:00: PyAutoLens: on branch feature/subhalo-detection-review (not main); PyAutoLens: 2 uncommitted source change(s). Await task-specific development-only override for #632 before source commit/push/PR. No merge.
