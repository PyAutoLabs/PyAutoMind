## image-source-mappings-p3
- issue: https://github.com/PyAutoLabs/autolens_workspace/issues/525 (closed completed 2026-09-03 by `Closes #525`)
- completed: 2026-09-03
- workspace-pr: autolens_workspace https://github.com/PyAutoLabs/autolens_workspace/pull/526 (head `ed44409f`, merge `31a7b6e4`) — label `pending-release`
- workspace-pr: HowToLens https://github.com/PyAutoLabs/HowToLens/pull/76 (head `ff4259ab`, merge `723f26ce`) — label `pending-release`
- workspace-pr: HowToGalaxy https://github.com/PyAutoLabs/HowToGalaxy/pull/72 (head `2200753d`, merge `85c08b44`) — label `pending-release`
- workspace-pr: autogalaxy_workspace https://github.com/PyAutoLabs/autogalaxy_workspace/pull/232 (head `efb21d9e`, merge `c14de5b7`) — label `pending-release`
- classification: docs (workspace) — epic `image-source-mappings`, phase 3 of 3 (ledger
  `draft/feature/autoarray/image_source_mappings_epic.md`). Fable session; execution delegated to Opus
  (subagent A autolens_workspace, subagent B the other three repos, split by repo so no git index was shared).
- ci: every workflow run for each head sha completed/success — autolens_workspace `Smoke Tests` (3.12 + 3.13),
  `Navigator Check`, `Script Size Guard`; HowToLens / HowToGalaxy `Smoke Tests`, `Tutorials Complete`,
  `Navigator Check`; autogalaxy_workspace `Smoke Tests`, `Navigator Check`, `Script Size Guard`. Local smoke
  7/7, 2/2, 2/2, 2/2; `check_tutorials_complete.py` passes in both HowTo repos.
- heart-ack (carried from the `active.md` entry): "release validation FAILED (stage integrate)";
  "PyAutoArray: open PR 11d old" — the same two reasons at ship time; release-only, not a development blocker.
- merge order: none among the four (independent repos); no library PR in this phase.
- release dependency: the four PRs carry `pending-release` because the scripts import Phase 1–2 APIs. The
  library obligations are the P1/P2 records' `pending-release:` lines (PyAutoArray#517/#518, PyAutoLens#720);
  nothing new is added here. PyPI users cannot run these scripts until both libraries release.
- opened ahead of the release gate by user decision (2026-09-03): workspace CI installs the libraries from
  source, so the gate that the epic ledger recorded ("Phase 3 after BOTH release") was waived.

## What shipped

**autolens_workspace#526.** New `scripts/guides/mappings.py`: point mappings (`PointSolver`), region mappings
of a parametric source (`aa.Circle(y, x, r)` positional + `al.mappings.source_mapping_from`, drawn in both
planes), `ShapeSolver.steps()` refinement frames, `find_magnification` against the analytic isothermal value
(finite source straddling the caustic measures 22.1 → 29.6 as the radius shrinks vs 30.0 point value — the
prose says why), pixelized region mappings via `inversion.source_clumps_from` / `mappings_from` with the
threshold demonstrated at 0.2 / 0.5 / 0.8 (1 / 2 / 4 clumps on the guide's own two-clump, four-knot source),
`subplot_fit_imaging_mappings` for both fits, brightest image-plane position per multiple image in arcsec,
FITS pixels and RA/Dec through an explicit `astropy.wcs.WCS` (guide-level; the library stops at pixels),
fibre-diameter caveat with `use_centroid=True`, per-image magnification for both engines with the flux-share
caveat. Dataset simulated under `should_simulate` into `dataset/imaging/mappings/` (gitignored; not
committed). `guides/plot/visuals.py` `__Regions__` section; `pixelization/fit.py` prose describes the 2×2
figure; four dead `slim_indexes_for_pix_indexes` sites (imaging + interferometer `delaunay.py`,
`likelihood_function.py`) draw one `regions=` figure of the source pixel nearest the source-plane centre.
`guides/mappings.py` added to `smoke_tests.txt` (~30 s, `ENV: full_datasets`) — flagged as strikeable.

**HowToLens#76 / HowToGalaxy#72.** `tutorial_2_mappers` BUGGY warning dropped; every dead index block →
`mapper.mappings_from(pix_indexes=…)` drawn with `subplot_image_and_mapper(regions=)` so a source cell and its
image-plane regions share a colour; the point-level `indexes=` block now plots via `plot_grid(indexes=)`; prose
rewritten around each figure; indexes clamped / grid-derived for the smoke mesh. `tutorial_3_inversions` draws
its five random mappings. HowToGalaxy selects cells by distance from the mesh centre (a single adaptive cell is a
speck; `mapper.pixels // 2` lands on the mesh edge).

**autogalaxy_workspace#232.** Both pixelization `likelihood_function.py` scripts draw the reverse mapping of
reconstruction pixel 200 via `regions=`; the `__Interpolation__` paragraph now points at the image-plane panel
where the footprint is visible. `pixelization/plot.py` untouched (never mentioned `subplot_mappings`).

## Traps and notes

- `autolens.plot` / `autogalaxy.plot` `plot_array` and `plot_grid` are `autogalaxy/util/plot_utils.py`
  wrappers that do NOT forward `regions=` / `indexes=`; every touched script does
  `import autoarray.plot as aaplt`. Library follow-up filed:
  `draft/bug/autoarray/mapping_overlay_follow_ups_forward_regions_throu.md` (with the degenerate
  `RectangularBilinearAdaptDensity` edge cells that map to nothing silently, per-polygon `region_labels`, and
  `plot_mapper` zoom/exception guards).
- `total_mappings_pixels` is absent from every workspace `config/`; the planned config sweep was a no-op.
- The 2026-09-03 morning session's two subagents were killed three times by API 529 before writing a line; the
  afternoon relaunch with identical briefs completed first time.

## Original prompt

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
Issued: 2026-09-03
Issue: https://github.com/PyAutoLabs/autolens_workspace/issues/525

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
