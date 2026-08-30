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
Consequence: judge
Review-minutes: 25
Unattended: ready
Filed: 2026-08-19 (backfilled from git)

Bug in autocti_workspace: the dataset_1d results/database example scripts have drifted from the current library API and are broken beyond the recently-fixed info.json and sample-index issues (the repo has no CI, so nothing catches drift). Two known sites, found 2026-08-19: (a) scripts/dataset_1d/advanced/database/examples/samples.py line ~195 does ml_instances[0].cti, but the guide chain now fits via af.FactorGraphModel whose global-model instances have no top-level .cti attribute — AttributeError once reached; (b) scripts/dataset_1d/results/examples/samples.py calls aplt.subplot_fit_dataset_1d, a plot symbol that no longer exists in the installed autocti (the PyAuto API gate flags it stale). Fix in autocti_workspace: update the examples to the FactorGraphModel instance structure and the live plot API, and consider a minimal CI smoke workflow for the repo so future drift is caught.

<!-- formalised by the Intake (Conception) Agent on 2026-08-19 from user-intake -->
