# Three feature introductions and illustrations

Issue: https://github.com/PyAutoLabs/autolens_workspace/issues/652
Issued: 2026-11-12
Consequence: judge
Repos: @autolens_workspace @PyAutoLens
Branch: feature/three-feature-review

## Original request

This is better. Apply all three features' text and images to autolens_workspace, the main start_here.py and RTD, using the revised operated image. Open both PRs for review, don't merge yet.

## Coordination approval

Yes, proceed with all three features in a separate documentation worktree alongside both tasks. Preserve their changes and check compatibility. Open both PRs for review, don't merge yet.

## Plan

- Apply approved v2 bundle introductions for linear_light_profiles, scaling_relation and advanced/operated_light_profile. Use the revised operated PSF image; linear profiles emphasize solved rather than sampled intensity.
- Add linear/scaling summaries and replace operated summary in main workspace start_here.py and RTD overview_3_features.md; reuse identical images with provenance.
- Regenerate four affected notebooks and catalogue files through PyAutoHands.
- Check approved text/image parity, executable AST/notebook code preservation, links/schemas, navigator/search-memory/size/whitespace, focused Sphinx render, and scratch merge compatibility with start-here-plot-ai. Installation docs use separate files; preserve them.
- Open paired review PRs, library first, behind Heart shipping gate. Do not merge.

Tier: judge — merge mode: human /prm.

## Details

Primary autolens_workspace: three feature start_here.py files under scripts/imaging/features, root start_here.py, their generated notebooks, llms-full.txt/workspace_index.json, images/features/{linear_light_profiles,scaling_relation,operated_light_profile}.png and provenance.
Companion PyAutoLens: docs/overview/overview_3_features.md and docs/overview/images/overview_3/ matching PNG/provenance files. No API/runtime/simulator/config changes. Numerical suites not rerun locally for documentation-only scope; disclose, and require CI before any future merge.
Approved input /mnt/c/Users/Jammy/Workspace/Science/scratch/three_feature_review_20261112/v2/; adapt only relative image paths.
Clean task worktrees from origin/main. Preserve canonical unrelated paper_jax/paper.md and dataset.fits. User approves coexistence with installation-docs-polish and start-here-plot-ai; do not edit their worktrees. Heart entry YELLOW permits development.

## Implementation checkpoint

# Three-feature review #652

Implemented and staged; no source commits, pushes or PRs yet. Awaiting development-only Heart RED override.

Passed: exact approved feature text and image parity; unchanged executable AST and notebook code cells for all four scripts/notebooks; notebook schemas and local image links; focused Sphinx build with warnings as errors; navigator, search-memory, size and staged whitespace checks. Clean three-way merge of root script/notebook with start-here-plot-ai; installation-docs-polish touches disjoint files. Numerical suites were not rerun locally for this prose/image-only change.

Open index.html for approved feature previews and rtd/index.html for the built tour summaries. Repository patches and drafted PR bodies are alongside them. Feature preview image paths remain local for viewing; applied repository paths were validated separately.

## Exact Heart RED reasons
- PyAutoNerves: 2 commit(s) behind origin
- PyAutoArray: 2 commit(s) behind origin
- PyAutoGalaxy: 6 commit(s) behind origin
- PyAutoLens: on branch feature/three-feature-review (not main)
- PyAutoLens: 4 uncommitted source change(s)
- PyAutoCTI: 2 commit(s) behind origin
- install verification FAILED (testpypi; checks F)
- release validation FAILED (stage integrate)

Bounded documentation-only combined task: the classifier generic large-task phasing is unnecessary; no API or runtime changes and the approved deliverable is two paired PRs.

## PRs opened

PyAutoLens RTD: https://github.com/PyAutoLabs/PyAutoLens/pull/845 (e1bcc2d4a677c9b3f2f9f7f18531a90fc6b78b70)
autolens_workspace: https://github.com/PyAutoLabs/autolens_workspace/pull/653 (25ef2779caa5c57e8dafc7dddb6d8e2ac712d848)

Development-only Heart RED override for #652

Live authorization:
> I approve the development-only Heart RED override for #652. Commit, push and open both PRs for review, don't merge yet.

Exact RED reasons:
- PyAutoNerves: 2 commit(s) behind origin
- PyAutoArray: 2 commit(s) behind origin
- PyAutoGalaxy: 6 commit(s) behind origin
- PyAutoLens: on branch feature/three-feature-review (not main)
- PyAutoLens: 4 uncommitted source change(s)
- PyAutoCTI: 2 commit(s) behind origin
- install verification FAILED (testpypi; checks F)
- release validation FAILED (stage integrate)

Passed: exact approved feature text and image parity; unchanged executable AST and notebook code cells for all four scripts/notebooks; notebook schemas and local image links; focused Sphinx build with warnings as errors; navigator, search-memory, size and staged whitespace checks. Clean three-way merge of root script/notebook with start-here-plot-ai; installation-docs-polish touches disjoint files. Numerical suites were not rerun locally for this prose/image-only change.

Commit/push/review PRs only. No merge or release authority.
