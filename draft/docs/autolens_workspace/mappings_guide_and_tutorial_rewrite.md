# Mappings guide (`guides/mappings.py`), tutorial_2_mappers rewrite with polygons, and dead index-section fixes across the workspaces

Type: docs
Target: autolens_workspace
Repos:
- autolens_workspace
- HowToLens
- HowToGalaxy
- autogalaxy_workspace
Difficulty: medium
Autonomy: supervised
Priority: high
Status: formalised
Consequence: judge
Review-minutes: 20
Unattended: ready
Epic: image-source-mappings
Phase: 3
Filed: 2026-09-02

Mappings guide (`guides/mappings.py`), tutorial_2_mappers rewrite with polygons, and dead index-section fixes across the workspaces.

> Phase 3 of the `image-source-mappings` epic — ledger
> `draft/feature/autoarray/image_source_mappings_epic.md`. Phase 2 is **merged** (record
> `complete/2026/09/image-source-mappings-p2.md` — PyAutoArray#518, PyAutoLens#720) but **not yet released**; this phase
> stays blocked until **both** the PyAutoArray and PyAutoLens releases land, because the guide and the rewritten tutorial
> call both libraries' new APIs, so both must be on PyPI first.

## The guide

**new** `autolens_workspace/scripts/guides/mappings.py` (top-level `guides/`, like `lens_calc.py`; `__Contents__` block
per `guides/lens_calc.py:21-40`; `__Env__` trailer; auto-simulate guard). Sections:

- **Point Mappings** — trace + `PointSolver`.
- **Region Mappings, Parametric Source** — `Circle`, `source_mapping_from`. This section also shows `steps()` refinement
  frames ("how the solver homes in") and quotes `find_magnification` against the analytic value for the example lens.
- **Region Mappings, Pixelized Source** — `source_clumps_from`, with the threshold demonstrated at 0.2 / 0.5 / 0.8 on a
  two-clump source (0.2 merges two galaxies into one, 0.5 one smooth source, 0.8 splits star-forming knots).
- **`subplot_mappings`**.
- **Brightest Image-Plane Positions for Spectroscopic Follow-Up (4MOST)** — `multiple_image_positions_from` → pixel
  coordinates → `astropy.wcs.WCS(dataset.data.header...)` **inline in the guide**, plus the fibre-diameter caveat.
  This is the 4MOST use case from the original request, and it is deliberately guide-level: the user decision
  (2026-09-02) is that **WCS/RA-Dec stays out of the library** — the library returns arcsec + pixel coordinates only,
  and the astropy conversion is shown here. `Array2D.from_fits` retains the FITS header (`uniform_2d.py:900`), so
  `dataset.data.header` carries the WCS keywords when the source FITS had them (verified fact 5).
- **Magnification per Image**.
- **Wrap Up**.

## Tutorials

Rewrite `HowToLens/scripts/chapter_3_pixelizations/tutorial_2_mappers.py`: drop the "VISUALS SLIGHTLY BUGGY" line (line 10);
replace the four dead `indexes = ...` blocks (lines 166/182/205/265) with `mapper.mappings_from(pix_indexes=...)` →
`regions=` on `plot_array` / `subplot_image_and_mapper`, drawing polygons in both planes; guard the hard-coded indexes
with `min(idx, mapper.pixels - 1)` for small-dataset meshes. Mirror to `HowToGalaxy/.../tutorial_2_mappers.py` (mapper
only); touch `tutorial_3_inversions.py` in both if their index sections are dead too.

## Dead index sections to fix

- `autolens_workspace/scripts/imaging/features/pixelization/delaunay.py:1283`
- `autolens_workspace/scripts/interferometer/.../delaunay.py:1083`
- the `likelihood_function.py` occurrences (imaging, interferometer, and the autogalaxy_workspace mirror)

(These are the sections known and deferred in `complete/2026/07/slam-adapt-inversion-cascade.md:117`.)

## Prose updates

- `autolens_workspace/scripts/imaging/features/pixelization/fit.py:254-261` — say "regions", not circles (today it
  promises coloured mapping circles that were never drawn).
- `autogalaxy_workspace/.../pixelization/plot.py`.
- `guides/plot/visuals.py` — document `regions=`.

Regenerate notebooks (`generate_and_merge` skill), smoke via `run_smoke.py`.

## Delegation note

**Tutorial prose is Opus-tier** (a Fable session delegates it to an Opus subagent), per the tutorial-prose split in
`PyAutoBrain/skills/WORKFLOW.md`. The mechanical legs (dead index-section fixes, notebook regeneration, smoke) can go
one rung further down.

## Verification

`python .github/scripts/run_smoke.py` on the touched scripts; regenerate notebooks; HowToLens `tutorial_2_mappers`
renders polygons in both planes with no BUGGY line.
