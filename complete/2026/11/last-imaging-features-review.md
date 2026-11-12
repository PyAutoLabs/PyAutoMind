# Final imaging feature introductions and illustrations

Issue: https://github.com/PyAutoLabs/autolens_workspace/issues/654 (closed)

Merged 2026-11-12 under the live human merge command after all 12 exact-head CI jobs succeeded and Heart freeze returned `not frozen`. Library first:
- PyAutoLens #850 https://github.com/PyAutoLabs/PyAutoLens/pull/850; source a53bb4dbaf79470c50294419e1fb877ba28b7719; merge 7b143f2bc707ee41107e65807e4361d04e8e4c76.
- autolens_workspace #655 https://github.com/PyAutoLabs/autolens_workspace/pull/655; source 5726f9e04b8647b0952efd1abc8e8857b97e2955; merge 86ccafab6402395cf7e1c957c674732260e79f2c.
Both source branches proved ancestors of origin/main.

Applied approved scientific-use-case-first introductions for no_lens_light, advanced/sky_background and advanced/subhalo, preserving teaching detail. Two new images reused in feature introductions, main tour and RTD; the approved subhalo image reused unchanged. Four notebooks and navigation catalogues regenerated. The sky prior boundary is explained, not changed.

Validation: exact approved prose/image parity; executable AST and notebook code preservation; notebook schemas and image paths; focused Sphinx warnings-as-errors build; navigator, search-memory, size and whitespace checks; concurrent api-reference-polish and general-docs-refresh file scopes disjoint. Local numerical suites not repeated for documentation-only edits; all four library CI jobs and eight workspace CI jobs passed before merge.

Development-only Heart RED override recorded on issue, PRs, active entry and first autonomy_log table. Separate live merge authority used; no release/rehearsal or assertion Heart is healthy. No pending-release obligation in the task active entry.

Review bundle: C:\Users\Jammy\Workspace\Science\scratch\last_three_imaging_review_20261112\applied\
Task worktrees: /home/jammy/Code/PyAutoLabs/.worktrees/last-imaging-features-review (remove after close-out).
All 16 imaging feature introductions have now completed this individual text/image review cycle. Non-imaging variants remain a separate follow-up.

## Original prompt

# Last three imaging feature introductions

Issue: https://github.com/PyAutoLabs/autolens_workspace/issues/654
Issued: 2026-11-12
Consequence: judge
Repos: @autolens_workspace @PyAutoLens
Branch: feature/last-imaging-features-review

## Original request

I like these. Apply all three texts and images to autolens_workspace, the main start_here.py and RTD, reusing the subhalo image. Open both PRs for review, don't merge yet.

## Coordination

Live reply: "Allow separate documentation worktree" to coexist with api-reference-polish and general-docs-refresh. Preserve their files and verify compatibility.

## Plan

- Apply approved v1 No Lens Light, Sky Background and Subhalo parent introductions, adapting only local image paths.
- Add No Lens Light to main tour and RTD, replace the sky summary, and add an overview route to the existing dark-matter subhalo section without duplicating or replacing its approved detection image.
- Copy two approved images/provenance into both repos; reuse existing approved subhalo image byte-for-byte.
- Regenerate the three feature notebooks, root notebook and navigation catalogues through PyAutoHands.
- Validate exact approved prose/images, unchanged executable code, notebook schemas and links, navigation/search-memory/size/whitespace, focused Sphinx rendering and compatibility with concurrent tasks.
- Open paired review PRs, library first, behind Heart shipping gate; no merge.

Tier: judge — merge mode: human /prm.

## Detailed scope

Workspace: scripts/imaging/features/no_lens_light/start_here.py, advanced/sky_background/start_here.py and advanced/subhalo/start_here.py; root start_here.py; notebook counterparts; llms-full.txt/workspace_index.json; images/features/{no_lens_light,sky_background}.png plus provenance. Existing images/features/subhalo_detection_illustration.png is reused, not edited.
Library: docs/overview/overview_3_features.md and docs/overview/images/overview_3/ matching new image/provenance assets. Preserve existing subhalo illustration.
Approved input: /mnt/c/Users/Jammy/Workspace/Science/scratch/last_three_imaging_review_20261112/v1/.
No runtime/API/config/simulator changes, including the noted sky prior boundary. Local numerical suites not repeated for documentation-only changes; CI required before any later merge.
Clean worktrees rooted at /home/jammy/Code/PyAutoLabs/.worktrees/last-imaging-features-review. Preserve unrelated canonical paper_jax/paper.md, dataset.fits and other tasks' dirty Mind state.

Classification disposition: bounded documentation-only batch, no API changes. Generic classifier design/core-API phasing is inapplicable; keep the two user-approved paired documentation PRs.

## Implementation checkpoint
# Last imaging features #654

Applied, staged and validated. No source commits, pushes or PRs yet. Awaiting development-only Heart RED override for #654.

Passed: exact approved feature text and image parity; subhalo image reused unchanged; all four executable ASTs and notebook code cells preserved; notebook schemas and image paths; focused Sphinx build with warnings as errors; navigator, search-memory, size and staged whitespace checks. Concurrent api-reference-polish and general-docs-refresh scopes are disjoint. Full numerical suites were not rerun locally for this documentation-only change; required CI remains mandatory before a future merge.

Open index.html for complete feature previews and rtd/index.html for the built tour summaries. Repository patches and PR drafts are alongside them.

## Exact Heart RED reasons
- PyAutoNerves: 2 commit(s) behind origin
- PyAutoArray: 2 commit(s) behind origin
- PyAutoGalaxy: 10 commit(s) behind origin
- PyAutoLens: on branch feature/last-imaging-features-review (not main)
- PyAutoLens: 3 uncommitted source change(s)
- PyAutoCTI: 2 commit(s) behind origin
- install verification FAILED (testpypi; checks F)
- release validation FAILED (stage integrate)

## PRs opened

PyAutoLens RTD: https://github.com/PyAutoLabs/PyAutoLens/pull/850 (a53bb4dbaf79470c50294419e1fb877ba28b7719)
autolens_workspace: https://github.com/PyAutoLabs/autolens_workspace/pull/655 (5726f9e04b8647b0952efd1abc8e8857b97e2955)

Development-only Heart RED override for #654

Live authorization:
> I approve the development-only Heart RED override for #654. Commit, push and open both PRs for review, don't merge yet.

Exact RED reasons:
- PyAutoNerves: 2 commit(s) behind origin
- PyAutoArray: 2 commit(s) behind origin
- PyAutoGalaxy: 10 commit(s) behind origin
- PyAutoLens: on branch feature/last-imaging-features-review (not main)
- PyAutoLens: 3 uncommitted source change(s)
- PyAutoCTI: 2 commit(s) behind origin
- install verification FAILED (testpypi; checks F)
- release validation FAILED (stage integrate)

Passed: exact approved feature text and image parity; subhalo image reused unchanged; all four executable ASTs and notebook code cells preserved; notebook schemas and image paths; focused Sphinx build with warnings as errors; navigator, search-memory, size and staged whitespace checks. Concurrent api-reference-polish and general-docs-refresh scopes are disjoint. Full numerical suites were not rerun locally for this documentation-only change; required CI remains mandatory before a future merge.

Commit/push/review PRs only. No merge or release authority.
