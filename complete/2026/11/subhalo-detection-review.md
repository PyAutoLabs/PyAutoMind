# Subhalo detection introduction and illustration

Merged 2026-11-12 after explicit human merge instruction, all 12 exact-head CI jobs passed, and Heart freeze returned not frozen. No release performed.

- Workspace PR: https://github.com/PyAutoLabs/autolens_workspace/pull/633
- Workspace merge: e555a20b28a99458544e3e3c107702ce7c80c37b
- RTD PR: https://github.com/PyAutoLabs/PyAutoLens/pull/827
- RTD merge: 99cf36a3efcddd80033036ac934c01aa1ecf3544
- Issue: https://github.com/PyAutoLabs/autolens_workspace/issues/632 (closed)

Applied approved scientific-use-case opening, early sensitivity-mapping and 54-lens paper links, preserved teaching, repaired contents and qualified evidence interpretation. Approved conceptual arc-perturbation illustration used in feature, workspace tour and RTD. Notebooks/catalogues regenerated. No executable/API changes.

Fresh local syntax, executable AST/notebook code-cell parity, approved text and image identity, image paths, navigation, size and focused Sphinx checks passed. All 8 workspace and 4 PyAutoLens CI jobs passed on the shipped heads.

Human review: /mnt/c/Users/Jammy/Workspace/Science/scratch/subhalo_detection_individual_review_20261112/applied/index.html

Continue individual feature reviews, bringing scientific use cases forward and preserving teaching detail. No next feature selected yet.

## Original prompt

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
Heart RED 2026-11-12T11:54:58.076217+00:00: PyAutoLens: on branch feature/subhalo-detection-review (not main); PyAutoLens: 2 uncommitted source change(s). Override approved in the following live user turn and recorded below. No merge.

## Development-only Heart RED override

Human authorization (2026-11-12): “I approve, contnue”, in direct response to the #632 development-only override request for commit, push and both review PRs. No merge authorized.

Exact RED reasons (2026-11-12T11:54:58.076217+00:00):
- `PyAutoLens: on branch feature/subhalo-detection-review (not main)`
- `PyAutoLens: 2 uncommitted source change(s)`

Fresh checks passed: syntax, executable AST and generated notebook code-cell parity, exact approved feature text (apart from image path), identical approved image assets, local image links, navigator/banner lint, search-memory check, size guard, whitespace and focused Sphinx build with warnings treated as errors. Full numerical/smoke suites were not rerun for this prose/assets-only patch; the preceding pixelization PRs passed all 12 exact-head CI jobs. No API or numerical changes.

No release, CI bypass or merge.

## Review handoff
Workspace: https://github.com/PyAutoLabs/autolens_workspace/pull/633 (14378ac299a0ce542e15b5c5087a5daf89da3a9c)
RTD: https://github.com/PyAutoLabs/PyAutoLens/pull/827 (ded15da089bf0401f186922d5cb097cdefc12828)
Both source worktrees clean; no merge; CI not awaited.
