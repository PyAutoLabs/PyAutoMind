# cluster/mass_parameterizations*.py promise model.info prints (and figures) they never make

Type: docs
Target: autolens_workspace
Repos:
- autolens_workspace
Themes:
- visualization
- cluster
Difficulty: small
Autonomy: supervised
Priority: low
Status: formalised
Consequence: judge
Review-minutes: 10
Unattended: ready
Filed: 2026-09-13

Found 2026-09-13 during the model-figures phase 6b rollout
(task `model-figures-rollout-lens`, autolens_workspace#542).

## Symptom

`scripts/cluster/mass_parameterizations.py` opens with "This script builds each
option with the model-composition API and **prints `model.info`**, so for every
model you can see at a glance exactly which parameters are free and which are
fixed", and its `__Reading model.info__` section says "For every model we print
`model.info`". The file contains ONE `print(model.info)` (the last section, line
~270). `scripts/cluster/mass_parameterizations_pyautolens.py` says "Everything
uses the model-composition API and prints `model.info` so free vs fixed is
explicit" and contains ZERO prints. Readers of the generated notebooks see the
promise and no output.

## Fix

- Add `print(model.info)` at the end of every section that composes a model in
  both scripts, and beside each print the model figure
  `af.ModelPlotter(model).figure()`. At the FIRST figure site in each script use the
  canonical two paragraphs the rollout settled on 2026-09-14 (copy them verbatim from
  `scripts/cluster/modeling.py` on main); at later sites use a one-to-three-line note
  stating a fact about the model. Do NOT describe the figure itself — no pills, plates,
  badges, greyed values or footer counts. The old map/legend reading this prompt
  originally called for was RETIRED with
  `complete/2026/09/model-figures-rollout-lens.md`; the figure is meant to be
  self-explanatory.
- Keep the scripts un-fitted; regenerate the two notebook twins from the repo
  root (`PYTHONPATH=../PyAutoHands/autohands python3 ../PyAutoHands/autohands/generate.py autolens`).

## Acceptance

- Every composed model in both scripts is printed and drawn; the prose's
  promise is true. Headless run exit 0; twins regenerated; navigator check OK.
