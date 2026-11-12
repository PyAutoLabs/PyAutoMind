# API Reference polish

Completed: 2026-11-12
Issue: https://github.com/PyAutoLabs/PyAutoLens/issues/846
Consequence: judge

## Merged scope
Six API category pages: docs/api/galaxy.rst, pixelization.rst and plot.rst in both libraries. Corrected construction/plotting guidance and clarified galaxies, collections, ray tracing, fields and redshifts while preserving scientific detail, URLs and anchors. No runtime changes.

## Merge receipts
- PyAutoLens: https://github.com/PyAutoLabs/PyAutoLens/pull/849 — head 9a1266dec6558f2b382be2f61405117aff9e1a77; merge 64e5f8a759de51642f996cda11b21e374600a2e4
- PyAutoGalaxy: https://github.com/PyAutoLabs/PyAutoGalaxy/pull/709 — head 28dfe2d5d7ce1fd12e4402417bd79dbfabeb1e10; merge 98f1091fc0ee2948bfd0e73227ab60bfe47f4fe0
- pending-release: PyAutoLens@https://github.com/PyAutoLabs/PyAutoLens/pull/849
- pending-release: PyAutoGalaxy@https://github.com/PyAutoLabs/PyAutoGalaxy/pull/709

## Validation
Each exact head: 2 successful workflows and 4 successful jobs (Docs, Python 3.12, Python 3.13, no-JAX). Both CLEAN, freeze clear. No existing reviews/threads and no actionable findings from in-session review. Both head commits proved ancestors of origin/main.
All 97 API entries and 29 section anchors retained; 150 links and 10 Python example blocks passed. Exact six-file scope; committed inputs match validated builds.
Full local Sphinx renders complete, but strict -W builds retain identical existing diagnostics: Lens 97; Galaxy 69. No new diagnostics or suppression; no claim of clean strict builds.

## Authorization and follow-up
Live human authorized Heart RED development shipping for #846, then separately authorized merging on green CI and clean review. Recorded in all four override sinks. No release, force merge or CI bypass. No workspace migration needed. Existing inherited-docstring diagnostics remain outside scope.
Human preview evidence: /mnt/c/Users/Jammy/Workspace/Science/scratch/api_rtd_review_20261112/
CI receipts: /home/jammy/Code/PyAutoLabs/scratch/api-reference-polish/merge/

## Original prompt

# API Reference polish

Type: docs
Consequence: judge
Targets: @PyAutoLens @PyAutoGalaxy

## Original request
Looks good, apply these six drafts to the PyAutoLens and PyAutoGalaxy RTD, preserving existing links and anchors. Check the documentation builds, but don't raise PRs yet.

## Approved scope
Apply previews_v1 from /mnt/c/Users/Jammy/Workspace/Science/scratch/api_rtd_review_20261112/ to docs/api/pixelization.rst, plot.rst and galaxy.rst in both libraries. Preserve all 97 API entries and existing URLs/anchors. No source docstring edits or other documentation sections. Build documentation and record baseline failures separately. No PR, merge or release.

## Plan
Create isolated feature/api-reference-polish worktrees from origin/main. Apply the six reviewed RST files after checking drift. Compare old/new rendered page anchors and outgoing API destinations; add compatibility anchors as needed. Run Sphinx builds and focused checks. Save readable built pages and validation evidence in Science/scratch. Leave library changes uncommitted for review.

Issue: https://github.com/PyAutoLabs/PyAutoLens/issues/846
Issued: 2026-11-12

## Application checkpoint
Applied the six approved files in .worktrees/api-reference-polish on feature/api-reference-polish in each library. Whitespace-only cleanup relative to previews_v1. No source drift at application; no changes outside the three API RST files per repo.
All 97 API entries retained. All 29 original rendered section IDs retained. All 150 checked local links and fragments resolve. All 10 Python example blocks execute against the worktree imports with Agg plotting and a supplied Array2D; no fits performed.
Full Sphinx HTML builds use the real configuration and autodoc in an isolated Python 3.12 environment. Baseline diagnostics: Lens 97, Galaxy 69; comparison shows no new diagnostics. Strict warning-as-error builds are not clean due to existing inherited-docstring and other documentation diagnostics. Final build receipt: scratch/api-reference-polish/build_results.json; human review pages and validation: /mnt/c/Users/Jammy/Workspace/Science/scratch/api_rtd_review_20261112/applied/.
No library commits, pushes or PRs. Mind sync remains local because prompt_sync_push refused unrelated pending files owned by other chats; do not include them in this task's commit.

## Development-only Heart RED override

Human authorization for #846:

> Yes, authorize the development-only Heart RED override for #846. Commit, push and open both PRs, noting the existing documentation warnings. Don't merge yet.

Heart snapshot: 2026-11-12T19:30:21.264922+00:00; verdict RED.

- `PyAutoNerves: 2 commit(s) behind origin`
- `PyAutoArray: 2 commit(s) behind origin`
- `PyAutoGalaxy: 10 commit(s) behind origin`
- `PyAutoLens: on branch feature/last-imaging-features-review (not main)`
- `PyAutoLens: 3 uncommitted source change(s)`
- `PyAutoCTI: 2 commit(s) behind origin`
- `install verification FAILED (testpypi; checks F)`
- `release validation FAILED (stage integrate)`

Validation: All 97 API entries and 29 original section anchors retained; 150 local links/fragments pass; 10 Python example blocks execute; exact six-file scope and git diff --check pass; human review approved. Full Sphinx renders: Lens 97 and Galaxy 69 diagnostics, identical to baseline; strict -W builds remain nonzero for existing diagnostics. No runtime changes; numerical suites and workspace science runs are not applicable to this documentation-only scope.

Commit, push and PR creation only. No merge, release, CI bypass or claim that this change repairs Heart.

## PR-open checkpoint
- PyAutoLens: https://github.com/PyAutoLabs/PyAutoLens/pull/849 — 9a1266dec6558f2b382be2f61405117aff9e1a77
- PyAutoGalaxy: https://github.com/PyAutoLabs/PyAutoGalaxy/pull/709 — 28dfe2d5d7ce1fd12e4402417bd79dbfabeb1e10
Both open, labelled pending-release, unmerged. Descriptions explicitly record unchanged baseline Sphinx diagnostics (Lens 97; Galaxy 69) and the authorized Heart RED override. No workspace migration is needed. CI is not bypassed and no waiter is armed.
