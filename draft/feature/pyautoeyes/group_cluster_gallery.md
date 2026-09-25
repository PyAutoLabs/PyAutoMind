# PyAutoEyes lens instance: group and cluster galleries (point-source + extended)

Type: feature
Target: PyAutoEyes
Repos:
- PyAutoEyes
Themes:
- visualization
Difficulty: large
Autonomy: supervised
Priority: normal
Epic: pyautoeyes-birth
Phase: 7
Status: draft — follows pyautoeyes-birth phase 1 and the multi-galaxy gallery; retargeted from the retired autolens-visualization epic (PyAutoMind#436)
Filed: 2026-09-25

Extend the permanent gallery to group- and cluster-scale lenses, for both
point-source and extended-source modelling:

- tracked group and cluster datasets (point-source positions/fluxes and
  extended imaging), each with a simulator under `lens/scripts/misc/simulators/`;
- flat producers `lens/scripts/group/visualization.py` and
  `lens/scripts/cluster/visualization.py` rendering every visualizer output the
  corresponding fit writes (point-source `FitPositions`/flux figures and the
  extended-source imaging figures), into `lens/scripts/<domain>/images/visualization/`;
- gallery rebuild, `GALLERY.md` sections, lint/render workflow coverage.

Reference producers: `autolens_workspace_test/scripts/cluster/visualization.py`
and `scripts/point_source/visualization/` there (tiny build datasets, figures
gitignored).

Witness: `pyauto-eyes check lens` exits 0 with group and cluster
sections; the Eyes survey reports both producers with 0 gaps and 0 orphans.
