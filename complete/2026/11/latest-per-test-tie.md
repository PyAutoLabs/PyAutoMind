- summary: test_autofit/results/test_identity.py::test_latest_per_keeps_the_latest_sibling flaked (main red at 963ff296a,
  unittest-nojax): status records stamp completion to the second, two tiny fits often tied and latest_per broke the tie by
  path. Test now backdates the first fit's status `updated` by a minute. Test-only; library tie-break unchanged (correct).
- tests: 20/20 passes; results folder 58 passed; PR CI green.
- why: it blocked `release validate` preflight ("PyAutoFit: CI failure").

## Original prompt

Issued: 2026-11-02
Issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1758
Consequence: judge

# Fix the latest_per sibling test's one-second completion tie (unblocks release validate)

Human: "Fix, then validate" (2026-11-02). Scope in the issue.
