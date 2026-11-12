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

## Shipping checkpoint
Approved v2 image and text applied; source changes staged, uncommitted.
Fresh checks: syntax; unchanged executable AST and notebook code cells; approved draft parity except image path/trailing whitespace; identical approved images and valid local links; navigator/banner, search-memory, size and whitespace checks; focused Sphinx build with warnings treated as errors. No numerical/API changes. Full numerical/smoke suites were not rerun for this prose/assets-only delta; preceding stellar + dark matter PRs passed all 12 CI jobs on the same base, which is prior evidence rather than fresh testing.

Heart RED 2026-11-12T17:09:03.637477+00:00:
- PyAutoLens: on branch feature/double-source-plane-review (not main)
- PyAutoLens: 2 uncommitted source change(s)
- install verification FAILED (testpypi; checks F)
- release validation FAILED (stage integrate)

Await development-only Heart RED override for #640 before commit/push/open both review PRs. No merge.
Review: /mnt/c/Users/Jammy/Workspace/Science/scratch/double_source_plane_individual_review_20261112/applied/index.html
Logs and PR drafts: organs/PyAutoMind/tmp/double_source_plane_review/

## Development-only Heart RED override

Human authorization (2026-11-12): I approve the development-only Heart RED override for #640. Commit, push and open both PRs for review, don't merge yet.

Exact RED reasons (2026-11-12T17:09:03.637477+00:00):
- `PyAutoLens: on branch feature/double-source-plane-review (not main)`
- `PyAutoLens: 2 uncommitted source change(s)`
- `install verification FAILED (testpypi; checks F)`
- `release validation FAILED (stage integrate)`

Fresh checks: syntax; unchanged executable AST and notebook code cells; approved draft parity except image path/trailing whitespace; identical approved images and valid local links; navigator/banner, search-memory, size and whitespace checks; focused Sphinx build with warnings treated as errors. No numerical/API changes. Full numerical/smoke suites were not rerun for this prose/assets-only delta; preceding stellar + dark matter PRs passed all 12 CI jobs on the same base, which is prior evidence rather than fresh testing.

Commit/push/PR-open only; no merge, release or CI bypass.

## Review PR handoff — 2026-11-12
- Workspace: https://github.com/PyAutoLabs/autolens_workspace/pull/641 — 5b01fd28f3dd9e3849f2f4af58a2979cb3e873f2
- RTD: https://github.com/PyAutoLabs/PyAutoLens/pull/831 — bd51344d88dbc07d3c41807950d61c99c4da48d0
- Both committed and pushed under the approved #640 development-only override. Open for human review; neither merged. CI not awaited. Next: human review, then separately authorized CI/freeze check and merge.
