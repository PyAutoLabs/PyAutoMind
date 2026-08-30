# autolens_workspace_developer: broad stale-API rot (56 symbols, no CI)

Type: maintenance
Target: autolens_workspace_developer
Repos:
- autolens_workspace_developer
Themes:
- hygiene
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: formalised
Consequence: judge
Review-minutes: 20
Unattended: ready
Filed: 2026-08-04 (backfilled from git)

Found 2026-08-04 while fixing the `aplt.Output` drift in this repo under
`plot-array-stale-kwargs` (HowToGalaxy#56). That task cleared `aplt.Output`
completely; this prompt records the **much larger** rot sitting underneath it,
which was deliberately left out of scope.

## What was measured

An alias-aware AST scan (resolving each file's own import aliases, then checking
every attribute chain against the *installed* stack) found **56 stale symbol
references** across the repo. Sample:

- `al.Preloads`, `al.mapper_indices_from` — `plotting_alignment/imaging_delaunay.py:139-140`,
  `imaging_rectangular.py:138-139`, `imaging_rectangular_no_interp.py:138-139`
- `al.mesh.RectangularKernelAdaptDensity`, `al.mesh.RectangularKernelAdaptImage` —
  `plotting_alignment/kernel_cdf_alignment.py`, `searches_minimal/probe_grad_pix*.py`
- `al.mesh.RectangularSplineAdaptImage`, `al.mesh.RectangularRotatedAdaptImage` —
  `rect_adapt_duo/compare_meshes.py`
- `al.AdaptImageMaker`, `al.mesh.Voronoi` — `slam_pipeline/dspl.py` (7 sites)
- `al.Grid2DIterate` — `plotting_alignment/plot/imaging/orientation/simulator.py:47`
- `aa.Mesh2DRectangularUniform`, `aa.MapperGrids` — `plotting_alignment/edges_standalone.py`
- `al.FitQuantity` — `legacy/quantity/tests/…` (likely intentionally legacy; check
  whether `legacy/` should be scanned at all, or condemned via PyAutoGut)

Separately, a signature-bind check found **kwarg** drift that a symbol scan
cannot see:

- `al.Pixelization(image_mesh=…)` — `imaging_delaunay.py:202`,
  `plot/imaging/orientation/pix.py:61,64`
- `al.Settings(force_edge_pixels_to_zeros=…, use_sparse_linalg=…)` —
  `imaging_delaunay.py:236`, `imaging_rectangular.py:232`,
  `imaging_rectangular_no_interp.py:230`

## Why it went unnoticed

This repo has **no smoke coverage** — nothing runs these scripts, so drift
accumulates silently. Four files repaired under #56 still do not run
end-to-end because they break *earlier* on the symbols above:
`imaging_delaunay.py`, `imaging_rectangular.py`, `imaging_rectangular_no_interp.py`,
`plot/imaging/orientation/simulator.py`.

Several scripts also depend on FITS datasets absent from the repo (e.g.
`plot/interferometer/orientation/simulator.py` needs
`dataset/interferometer/uv_wavelengths/sma.fits`), so end-to-end runs are not
possible without sourcing data first — plan verification accordingly.

## Suggested approach

Triage before repairing — a blanket rename would be wrong here:

1. **Decide what is still wanted.** This is a developer/experiment repo; some of
   this (`legacy/`, `rect_adapt_duo/`, `searches_minimal/`) may be dead
   experiments better condemned to PyAutoGut than modernised. Ask the human
   before repairing anything under `legacy/`.
2. For what survives, map each stale symbol to its current API by introspecting
   the installed stack — do not guess a rename.
3. Consider whether a **minimal smoke tier** is worth adding for the handful of
   scripts that are genuinely still used, so this cannot silently rot again.
   Note the dataset gap above: a smoke tier only helps for scripts whose data
   is reachable.

## Verification

Re-run both detectors on the post-fix tree and require the counts to drop to
the intended targets — do not trust the pre-fix inventory as proof:
an alias-aware symbol scan, plus an `inspect.signature`-bind pass over every
library call (the kwarg drift above is invisible to the symbol scan alone).
