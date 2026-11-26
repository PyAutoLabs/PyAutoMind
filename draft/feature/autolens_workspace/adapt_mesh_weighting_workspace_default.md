# Adapt mesh weighting phase 3: every workspace uses HilbertSNR and the soft AdaptSplit image

Type: feature
Target: autolens_workspace
Repos:
- autolens_workspace
- HowToLens
- HowToGalaxy
- autolens_workspace_test
- autogalaxy_workspace_test
Difficulty: large
Autonomy: supervised
Priority: high
Consequence: judge
Parent: complete/2026/11/adapt-mesh-weighting-library.md (PyAutoArray#716)
Filed: 2026-11-26

Phase 3 of making the adapt-mesh-weighting result the default everywhere (human, 2026-11-26:
"make this the default everywhere (but keep BC via `Hilbert` ..., ensure `AdaptSplit` retains BC
too), so all workspaces use the new one and a user doesnt need to supply weight_power=3.5 and
weight_floor=0.01 the default always gives this great adaption"). Needs phase 1
(PyAutoArray#717) and phase 2 (`complete/2026/11/adapt-mesh-weighting-galaxy.md`: PyAutoArray#718, PyAutoGalaxy#763, PyAutoLens#897, all merged)
merged.

## What to do

- (The `al.` exports shipped in phase 2 after all: PyAutoLens#897.) Scripts use the phase 2 API:
  `al.image_mesh.HilbertSNR(pixels=..., edge_pixels=30)`, `al.AdaptImages.from_result(result=...,
  image_mesh={"source": image_mesh})`, `al.mesh.Delaunay(pixels=image_mesh.pixels,
  zeroed_pixels=image_mesh.edge_pixels)`; `al.galaxy_snr_maps_from` where the raw S/N map is needed
  (e.g. the over-sampling threshold in `group/slam.py`).

- Every script that builds a Hilbert image mesh switches from
  `image_mesh.Hilbert(pixels=..., weight_power=3.5, weight_floor=0.01)` to
  `image_mesh.HilbertSNR(pixels=...)`, fed the S/N map before the adapt floor, and gives
  `AdaptSplit` the soft adapt image (phase 2's one call).
- Remove the S/N 3 cap on the source adapt image (autolens_workspace #522, Mind
  `complete/2026/09/adapt-image-snr-cap.md`) wherever it is applied.
- Text in the tutorials / HowTo chapters that explains `weight_power` / `weight_floor` and the
  cap is rewritten for the new default (what the point budget does, its knobs, its two known
  limits), with `Hilbert` mentioned as the older peak-normalised option.
- Found 2026-11-26 with `image_mesh.Hilbert` (files): autolens_workspace 5, HowToLens 1,
  HowToGalaxy 1, autolens_workspace_test 15, autogalaxy_workspace_test 6. In the `_test`
  workspaces, scripts that pin likelihoods: keep `Hilbert` where the pin tests `Hilbert` itself;
  switch (and re-pin with a one-line reason) where the script stands for the user default.
- Interferometer and rectangular-mesh scripts: see the Mind follow-ups
  `draft/research/autoarray/interferometer_adapt_image_get_the_imaging_mesh.md` and
  `draft/research/autoarray/adaptive_rectangular_meshes_repeat_the_adapt_ima.md`; do not change
  them here beyond what the imaging default requires.

Evidence for the default: `~/Science/Science/development/adapt_snr_cap/` (`wiki/project/state.md`,
`results/snr_range/`, `results/compare_cpu/`).

## Folded in: adapt image is the S/N map (prose)

From `draft/docs/autogalaxy/adapt_image_is_the_s_n_map.md` (superseded 2026-11-26; its library
docstrings shipped in PyAutoGalaxy#644, and its API-honesty assessment is answered by the S/N-map
API of PyAutoGalaxy#763: `galaxy_snr_maps_from`, `soft_snr_maps_from`, `AdaptImages.from_result`).
Where the scripts are rewritten for the new default, the `__Adapt Images__` cells say what the adapt
input is: the source's signal-to-noise map (data with the other galaxies' model images subtracted,
over the noise map) from the previous result, what the mesh and the adaptive regularization adapt
to, and why S/N (unit-free, the same across datasets, where an image depends on brightness units).
Known stale cells (2026-11-05 sweep): autolens_workspace `scripts/guides/modeling/slam_start_here.py`,
`scripts/multi_galaxy/features/pixelization/adaptive.py`, the subhalo `slam_source_pixelized.py`
("an initial estimate of the source morphology").
