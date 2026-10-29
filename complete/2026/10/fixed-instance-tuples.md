# Enumerate fixed values once

- completed: 2026-10-25
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1718
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1722
- merge-commit: eda10ad1c4c5024b34aa35d4b4cdcfce992421fe
- authorization: human /prm on 2026-10-25; merged unchanged at the checked head
- validation: every head workflow/job passed (Python 3.12, Python 3.13, no-JAX; applicable docs); combined serial suite 3913 passed, 1 skipped, 1 xfailed; four branches merge cleanly; model identifier parity passed
- limitation: downstream workspace smoke was not run; the gap was disclosed before the human merge command and remains recorded, not reported as a pass
- release: not performed; preserve pending-release until a published release is verified

## Outcome

Enumerate fixed values once. The implementation and regression tests are in the linked PR. Test-only #1723 was merged first to remove the known random start-point flake. Its three witness tests passed 200 repetitions each (600 passes). The source changes preserve representative output identifiers. Initial parallel unit failures reproduced the existing shared-output collision task; acceptance used serial combined validation and current-head GitHub CI.

## Close-out

All branch heads are ancestors of origin/main. No source changes were made during /prm. Issues closed as completed; prompts moved through lifecycle.py. The three declared glance tasks record stage-1 merged-unchanged shadow rows from the observed head equality; no independent-adversary evidence is claimed.

## Original prompt

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
Consequence: glance
Witness: on a model with one fixed float (af.Model(Gaussian, centre=0.0)), direct_instance_tuples returns that centre once, not twice.
Review-minutes: 3
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

Issued: 2026-10-25
