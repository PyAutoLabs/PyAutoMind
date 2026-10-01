## point-audits-wheel-provenance
- issue: https://github.com/PyAutoLabs/autolens_workspace_test/issues/335
- completed: 2026-10-01
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace_test/pull/336
- merge-commit: 6a8b6466aa962cc22bbaf736bf2008fe11382eb1
- summary: Point-solver audits now work with installed wheels, preserve checkout provenance, fingerprint installed package contents and replay the exact digest-verified historical method without runtime Git history.

## Validation and approval

Source/wheel/Heart-isolated regression tests: 9/9 each. Full original TestPyPI wheel audit: 24 cases plus resume. Historical replay: 16 comparisons, zero difference, source and wheel environments. Exact historical source and twelve boundary pins checked against Git. Isolated workspace smoke: 32/32. Ruff, Black and diff checks passed. In-session review; no independent-review claim.

Every run/job reported for e4ba91ffa391c298ae2f281644f91b6a31e37946 was green, including Python 3.12 and 3.13. Human “continue, I authorize” approved merge in this chat; PR merged unchanged on 2026-10-01T16:46:01Z and its head is an ancestor of origin/main.

Corrective RED reason: `release validation FAILED (stage integrate)`.
Live corrective approval: https://github.com/PyAutoLabs/autolens_workspace_test/issues/335#issuecomment-5935062749.
No numerical thresholds, skipped coverage, library code or Heart weights changed. No release or rehearsal performed by this corrective task. Fresh authoritative validation is still needed; older workspace timeout and manifest warnings remain separate.

## Retained local evidence

Task worktree retained at /home/jammy/Code/PyAutoLabs/.worktrees/point-audits-wheel-provenance to preserve datasets, fit output and validation JSON/logs (about 8 MB). No deletion authorized for these data products. The source branch is merged; this retained worktree is not active development. Remove only after a separate data-retention decision.

## Original prompt

# Make point-solver audits work with installed wheels

Type: bug
Autonomy: human-required
Difficulty: medium
Repository: @autolens_workspace_test

## Original request and approval

The health-dashboard task diagnosed release integration run 36838423356 failing
`error_audit.py` and `history_audit.py`: both invoke Git in wheel site-packages.
The assistant asked: “Approve starting corrective development for the two
wheel-incompatible point-solver audits, addressing ‘release validation FAILED
(stage integrate)’?”

User reply, verbatim:
> continue, I approve of this plan

## Scope

Correct the two scripts without skipping audits, changing numerical tolerances,
waiving tests or changing Heart weights. Preserve source-checkout provenance;
record installed distribution identity for wheels. Bundle the exact historical
method and its pinned Git metadata so historical replay remains independently
attributed and works without runtime Git history. Fail closed for malformed or
mismatched evidence. No library API changes, merge, cleanup, release or rehearsal.

## Validation

Targeted provenance and historical-fixture regression tests; numerical replay;
exercise wheel-installed packages outside a Git checkout and source imports.
Run the applicable workspace smoke checks before shipping a pending-release PR.

## Heart corrective authorization

Exact RED reason: release validation FAILED (stage integrate)
Human approved this incident's corrective development in this chat on 2026-10-01.
Record the approval and causal mapping on the issue, PR, active entry and autonomy log.

Issued: 2026-10-01
Issue: https://github.com/PyAutoLabs/autolens_workspace_test/issues/335
