# Preserve assertion labels

- completed: 2026-10-25
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1717
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1721
- merge-commit: 75124bb5ed2307246a1a2ef4d553dc9e444bd290
- pending-release: PyAutoFit@https://github.com/PyAutoLabs/PyAutoFit/pull/1721
- authorization: human /prm on 2026-10-25; merged unchanged at the checked head
- validation: every head workflow/job passed (Python 3.12, Python 3.13, no-JAX; applicable docs); combined serial suite 3913 passed, 1 skipped, 1 xfailed; four branches merge cleanly; model identifier parity passed
- limitation: downstream workspace smoke was not run; the gap was disclosed before the human merge command and remains recorded, not reported as a pass
- release: not performed; preserve pending-release until a published release is verified

## Outcome

Preserve assertion labels. The implementation and regression tests are in the linked PR. Test-only #1723 was merged first to remove the known random start-point flake. Its three witness tests passed 200 repetitions each (600 passes). The source changes preserve representative output identifiers. Initial parallel unit failures reproduced the existing shared-output collision task; acceptance used serial combined validation and current-head GitHub CI.

## Close-out

All branch heads are ancestors of origin/main. No source changes were made during /prm. Issues closed as completed; prompts moved through lifecycle.py. The three declared glance tasks record stage-1 merged-unchanged shadow rows from the observed head equality; no independent-adversary evidence is claimed.

## Original prompt

# add_assertion name is silently dropped

Type: bug
Target: PyAutoFit
Repos:
- PyAutoFit
Themes:
- visualization
Difficulty: small
Autonomy: safe
Priority: normal
Status: formalised
Consequence: glance
Witness: model.add_assertion(model.sigma > 5.0, name="sigma_floor") then reading the assertion back reports name == "sigma_floor" instead of the default/None it reports today.
Review-minutes: 3
Unattended: ready
Filed: 2026-09-10

`add_assertion(..., name=...)` accepts a `name` and then throws it away.

The assertion classes expose `name` as a **read-only property**, so the
constructor's assignment either no-ops or never happens; nothing is written to
the backing attribute. The fix is one line: write **`_name`** (the backing
field the property reads) rather than `name`.

Consequence: assertion labels are unusable. Anything that wants to display an
assertion — `model.info`, a log message, the model figure being designed under
the `model-figures` epic (`draft/feature/autofit/model_figures_epic.md`) — has
no human-readable handle for it and must fall back to reconstructing the
operands. Combined with the sibling defect that `repr()` of an assertion
recurses forever (`draft/bug/autofit/assertion_repr_recurses_forever.md`),
there is currently *no* safe way to print an assertion.

Add a test that sets a name through `add_assertion` and reads it back, and one
that checks the default when no name is given.

Found on 2026-09-10 by execution while auditing the PyAutoFit model API for the
model-figures design (research leg B, "What is missing from the PyAutoFit model
API", item 3).

Issued: 2026-10-25
