# autolens_visualization: group and cluster galleries (point-source + extended)

Type: feature
Target: autolens_visualization
Repos:
- autolens_visualization
Themes:
- visualization
Difficulty: large
Autonomy: supervised
Priority: normal
Epic: pyautoeyes-birth
Phase: 7
Status: draft — follows pyautoeyes-birth phase 1a and the multi-galaxy gallery; retargeted from the retired autolens-visualization epic (PyAutoMind#436), then to the `autolens_visualization` project repo under the 2026-09-28 layered design
Filed: 2026-09-25

Extend the permanent gallery to group- and cluster-scale lenses, for both
point-source and extended-source modelling:

- tracked group and cluster datasets (point-source positions/fluxes and
  extended imaging), each with a simulator under `scripts/misc/simulators/`;
- flat producers `scripts/group/visualization.py` and
  `scripts/cluster/visualization.py` rendering every visualizer output the
  corresponding fit writes (point-source `FitPositions`/flux figures and the
  extended-source imaging figures), into `scripts/<domain>/images/visualization/`;
- gallery rebuild, `GALLERY.md` sections, lint/render workflow coverage.

Reference producers: `autolens_workspace_test/scripts/cluster/visualization.py`
and `scripts/point_source/visualization/` there (tiny build datasets, figures
gitignored).

Witness: `python gallery/gallery_build.py --check` in `lens/autolens_visualization` exits 0 with group and cluster
sections; the Eyes survey reports both producers with 0 gaps and 0 orphans.
