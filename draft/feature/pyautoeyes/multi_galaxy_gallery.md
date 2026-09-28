# autolens_visualization: multi-galaxy gallery — producer and dataset

Type: feature
Target: autolens_visualization
Repos:
- autolens_visualization
Themes:
- visualization
Difficulty: medium
Autonomy: supervised
Priority: normal
Epic: pyautoeyes-birth
Phase: 6
Status: draft — follows pyautoeyes-birth phase 1a (the lens project repo re-birth); retargeted from the retired autolens-visualization epic (PyAutoMind#436), then to the `autolens_visualization` project repo under the 2026-09-28 layered design
Filed: 2026-09-25

The PyAutoMind#436 birth shipped imaging and interferometer
galleries only. Add the multi-galaxy domain to the gallery:

- a tracked HST-scale multi-galaxy dataset (lens plus at least one extra
  line-of-sight or companion galaxy), with its simulator under
  `scripts/misc/simulators/` so it regenerates;
- a flat `scripts/multi_galaxy/visualization.py` producer following the existing
  imaging/interferometer pattern (true model, `visualize_before_fit` + `visualize` with the all-true
  `config/visualize/plots.yaml`, parametric and Delaunay sources) writing to
  `scripts/multi_galaxy/images/visualization/`;
- the render harness (`gallery/gallery_build.py`) picks the domain up and the tracked
  `gallery/viz_manifest.yaml` lists it (so the PyAutoEyes dashboard shows it); `GALLERY.md` regenerated and
  `--check` green; lint/render workflows run the new producer.

Witness: `python gallery/gallery_build.py --check` in `lens/autolens_visualization` exits 0 with a multi_galaxy section
in `GALLERY.md`, and `pyauto-brain eyes survey lens/autolens_visualization --json`
reports the new producer with 0 gaps and 0 orphans.
