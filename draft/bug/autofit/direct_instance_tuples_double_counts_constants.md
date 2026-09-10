# direct_instance_tuples double-counts Constants

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
Witness: on a model with one fixed float (af.Model(Gaussian, centre=0.0)), direct_instance_tuples returns that centre once, not twice.
Review-minutes: 15
Unattended: ready
Filed: 2026-09-10

`direct_instance_tuples` returns every fixed value **twice**.

`Model.__setattr__` wraps an assigned float in a `Constant`, which is a subclass
of both `float` and `ModelObject`. `direct_instance_tuples` gathers with
`direct_tuples_with_type(Constant)` *and* with `direct_tuples_with_type(float)`
(or equivalent), so each `Constant` matches both passes and appears twice in the
result.

One-line fix: **`direct_tuples_with_type(Constant)` alone suffices**, because
`Constant` *is* a `float` — the extra `float` pass adds nothing but duplicates.

Consequence: any caller that counts fixed parameters gets double. The
model-figures work (`draft/feature/autofit/model_figures_epic.md`) counts them
for the footer ("63 fixed parameters hidden"), and the group-scale lens model
has 291 fixed leaf slots, so the error is not subtle.

Add a test asserting the length of `direct_instance_tuples` on a model with a
known number of fixed floats, including the tuple case (`centre=(0.0, 0.0)`),
where the duplication compounds.

Found on 2026-09-10 by execution while auditing the PyAutoFit model API for the
model-figures design (research leg B, "What is missing from the PyAutoFit model
API", item 6).
