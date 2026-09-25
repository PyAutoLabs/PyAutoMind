# PyAutoEyes lens instance: multi-galaxy gallery — producer and dataset

Type: feature
Target: PyAutoEyes
Repos:
- PyAutoEyes
Themes:
- visualization
Difficulty: medium
Autonomy: supervised
Priority: normal
Epic: pyautoeyes-birth
Phase: 6
Status: draft — follows pyautoeyes-birth phase 1 (lens/ instance layout); retargeted from the retired autolens-visualization epic (PyAutoMind#436)
Filed: 2026-09-25

The PyAutoMind#436 birth shipped imaging and interferometer
galleries only. Add the multi-galaxy domain to the gallery:

- a tracked HST-scale multi-galaxy dataset (lens plus at least one extra
  line-of-sight or companion galaxy), with its simulator under
  `lens/scripts/misc/simulators/` so it regenerates;
- a flat `lens/scripts/multi_galaxy/visualization.py` producer following the phase-1
  pattern (true model, `visualize_before_fit` + `visualize` with the all-true
  `config/visualize/plots.yaml`, parametric and Delaunay sources) writing to
  `lens/scripts/multi_galaxy/images/visualization/`;
- the Eyes harness (`eyes/build.py`, phase 1) picks the domain up; `GALLERY.md` regenerated and
  `--check` green; lint/render workflows run the new producer.

Witness: `pyauto-eyes check lens` exits 0 with a multi_galaxy section
in `GALLERY.md`, and `pyauto-brain eyes survey organs/PyAutoEyes/lens --json`
reports the new producer with 0 gaps and 0 orphans.
