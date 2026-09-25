# PyAutoEyes phase 3 — galaxy instance (PyAutoGalaxy figures)

Type: feature
Target: PyAutoEyes
Repos:
- PyAutoEyes
Themes:
- visualization
- infrastructure
Difficulty: medium
Autonomy: supervised
Priority: normal
Lane: local-dev
Status: draft
Consequence: judge
Witness: the galaxy instance survey reports no gaps/orphans; `pyauto-eyes check galaxy` green; GALLERY.md links resolve (lychee); board shows a galaxy row
Review-minutes: 15
Epic: pyautoeyes-birth
Phase: 3
Filed: 2026-09-25

Blocked on: phase 2 shipped.

## Task

Port `autogalaxy_workspace_test/scripts/{imaging,interferometer,ellipse}/visualization/`
to `galaxy/scripts/<domain>/visualization.py` (flat producers, HST-scale
imaging + SMA interferometer presets shared from `eyes/instruments`),
`plots.yaml` all-true, datasets simulated into `galaxy/dataset`. Register the
instance in `registry.yaml`; render; board row; `render.yml`
`pyautogalaxy-release` dispatch event.
