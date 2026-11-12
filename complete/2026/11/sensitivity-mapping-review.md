# Sensitivity mapping introduction and illustration

Merged 2026-11-12 on explicit human instruction after all 12 exact-head CI jobs passed and Heart freeze returned not frozen. No release performed.

- Workspace PR: https://github.com/PyAutoLabs/autolens_workspace/pull/635
- Workspace merge: de38eb208746aebcf861c5174773fd9fb2f0ac83
- RTD PR: https://github.com/PyAutoLabs/PyAutoLens/pull/828
- RTD merge: b5768d53bbfaf2723e9cd70380655450ffb90bde
- Issue: https://github.com/PyAutoLabs/autolens_workspace/issues/634 (closed)

Applied approved scientific-use-case opening, early population-study context and pixelized-source link; all 15 teaching blocks retained. Corrected the four-position fixed injected-mass grid description and distinguished injection values from recovery-fit priors. Added approved conceptual sensitivity illustration to feature, distinct main-tour section and RTD. Notebooks/catalogues regenerated. Executable code and APIs unchanged.

Local syntax, executable AST/notebook code-cell parity, approved text/image parity, image paths, navigation, size and focused Sphinx checks passed. All 8 workspace and 4 PyAutoLens exact-head CI jobs passed.

Human review: /mnt/c/Users/Jammy/Workspace/Science/scratch/sensitivity_mapping_individual_review_20261112/applied/index.html

Continue individual feature reviews with scientific use cases up front, striking illustrative images and preserved teaching detail. No next feature selected.

## Original prompt

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
Heart RED 2026-11-12T14:24:33.416704+00:00: PyAutoLens: on branch feature/sensitivity-mapping-review (not main); PyAutoLens: 2 uncommitted source change(s). Task-specific override approved in the subsequent live user turn and recorded below. No merge.

## Development-only Heart RED override

Human authorization (2026-11-12): “I approve the development-only Heart RED override for #634. Commit, push and open both PRs for review, don't merge yet.”

Exact RED reasons (2026-11-12T14:24:33.416704+00:00):
- `PyAutoLens: on branch feature/sensitivity-mapping-review (not main)`
- `PyAutoLens: 2 uncommitted source change(s)`

Fresh checks passed: syntax, executable AST and generated notebook code-cell parity, approved feature text parity (image path and trailing-space cleanup only), image identity and local links, navigator/banner lint, search-memory check, script-size guard, whitespace and focused Sphinx build with warnings treated as errors. All 15 narrative blocks and original headings retained. No API or executable changes. Full numerical/smoke suites were not rerun for this prose/assets-only patch; the preceding subhalo PRs passed all 12 exact-head CI jobs, which are prior evidence rather than fresh tests.

Commit, push and PR-open only; no merge, release or CI bypass.

## Review handoff
Workspace: https://github.com/PyAutoLabs/autolens_workspace/pull/635 (2631a3a74b1a1e288d1ff08d27f93f693a20ffa4)
RTD: https://github.com/PyAutoLabs/PyAutoLens/pull/828 (7b4a1a87b319e889fc8b86b6dff866472451391d)
Both source worktrees clean; no merge. CI not awaited.
