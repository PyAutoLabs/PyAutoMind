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
