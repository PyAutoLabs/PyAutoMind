# Shapelets feature review
Repos: @autolens_workspace @PyAutoLens
Type: docs
Consequence: judge

## Original request
I like this. Apply the shapelets text and image to autolens_workspace, the main start_here.py and RTD. Keep the existing basis grid as a teaching figure. Open both PRs for review, don't merge yet.

## Coordination authorization
Yes, proceed with the shapelets changes in a separate documentation worktree alongside three-autos-public-framing. Open both PRs for review, don't merge yet.

## Plan
Apply the approved shapelets draft and minimal-text illustration. Lead with source science and preserve basis, solver, interpretation and fitting detail. Retain the existing basis grid as a teaching figure. Update main tour and RTD, correcting obsolete navigation. Generate notebooks/catalogues and validate before opening two linked review PRs. No merge.

## Detailed implementation
- scripts/imaging/features/advanced/shapelets/start_here.py: approved draft with repository-relative image references.
- start_here.py and docs/overview/overview_3_features.md: science-first Shapelets section, new illustration, existing basis grid retained below explanatory text.
- images/features/shapelets_illustration.png and shapelets_basis.png; RTD overview_3/shapelets_illustration.png and existing shapelets.png. Preserve the original grid byte-for-byte.
- Add image prompt/provenance; regenerate root and feature notebooks plus catalogues via PyAutoHands.
- Check syntax, unchanged executable AST/notebook code, approved text/image parity, local links, navigator/banner, search-memory, size, whitespace and focused Sphinx build.
- No API or numerical changes. Prior CI evidence distinguished from fresh documentation checks.

Branch: feature/shapelets-review
Worktree: /home/jammy/Code/PyAutoLabs/.worktrees/shapelets-review
Tier: judge — review PRs only; no merge.
Approved preview: /mnt/c/Users/Jammy/Workspace/Science/scratch/shapelets_individual_review_20261112/v1/


Issue: https://github.com/PyAutoLabs/autolens_workspace/issues/642
Issued: 2026-11-12
Classifier API/phasing heuristics overestimate the docs-only scope; inspection confirms no API/numerical change.

## Shipping checkpoint
Approved draft/illustration applied; original basis grid retained byte-for-byte. Changes staged, uncommitted.
Fresh checks passed: syntax; executable AST/notebook code-cell parity; approved draft and illustration identity; original basis grid preserved byte-for-byte; local image links; navigator/banner, search-memory, size and whitespace checks; focused Sphinx build with warnings treated as errors. No numerical/API changes. Full numerical/smoke suites were not rerun for this prose/assets-only delta; preceding double source-plane PRs passed all 12 CI jobs on the same base (prior evidence, not fresh testing).

Heart RED 2026-11-12T17:29:04.434775+00:00:
- PyAutoLens: on branch feature/shapelets-review (not main)
- PyAutoLens: 2 uncommitted source change(s)
- install verification FAILED (testpypi; checks F)
- release validation FAILED (stage integrate)

Await live development-only override for #642 before commit/push/open both review PRs. No merge.
Review: /mnt/c/Users/Jammy/Workspace/Science/scratch/shapelets_individual_review_20261112/applied/index.html
Logs/PR drafts: organs/PyAutoMind/tmp/shapelets_review/

## Development-only Heart RED override

Human authorization (2026-11-12): I approve the development-only Heart RED override for #642. Commit, push and open both PRs for review, don't merge yet.

Exact RED reasons (2026-11-12T17:29:04.434775+00:00):
- `PyAutoLens: on branch feature/shapelets-review (not main)`
- `PyAutoLens: 2 uncommitted source change(s)`
- `install verification FAILED (testpypi; checks F)`
- `release validation FAILED (stage integrate)`

Fresh checks passed: syntax; executable AST/notebook code-cell parity; approved draft and illustration identity; original basis grid preserved byte-for-byte; local image links; navigator/banner, search-memory, size and whitespace checks; focused Sphinx build with warnings treated as errors. No numerical/API changes. Full numerical/smoke suites were not rerun for this prose/assets-only delta; preceding double source-plane PRs passed all 12 CI jobs on the same base (prior evidence, not fresh testing).

Commit/push/PR-open only; no merge, release or CI bypass.

## Review PR handoff — 2026-11-12
- Workspace: https://github.com/PyAutoLabs/autolens_workspace/pull/643 — 21b58a4d8c4f9bd04a9d724bf93e65a78cb923ca
- RTD: https://github.com/PyAutoLabs/PyAutoLens/pull/835 — 083bba094e7a4fbc8cdfe546c65c69195e3d95d9
- Both committed and pushed under the approved #642 development-only override. Original basis grid preserved. Neither merged; CI not awaited. Next: human review, then separately authorized CI/freeze check and merge.
