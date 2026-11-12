# Double source-plane lens feature review
Repos: @autolens_workspace @PyAutoLens
Type: docs
Consequence: judge

## Original request
This is better. Apply the revised image and double source-plane lens text to autolens_workspace, the main start_here.py and RTD. Open both PRs for review, don't merge yet.

## Plan
Apply approved text and v2 simplified image titled double_source_plane_lens. Lead with cosmic geometry, mass structure and source science while retaining multi-plane geometry, inference limitations and staged fitting teaching. Add matching main-tour and RTD sections. Generate notebooks/catalogues and validate; open two linked PRs, no merge.

## Detailed implementation
- scripts/imaging/features/advanced/double_source_plane_lens/start_here.py: approved draft with repository-relative image link.
- start_here.py and docs/overview/overview_3_features.md: dedicated Double Source-Plane Lenses section before Automated Pipelines / SLaM.
- images/features/double_source_plane_illustration.png and RTD overview_3 counterpart: identical approved image plus provenance/prompt.
- PyAutoHands regenerates root and feature notebooks and catalogues.
- Validate syntax, executable AST/notebook code parity, approved text/image identity, links, navigator/banner checks, search-memory, size/whitespace and focused Sphinx build.
- No API or numerical changes; distinguish fresh documentation validation from prior numerical CI.

## Branch survey
Canonical PyAutoLens main has unrelated paper_jax/paper.md edit; workspace main has untracked dataset.fits. No active conflicting claims. Separate worktrees from origin/main.
Branch: feature/double-source-plane-review
Worktree: /home/jammy/Code/PyAutoLabs/.worktrees/double-source-plane-review
Tier: judge — review PRs only, no merge.

## Approved preview
/mnt/c/Users/Jammy/Workspace/Science/scratch/double_source_plane_individual_review_20261112/v2/


Issue: https://github.com/PyAutoLabs/autolens_workspace/issues/640
Issued: 2026-11-12

Classifier API/phasing heuristic overestimates this prose/assets-only scope; inspection confirms no numerical or API change.
