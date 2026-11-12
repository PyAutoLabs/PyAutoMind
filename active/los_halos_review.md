# Line-of-sight halo feature review

Issue: https://github.com/PyAutoLabs/autolens_workspace/issues/645
Issued: 2026-11-12
Consequence: judge
Repos: @autolens_workspace @PyAutoLens
Branch: feature/los-halos-review

## Original request

This is better. Apply the revised los_halos image and text to autolens_workspace, the main start_here.py and RTD. Open both PRs for review, don't merge yet.

## Coordination approval

Yes, proceed with los_halos in a separate documentation worktree alongside start-here-intro-polish. Preserve those introduction changes and open both PRs for review, don't merge yet.

## Plan

- Apply the approved scientific-use-cases-first introduction, preserving teaching detail and simulator-only scope.
- Reuse the approved two-panel population image in the feature, main workspace tour and RTD feature overview.
- Regenerate affected notebooks and navigation catalogues through PyAutoHands.
- Validate exact approved prose/image parity, unchanged executable code, links, focused Sphinx rendering and preservation of the other task's introduction edits.
- Open paired documentation PRs, library first, behind the Heart shipping gate. Do not merge.

Tier: judge — merge mode: human /prm.

## Detailed implementation

Primary: autolens_workspace. Companion: PyAutoLens documentation only.
Feature: scripts/imaging/features/advanced/los_halos/start_here.py.
Tours: autolens_workspace/start_here.py and PyAutoLens/docs/overview/overview_3_features.md.
Assets: images/features/los_halos.png and docs/overview/images/overview_3/los_halos.png, matching provenance files.
Generate root start_here.ipynb and notebooks/imaging/features/advanced/los_halos/start_here.ipynb plus navigation markdown/catalogues.
No simulator, runtime, configuration or API changes. No dataset-level start_here files.
Approved input: /mnt/c/Users/Jammy/Workspace/Science/scratch/los_halos_individual_review_20261112/v2/.
Concurrent start-here-intro-polish edits root opening prose and RTD overview_1_start_here.md; do not copy old introductions over its changes. Keep this PR's root change confined to the feature tour and test merge compatibility.
Validation: Python syntax, stripped executable AST and notebook code-cell equality, approved text match, SHA256 image identity, local image paths, focused Sphinx build, navigation/search-memory and file-size checks, diff whitespace. Numerical suites not rerun for documentation-only changes; disclose this in PRs.

## Branch survey

Canonical PyAutoLens main is behind origin/main and has unrelated paper_jax/paper.md edits; canonical autolens_workspace main is behind and has untracked dataset.fits. Both preserved. Separate clean worktrees created from origin/main with user-approved coordination alongside start-here-intro-polish. Mind state uses an isolated worktree.

Feature routing classified combined library/workspace. Generic large/API-risk phasing is not applicable: this is the approved two-repo prose/image-only task with no API changes.

## Applied checkpoint — 2026-11-12

- Approved v2 image and v1/v2 text applied exactly, adapting the feature image path only. Main tour and RTD add a population-focused LOS section beside subhalo detection.
- Source changes staged and uncommitted: 8 workspace files, 3 RTD files. No runtime/config/simulator edits.
- start-here-intro-polish merged during work; both task branches fast-forwarded to latest main (Lens 2947020d0; workspace 60b3bf51). Task patches restored cleanly and notebooks regenerated. Workspace opening through Features is byte-identical to main; RTD overview_1 untouched.
- PASS: syntax; stripped executable AST/notebook code-cell parity; notebook schemas; exact approved feature prose; SHA256 image parity; local image paths; navigator/banner and search-memory checks; size check; staged diff whitespace; focused Sphinx feature-section build with -W.
- Full API docs/numerical suites/simulation smoke not rerun for prose-only changes. No new API. Disclosed in prepared PR bodies.
- Review: /mnt/c/Users/Jammy/Workspace/Science/scratch/los_halos_individual_review_20261112/applied/index.html
- Internal logs and PR bodies: organs/PyAutoMind/tmp/los_halos_review/.
- Next: current Heart shipping gate, then commit/push and open both PRs only on permitted verdict or live task-specific override. No merge authorized.

Heart gate: RED at 2026-11-12T18:07:53.810744+00:00. Exact reasons:
- PyAutoNerves: 2 commit(s) behind origin
- PyAutoArray: 2 commit(s) behind origin
- PyAutoGalaxy: 4 commit(s) behind origin
- PyAutoLens: on branch feature/los-halos-review (not main)
- PyAutoLens: 2 uncommitted source change(s)
- PyAutoCTI: 2 commit(s) behind origin
- install verification FAILED (testpypi; checks F)
- release validation FAILED (stage integrate)

Await live development-only override for #645. No source commit/push or PR yet.
