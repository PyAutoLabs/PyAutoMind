# PyAutoEyes phase 4 — fit + cti instances (PyAutoFit, PyAutoCTI figures)

Type: feature
Target: PyAutoEyes
Repos:
- PyAutoEyes
Themes:
- visualization
- infrastructure
Difficulty: large
Autonomy: supervised
Priority: normal
Lane: local-dev
Status: draft
Consequence: judge
Witness: the fit and cti instance surveys report no gaps/orphans; `pyauto-eyes check --all` green; GALLERY.md links resolve (lychee); board shows fit and cti rows
Review-minutes: 15
Epic: pyautoeyes-birth
Phase: 4
Filed: 2026-09-25

Blocked on: phase 3 shipped.

## Task

`fit/` (ModelPlotter, EPPlotter, VisualizerExample on `gaussian_x1`) and
`cti/` (Dataset1D + ImagingCI visualizers, simulated from
`autocti_workspace/scripts/*/simulators`). Same steps as phase 3: flat
producers, all-true `plots.yaml`, simulated datasets, registry entries,
render, board rows, per-library release dispatch events.
