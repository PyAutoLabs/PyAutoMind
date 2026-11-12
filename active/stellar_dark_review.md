# Apply approved stellar + dark matter introduction and illustration
Repos: @autolens_workspace @PyAutoLens
Type: docs
Consequence: judge

## Original request
I like this. Apply the stellar + dark matter text and image to autolens_workspace, the main start_here.py and RTD. Open both PRs for review, don't merge yet.

## Plan
Apply the approved v1 feature text and two-panel image. Lead with scientific uses and Nightingale et al. (2019), retain teaching and model assumptions, distinguish tutorial priors from staged fitting. Add dedicated stellar + dark matter summaries to the tour and RTD while preserving multipole guidance. Regenerate the affected notebooks and catalogues. Open linked review PRs, no merge.

## Detailed implementation
- scripts/imaging/features/advanced/mass_stellar_dark/start_here.py: exact approved draft except repository-relative image reference.
- start_here.py and docs/overview/overview_3_features.md: separate stellar + dark matter section from general Mass Models; replace overconfident decomposition wording.
- images/features/stellar_dark_illustration.png and RTD overview_3 counterpart: identical approved asset plus prompt/provenance.
- Generate root and feature notebooks with PyAutoHands; regenerate catalogues.
- Validate syntax, executable AST and notebook code-cell parity, approved text/image identity, links, navigator, script size, whitespace and focused Sphinx build.
- No numerical or API changes. Prior CI is historical evidence, not fresh testing.

## Branch survey and coordination
Canonical PyAutoLens main has unrelated paper_jax/paper.md edit; autolens_workspace main has untracked dataset.fits. Use isolated worktrees from origin/main.
Branch: feature/stellar-dark-review.
Worktree: /home/jammy/Code/PyAutoLabs/.worktrees/stellar-dark-review
Reuse explicit same-session separate documentation worktree approval alongside magnification-maps-wiring.
Tier: judge — review PRs only; no merge.

## Approved preview
/mnt/c/Users/Jammy/Workspace/Science/scratch/stellar_dark_individual_review_20261112/v1/


Issue: https://github.com/PyAutoLabs/autolens_workspace/issues/638
Issued: 2026-11-12

Classifier API-risk/phasing heuristics overestimated this docs-only scope; inspection confirms no API or numerical change. Keep the approved two-PR scope.
