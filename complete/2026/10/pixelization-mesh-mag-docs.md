# Pixelization source_science: mesh magnification documented and checked against truth (arc 4e)

Issue autolens_workspace#605 → PR autolens_workspace#606 merged 2026-10-30 (`65efb65e`). Epic `cluster-strong-lensing`,
phase 4e (docs before phase 6). Library prerequisite PyAutoArray#668 (adaptive-rect true pixel centres, record
`complete/2026/10/adaptive-rect-mesh-node-positions.md`); text also describes PyAutoArray#664/#666. All three pending
release — human authorized merging the workspace before the release.

Shipped in the four pixelization source_science scripts (imaging, interferometer, group, multi_galaxy):
`__Magnification via Mesh__` rewritten (areas = basis-function integrals; per-mesh computation; accuracy; mesh vs
interpolation route; `magnification` latent), new `__True Magnification__` from `tracer.json`, imaging extra-galaxy
noise scaling, interferometer coefficient 0.1, `griddata(fill_value=0.0)` for reconstruction interpolation. Human
prose rule: describe the calculation as it stands, no fix/history wording.

Full-size results (truth / mesh / interpolation): imaging 34.91 / 31.63 / 33.22; interferometer 7.16 / 7.62 / 11.82;
group 20.51 / 20.00 / 20.34; multi_galaxy 25.58 / 22.70 / 24.10. Before: imaging mesh 16.6, interpolation 7.2;
interferometer mesh 4.5; group/multi interpolation NaN. CI smoke 3.12/3.13 + navigator + size-guard green.

Spun out: research `draft/research/autolens_inference/kernel_regularization_distances_adaptive_rectangular.md`.

## Original prompt

# Pixelization source_science.py: document mesh magnification areas properly…

Type: docs
Target: autolens_workspace
Repos:
- autolens_workspace
Difficulty: medium
Autonomy: supervised
Priority: high
Memory: reading-queue.md; wiki/lensing/sources/dark-matter-substructure.md; wiki/galaxies/sources/cosmos-survey.md
Status: formalised
Consequence: judge
Witness: grep finds no `mesh_areas` in the four pixelization source_science.py scripts, each states the areas are the pixels' basis-function integrals and which mesh is approximate, and all four run clean in smoke.
Review-minutes: 20
Unattended: ready
Issued: 2026-10-30
Issue: https://github.com/PyAutoLabs/autolens_workspace/issues/605

# Pixelization source_science.py: document mesh magnification areas properly (arc phase 4 docs, before phase 6)

Type: docs
Target: autolens_workspace
Repos:
- autolens_workspace
Epic: cluster-strong-lensing
Phase: 4e
Arc: draft/feature/autolens/source_cluster_arc.md
Consequence: judge
Autonomy: supervised
Priority: high
Difficulty: medium
Witness: grep finds no `mesh_areas` in the four pixelization source_science.py scripts, each states the areas are the pixels' basis-function integrals and which mesh is approximate, and all four run clean in smoke.

## Original request (verbatim, 2026-10-29)

> intake workspace updates to ensure this is documented properly in source_science.py scripts of pixelization feature before we do 6

## Context

Arc phases 4a (PyAutoArray#664, merged; pending release) and 4b (PyAutoArray#665, in flight) made
`mapper.mesh_geometry.areas_for_magnification` the integral of each mesh pixel's interpolation basis function
(the quadrature weights for which `sum(reconstruction * areas)` is the reconstructed source's integral) on
every mesh: exact for Delaunay (barycentric dual areas), RectangularUniform (uniform cells), the four adaptive
rectangular meshes (per-axis hat quadrature through the CDF) and KNearestNeighbor / KNNBarycentric
(quadrature of their own weights over the hull); DelaunayNN still uses the Delaunay dual areas (approximation,
within 0.5%). Measured against simulator truth (autolens_workspace_test `scripts/imaging/mesh_magnification.py`)
every mesh recovers the true magnification within 1% except RectangularRTUAdaptDensity lensed (-1.82%,
reconstruction-limited).

## Problem

The four pixelization source_science scripts compute magnification from these areas, but their prose predates
the fixes:
- `scripts/imaging/features/pixelization/source_science.py` (`__Magnification via Mesh__`, ~L390-408)
- `scripts/interferometer/features/pixelization/source_science.py`
- `scripts/group/features/pixelization/source_science.py`
- `scripts/multi_galaxy/features/pixelization/source_science.py`

Stale points seen 2026-10-29: the text says the areas are "accessed via the `mesh_areas` attribute" (no such
attribute; the code uses `mapper.mesh_geometry.areas_for_magnification`); it calls them simply "areas of every
pixel", not the quadrature weights of the interpolated source; it does not say which meshes are exact or how
accurate, nor how the mesh route compares with the 1000x1000 interpolation-grid route above it; it does not
point at the PyAutoLens `magnification` latent that computes the same quantity during a fit.

## Style (human, 2026-10-29: "make sure it also knows to use autobrain docs style for python scripts")

All prose added or rewritten in these scripts follows the PyAutoBrain docs style for Python scripts:
- `PyAutoBrain/skills/TUTORIAL_WRITING_STYLE.md`: voice, British English, concrete descriptions, define
  each term at first use, no hype or jargon. Reference example: the COSMOS-Web Ring guided tour (October 2026).
- Script format: the workspace contents + `"""__Section__"""` docstring structure. Top-level docstrings become
  notebook markdown cells (PyAutoHands generation), so the docstrings are the product. Plan placement and the
  format checklist through the Workspace Agent (`/workspace`) before editing, and keep the contents list at the
  top of each script in step with any renamed or added section.
- Do not paste PR numbers or measurement tables into user prose. Say what the areas are and how accurate
  they are in plain words; the PyAutoArray#664/#665 references belong in commit and PR text.

## Work

1. In all four scripts, rewrite the magnification-via-mesh docs: what `areas_for_magnification` is (integral of
   each pixel's basis function, so the sum is the reconstructed source flux), that it is exact on every mesh
   except DelaunayNN (≈0.5%), the measured accuracy, and when to prefer it over the interpolation-grid route.
2. Fix the `mesh_areas` misnomer; keep the four scripts consistent (same wording, same API).
3. Mention the `magnification` latent (PyAutoLens `analysis/latent.py`) as the in-fit equivalent.
4. Check the non-pixelization `source_science.py` siblings and the HowToLens / autolens_assistant mirrors for the
   same stale claims; fix or list them.
5. Smoke the four scripts. Release gate: the text describes PyAutoArray#664/#665 behaviour, so ship after (or
   with) the release carrying them, or word it version-neutrally.

Must land before arc phase 6 (LEGGOS area magnification builds on these areas).

<!-- formalised by the Intake (Conception) Agent on 2026-10-29 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/82a81821-91bc-4bc6-b073-34d547f8bfc1/scratchpad/intake_ss.md -->
