# Bug in autocti_workspace: the dataset_1d results/database example scripts have drifted

Type: triage
Target: autocti
Repos:
- autocti
- autocti_workspace
Themes:
- cti
- notebooks
Difficulty: large
Autonomy: supervised
Priority: normal
Status: formalised
Consequence: glance
Witness: `scripts/dataset_1d/advanced/database/examples/samples.py` and `scripts/dataset_1d/results/examples/samples.py` run end-to-end against the installed autocti (FactorGraphModel instance structure, live plot API), and a minimal smoke workflow runs them in CI.
Review-minutes: 3
Unattended: ready
Filed: 2026-08-19 (backfilled from git)

<!-- formalised by the Intake (Conception) Agent on 2026-08-19 from user-intake -->
