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
Consequence: judge
Witness: model.add_assertion(model.sigma > 5.0, name="sigma_floor") then reading the assertion back reports name == "sigma_floor" instead of the default/None it reports today.
Review-minutes: 15
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
