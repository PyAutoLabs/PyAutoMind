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
