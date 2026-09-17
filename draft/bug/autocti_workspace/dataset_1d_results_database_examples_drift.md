# autocti_workspace: the dataset_1d results/database example scripts have drifted

Type: bug
Target: autocti_workspace
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

<!-- re-homed from draft/triage/ to draft/bug/autocti_workspace/ at the witness-campaign close-out, 2026-09-17: two concrete sites, a bug not a triage -->
<!-- formalised by the Intake (Conception) Agent on 2026-08-19 from user-intake -->
