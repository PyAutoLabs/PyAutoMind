# PyAutoEyes phase 5 — retire duplicate galleries + public surfaces

Type: feature
Target: PyAutoEyes
Repos:
- PyAutoEyes
- autolens_workspace_test
- PyAutoBrain
- PyAutoScientist
- pyautolabs.github.io
Themes:
- visualization
- infrastructure
Difficulty: medium
Autonomy: supervised
Priority: normal
Lane: local-dev
Status: draft
Consequence: judge
Witness: `autolens_workspace_test/gallery/` deleted with no CI referencing it; RTD `docs/organs/eyes.md` full page builds; `repos_sync.py --check` green
Review-minutes: 15
Epic: pyautoeyes-birth
Phase: 5
Filed: 2026-09-25

Unblocked: phase 4 COMPLETE 2026-09-29 (PyAutoMind#455; record complete/2026/09/eyes-fit-cti-instances.md).

## Task

Delete `autolens_workspace_test/gallery/` (no CI uses it; the lens figures
live in `autolens_visualization`) and decide, per workspace_test, whether
their `visualization*.py` scripts stay as smoke scripts; drop
`autolens_workspace_test` as a secondary Eyes conductor instance. RTD
`docs/organs/eyes.md` full page describing the two layers (the
`<lib>_visualization` project repos and the PyAutoEyes dashboard);
PyAutoScientist + hub prose linking the dashboard;
`autolens_profiling`/`autolens_inference` unchanged (profiling stays
per-library by the pinned-timing argument).
