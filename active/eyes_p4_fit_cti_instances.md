# PyAutoEyes phase 4 — birth autofit_visualization + autocti_visualization

Type: feature
Target: autofit_visualization
Repos:
- autofit_visualization
- autocti_visualization
- PyAutoEyes
- PyAutoMind
- PyAutoBrain
- PyAutoHeart
Themes:
- visualization
- infrastructure
Difficulty: large
Autonomy: supervised
Priority: normal
Lane: local-dev
Status: active
Consequence: judge
Witness: the fit and cti project-repo surveys report no gaps/orphans; each repo's `gallery_build.py --check` green with a tracked manifest; `pyauto-eyes check` green over all four registry rows; the PyAutoEyes dashboard shows fit and cti sections; `repos_sync.py --check` clean
Review-minutes: 15
Epic: pyautoeyes-birth
Phase: 4
Filed: 2026-09-25
Issued: 2026-09-29

Issue: https://github.com/PyAutoLabs/PyAutoMind/issues/455 — both repos created 2026-09-29.

## Task

Two project repos, same steps as phase 3:

- `fit/autofit_visualization` — ModelPlotter, EPPlotter, VisualizerExample on
  `gaussian_x1`.
- `cti/autocti_visualization` — Dataset1D + ImagingCI visualizers, simulated
  from `autocti_workspace/scripts/*/simulators`.

Each: flat producers, all-true `plots.yaml`, simulated datasets, render
harness, tracked PNGs + `GALLERY.md` + tracked manifest, `lint.yml` +
`render.yml` on its library's release dispatch (`pyautofit-release`,
`pyautocti-release`) firing `eyes-refresh`; Mind/Brain/Heart registration as
phase 1a; PyAutoEyes `registry.yaml` rows.
