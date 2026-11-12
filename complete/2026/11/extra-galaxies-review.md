# Extra Galaxies feature review

Completed: 2026-11-12
Issue: https://github.com/PyAutoLabs/autolens_workspace/issues/648 (closed)

Approved two-panel Extra Galaxies illustration and science-first introduction merged into the feature, main workspace tour and RTD. Teaching retained on separate light/mass decisions, noise scaling, centres, component inspection, SLaM and larger lens systems. No runtime/API/configuration changes. Both concurrent tasks preserved; scratch merge compatibility verified.

## Merge receipts

- PyAutoLens#840: https://github.com/PyAutoLabs/PyAutoLens/pull/840 — merge e4051fe31055345f01f0590b4a8055dc20000c7e; tested head c0db3b63462c0afedc6c36e4169bcdbba7cf69ee.
- autolens_workspace#650: https://github.com/PyAutoLabs/autolens_workspace/pull/650 — merge 42a5be1dcbf8574a7cfef2300f3a1fe07f181046; tested head 2673459bd5b022a0763395552f305f5db18f1601.
- All 12 exact-head CI jobs passed (4 library, 8 workspace), no pending/skipped jobs. Both merge states CLEAN. Heart freeze not frozen. Live human separately authorized conditional merge; library merged first. No release performed.
- Source branch HEADs proven ancestors of fetched origin/main.

## Validation

Approved prose/image parity, executable AST/notebook code-cell parity, image references, PyAutoHands generation, navigation/banner/search-memory/size/whitespace checks and focused Sphinx build -W passed. Numerical CI and smoke passed before merge. Development-only Heart RED override remains recorded in original prompt, issue, both PRs and autonomy log; no assertion of release readiness.

Review bundle: /mnt/c/Users/Jammy/Workspace/Science/scratch/extra_galaxies_individual_review_20261112/applied/index.html

## Original prompt

# Extra Galaxies feature review

Issue: https://github.com/PyAutoLabs/autolens_workspace/issues/648
Issued: 2026-11-12
Consequence: judge
Repos: @autolens_workspace @PyAutoLens
Branch: feature/extra-galaxies-review

## Original request

This is better. Apply the revised Extra Galaxies image and text to autolens_workspace, the main start_here.py and RTD. Open both PRs for review, don't merge yet.

## Coordination approval

Yes, proceed with extra_galaxies in a separate documentation worktree alongside both tasks. Preserve their changes and check merge compatibility. Open both PRs for review, don't merge yet.

## Plan

- Apply approved feature text and v2 image titled Extra Galaxies, preserving scientific use cases and teaching detail.
- Add an Extra Galaxies overview beside the group section in the root workspace tour and RTD feature page, using identical assets.
- Regenerate affected notebooks and catalogues with PyAutoHands.
- Validate approved prose/image parity, executable AST and notebook code-cell invariance, image references, notebook schemas, focused Sphinx render, navigation/search-memory/size/whitespace checks.
- Check compatibility with new-user-guide-visuals and start-here-plot-ai without editing their worktrees.
- Open paired PRs, library first, behind the Heart gate. Do not merge.

Tier: judge — merge mode: human /prm.

## Detailed scope

Primary autolens_workspace: scripts/imaging/features/extra_galaxies/start_here.py, root start_here.py, notebook counterparts, generated catalogue files, images/features/extra_galaxies.png and provenance.
PyAutoLens: docs/overview/overview_3_features.md, docs/overview/images/overview_3/extra_galaxies.png and provenance.
Approved input: /mnt/c/Users/Jammy/Workspace/Science/scratch/extra_galaxies_individual_review_20261112/v2/.
Adapt only the feature's relative image path. No changes to simulators, runtime, APIs, configuration or dataset-level introductions. Numerical suites not rerun for prose-only scope; required CI gates any future merge.

## Survey

Clean separate worktrees from origin/main. Canonical PyAutoLens main is behind with unrelated paper_jax/paper.md edits; canonical workspace main behind with untracked dataset.fits; preserved. User explicitly authorizes coexistence with new-user-guide-visuals (both repos) and start-here-plot-ai (workspace). Their in-progress changes will be checked via patch compatibility. Heart entry YELLOW permits development; shipping gate remains separate.

Brain classification combined library/workspace accepted. Generic large/API-risk phased recommendation is inapplicable to this bounded approved prose/image-only task; no API changes.

## Applied checkpoint — 2026-11-12

Approved v2 Extra Galaxies title/image and approved feature text applied, adapting only the image path. Root tour and RTD add the corresponding overview before Groups. Source changes staged, not committed; no PRs yet.

Validation passes: exact approved prose/image parity, executable AST and notebook code-cell parity, image links, PyAutoHands notebook/catalogue generation, navigator/banner/search-memory/size/whitespace checks, focused Sphinx build -W. Both concurrent tasks combine cleanly in scratch three-way merges of root script and notebook. No changes to their worktrees. No local numerical suite/simulation smoke rerun for prose-only scope; CI remains required.

Review: /mnt/c/Users/Jammy/Workspace/Science/scratch/extra_galaxies_individual_review_20261112/applied/index.html
Logs/PR bodies: organs/PyAutoMind/tmp/extra_galaxies_review/.
User steered with $prm during implementation. No PR exists to merge yet; shipping needs its live task-specific Heart override first. No merge performed.

Heart RED at 2026-11-12T18:29:55.724424+00:00:
- PyAutoNerves: 2 commit(s) behind origin
- PyAutoArray: 2 commit(s) behind origin
- PyAutoGalaxy: 4 commit(s) behind origin
- PyAutoLens: on branch feature/extra-galaxies-review (not main)
- PyAutoLens: 2 uncommitted source change(s)
- PyAutoCTI: 2 commit(s) behind origin
- install verification FAILED (testpypi; checks F)
- release validation FAILED (stage integrate)

Awaiting development-only Heart RED override for #648 before source commit/push/PR-open.

## Development-only Heart RED override

Live user authorization:
> I approve the development-only Heart RED override for #648. Commit, push and open both PRs for review, don't merge yet.

Exact Heart RED reasons (2026-11-12T18:29:55.724424+00:00):
- PyAutoNerves: 2 commit(s) behind origin
- PyAutoArray: 2 commit(s) behind origin
- PyAutoGalaxy: 4 commit(s) behind origin
- PyAutoLens: on branch feature/extra-galaxies-review (not main)
- PyAutoLens: 2 uncommitted source change(s)
- PyAutoCTI: 2 commit(s) behind origin
- install verification FAILED (testpypi; checks F)
- release validation FAILED (stage integrate)

Approved prose/image parity, executable AST/notebook code-cell parity, image links, generation, navigator/banner/search-memory/size/whitespace checks and focused Sphinx build passed. Both concurrent tasks combine cleanly in scratch merges. Human text/image review approved. Numerical suites and simulation smoke not rerun for docs-only scope; CI still required before merge.

Commit, push and PR-open only. No merge or release.

## PR-open checkpoint — 2026-11-12

RTD: https://github.com/PyAutoLabs/PyAutoLens/pull/840 — c0db3b63462c0afedc6c36e4169bcdbba7cf69ee.
Workspace: https://github.com/PyAutoLabs/autolens_workspace/pull/650 — 2673459bd5b022a0763395552f305f5db18f1601.
Both open for human review; no merge/release performed. Latest user explicitly said do not merge, superseding earlier $prm steering. Source worktrees clean and pushed. Override recorded in issue, PR bodies, active.md and autonomy log. CI not yet declared green.
