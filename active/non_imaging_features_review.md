# Non-imaging feature introductions and image reuse

Issue: https://github.com/PyAutoLabs/autolens_workspace/issues/656
Issued: 2026-11-12
Consequence: judge
Difficulty: medium
Lane: local-dev

@autolens_workspace @PyAutoLens

## Original request

I like these. Apply all 51 texts and the images to autolens_workspace, the main start_here.py and RTD, reusing the approved images as proposed. Open both PRs for review, don't merge yet.

## Approved scope

Apply the approved 2026-11-12 preview: all 51 non-imaging feature introductions, scientific use cases first with teaching detail retained. Reuse the approved feature images and RTD lens-scales/dataset-types assets unchanged; add the approved Group Halo, Deblending and Strong + Weak Lensing illustrations. Keep executable code unchanged. Update workspace root start_here.py and RTD overview with scientific routing and feature links, preserving recent introductory changes. Regenerate corresponding notebooks and navigation. No merges or releases.

Preview: /mnt/c/Users/Jammy/Workspace/Science/scratch/non_imaging_feature_review_20261112/

## Plan

1. Compare the 51 approved source snapshots against current main and preserve concurrent edits.
2. Apply prose and image links in scripts/{group,interferometer,multi_dataset,multi_galaxy,point_source,weak}/features/**/start_here.py.
3. Reuse existing images; add only the three approved new assets and their prompts. Link scale/dataset diagrams to the existing new-user-guide assets.
4. Update root start_here.py and PyAutoLens/docs/overview/overview_3_features.md, with domain-specific feature links and three new illustrations. Retain all existing teaching figures.
5. Regenerate 52 notebooks and navigator using PyAutoHands. Validate AST/code-cell preservation, notebook schemas, links, image identity, size guard and Sphinx render.
6. Check current Heart readiness; open paired review PRs, library documentation first. No merge.

Tier: judge — merge mode: human /prm

## Branch survey

Canonical PyAutoLens: main, unrelated modified paper_jax/paper.md.
Canonical autolens_workspace: main, unrelated untracked dataset.fits.
Canonical PyAutoMind: main, unrelated lifecycle edits; use isolated Mind worktree.
Current origin/main active registry has no claims on either target repository. Local guard clear; old unregistered feature worktrees are left untouched.
Worktree: /home/jammy/Code/PyAutoLabs/.worktrees/non-imaging-features-review
Branch: feature/non-imaging-features-review

## Implementation checkpoint
# Non-imaging feature review #656

Applied, staged and validated; no source commits, pushes or PRs yet. Awaiting live development-only Heart RED override for #656.

52 scripts preserve executable ASTs; 52 regenerated notebooks validate and preserve executable code (one approved commented sensitivity-sketch explanation changed); 267 notebook links resolve; 51 approved drafts and images match; all 51 linked from both overviews; Sphinx full feature-page build passes with warnings as errors; navigator, search-memory, size guard and staged whitespace checks pass. Existing root pixelization-overview link is missing on the base branch and remains unchanged. Numerical suites were not rerun for documentation-only changes; required CI remains mandatory before merge.

Worktree: /home/jammy/Code/PyAutoLabs/.worktrees/non-imaging-features-review
Branch: feature/non-imaging-features-review

## Exact Heart RED reasons
- PyAutoNerves: 2 commit(s) behind origin
- PyAutoArray: 2 commit(s) behind origin
- PyAutoGalaxy: 14 commit(s) behind origin
- PyAutoLens: on branch feature/non-imaging-features-review (not main)
- PyAutoLens: 4 uncommitted source change(s)
- PyAutoCTI: 2 commit(s) behind origin
- install verification FAILED (testpypi; checks F)
- release validation FAILED (stage integrate)

Next: after task-specific approval, record the override in all four required sinks and commit/push/open PyAutoLens PR first, then workspace PR. Do not merge.

## Development-only Heart RED override

Live user authorization: "Approve development-only override for #656", in reply to the task-specific request to commit, push and open both PRs for review, with no merge or release.

Exact RED reasons:
- PyAutoNerves: 2 commit(s) behind origin
- PyAutoArray: 2 commit(s) behind origin
- PyAutoGalaxy: 14 commit(s) behind origin
- PyAutoLens: on branch feature/non-imaging-features-review (not main)
- PyAutoLens: 4 uncommitted source change(s)
- PyAutoCTI: 2 commit(s) behind origin
- install verification FAILED (testpypi; checks F)
- release validation FAILED (stage integrate)

Passed branch checks: 52 script ASTs and notebook executable code preserved; 52 notebook schemas valid; 267 notebook links resolve; approved text/image parity; full feature-page Sphinx build with warnings as errors, navigator, search-memory, size and whitespace checks pass. Numerical suites not rerun for documentation-only scope; required CI remains mandatory. Human approved the previews and implementation.

No release, merge or CI bypass authorized.

## PR-open checkpoint
- Library PR: https://github.com/PyAutoLabs/PyAutoLens/pull/851
- Workspace PR: https://github.com/PyAutoLabs/autolens_workspace/pull/657
- Library head: a18b5f00bfc79d838a539c966b7d2b40ec9e3c94
- Workspace head: b01dfe87807cec5c2212fe597612968c99671134
- Status: both open for review, no merge or release; development-only Heart RED override recorded in issue, PR bodies, active registry and first autonomy-log table.
- Next: human review; on a separate explicit merge request, check exact-head CI and release freeze. Do not auto-merge or poll beyond this deliverable.
