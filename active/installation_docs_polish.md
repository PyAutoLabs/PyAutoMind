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
