# Installation docs polish

Issue: https://github.com/PyAutoLabs/PyAutoLens/issues/841
Status: human-review; applied in worktrees, no PRs authorized.

## User request

> Looks good, apply these Installation updates to both PyAutoLens and PyAutoGalaxy RTD, preserving existing links and anchors. Don't raise PRs yet.

## Approved implementation

Applied reviewed v1 drafts to both docs/installation trees, adding shared workspace and acceleration pages. Retained all old page URLs and rendered IDs/anchors, using aliases for renamed headings and short onward links for moved content. Kept Galaxy Numba compatibility page and added missing Lens page. Updated only Installation navigation in docs/index.md.

Worktree: /home/jammy/Code/PyAutoLabs/.worktrees/installation-docs-polish
Repositories: PyAutoLens and PyAutoGalaxy, both feature/installation-docs-polish.

Validation: focused Sphinx builds with warnings as errors passed for both; before/after rendered-ID comparisons passed; diff whitespace checks passed. No fresh cross-platform install or numerical tests claimed. No runtime/API changes.

Preview: /mnt/c/Users/Jammy/Workspace/Science/scratch/installation_review_20261112/applied/index.html
Validation logs and baseline IDs: worktree validation/<repo>/{before,after}/build.log and old_ids.json.
Original review notes and limitations: scratch/installation_review_20261112/v1/index.html in the human scratch folder.

Heart entry: YELLOW, Release YELLOW; monitoring RED, 16/100, 165 unresolved. No shipping/merge override inferred. Next: human review; no PRs until requested.

## Heart RED development override — #841

> Yes, override Heart RED for #841 and go ahead with the commits, pushes and both Installation PRs for PyAutoLens and PyAutoGalaxy. Don't merge yet.

Current RED reasons:
- PyAutoNerves: 2 commit(s) behind origin
- PyAutoArray: 2 commit(s) behind origin
- PyAutoGalaxy: 4 commit(s) behind origin
- PyAutoLens: on branch feature/extra-galaxies-review (not main)
- PyAutoLens: 2 uncommitted source change(s)
- PyAutoCTI: 2 commit(s) behind origin
- install verification FAILED (testpypi; checks F)
- release validation FAILED (stage integrate)

Validation: Focused Sphinx builds with warnings as errors passed; all old rendered anchors retained; 420 local links/fragments passed with no duplicate IDs; git diff whitespace checks passed; human review approved. Documentation only; no runtime changes. Fresh multi-platform installs and numerical suites not run locally.

Authorized: commits, pushes and two PRs. No merge or release.

## PR-open checkpoint

- https://github.com/PyAutoLabs/PyAutoLens/pull/842
- https://github.com/PyAutoLabs/PyAutoGalaxy/pull/706

Both commits pushed; PR file scope and pending-release labels verified. No merge performed. Prior no-PR checkpoint superseded by live user shipping authorization above. Await separate review/merge instruction.
