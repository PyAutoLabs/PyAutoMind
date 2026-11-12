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
