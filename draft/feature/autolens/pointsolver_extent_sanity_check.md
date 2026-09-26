# PointSolver grid-extent sanity check — warn when the data approach the solver grid edge, hint when the grid is oversized

Type: feature
Target: autolens
Repos:
- PyAutoLens
- autolens_workspace_test
Themes:
- point-source
- profiling
Difficulty: medium
Autonomy: supervised
Priority: high
Status: formalised
Consequence: judge
Review-minutes: 20
Unattended: ready
Epic: point-source-cpu-speed
Filed: 2026-09-26
Parent: active/pointsolver_cpu_speed_phase_4.md (issue autolens_profiling#314)

## Human decision (2026-09-26, live)

> "I think +-3" is a bit small for galaxy scale lenses and I think we would need to update it in
> workspace accordingly for each package. but +-10" still wont do clusters well so I think a
> workspace level task is right. We probabbly need some sort of a sanity check that prints or alerts
> the user? and warning based on the extent of the masked data (or the Point dataset)?"

So there is **no library default change for the solver extent**. Each workspace package sets its own
extent (`draft/feature/autolens_workspace/pointsolver_grid_extent_per_package.md`, which depends on
this task). The library gets this sanity check, so that a wrong extent is visible to the user.

## Goal

Add a **one-off, construction-time, non-JAX** sanity check where the solver and the data meet.

1. **WARN** (risk of missed images) when the observed `PointDataset` positions, plus a margin, fall
   outside or near the edge of the solver's grid extent. The solver extent is
   `y_min / y_max / x_min / x_max`. The margin should be tied to the solver's initial `scale` (one or
   two step-0 triangles) and to the position noise, not a fixed arcsec. An image beyond the grid
   cannot be found, and one within a triangle of the edge may be missed.
2. **INFO / performance hint** (softer) when the extent is much larger than the positions need, e.g.
   more than 3× the positions' bounding radius about the lens / positions centre. Quote the phase-4a
   cost: step-0 rows scale with extent², and step 0 is ≈ 66 % of the single-source likelihood.
3. **Fallback** for imaging-based point workflows with no `PointDataset`: use the mask extent.
   **Verify first whether this is needed.** `autolens/analysis/result.py` (≈ L117–121 and L187–191)
   already builds its `PointSolver` from `dataset.mask.derive_grid.all_false`, so there the solver
   grid *is* the mask grid. Find any other imaging/interferometer path that pairs a user-built solver
   with masked data before designing a fallback.

## Where (verify in code at start_dev)

- Likely `AnalysisPoint.__init__`, in PyAutoLens `autolens/point/model/analysis.py` (≈ L40–105). It
  receives both `dataset: PointDataset` and `solver: PointSolver` and stores them. Nothing there is
  traced by JAX.
- An alternative is the fit setup. Pick the single place a user always passes through before a
  search, and make it fire **once per analysis**, not per likelihood call.
- The solver extent lives on `AbstractSolver` (`autolens/point/solver/shape_solver.py` ≈ L35–90:
  `y_min, y_max, x_min, x_max, scale, pixel_scale_precision`). `for_grid` (≈ L154) derives them from
  the grid.
- Handle the multi-plane / multi-source case, where one solver serves several `PointDataset`s (a
  list of analyses), and datasets with fluxes / time delays but no positions (skip).

## Conventions (grep before writing)

- Logging: PyAutoLens uses a module-level `logger = logging.getLogger(__name__)` everywhere
  (`autolens/point/solver/point_solver.py:32`, `shape_solver.py:30`). There is a once-per-process
  `logger.warning` pattern with a module-global flag at `point_solver.py` ≈ L132–145 (the
  `PYAUTO_SMALL_DATASETS` short-circuit warning). `warnings.warn` is used only in `lens/tracer.py` and
  `interop/coolest.py`. Match the logger convention. Decide at start_dev whether the edge case is
  `logger.warning` and the oversize case `logger.info`.
- **Silent in test_mode where appropriate.** `autonerves.test_mode.is_test_mode()` is re-exported in
  `autolens/__init__.py`. Also consider `PYAUTO_SMALL_DATASETS=1`, where the solve is already
  short-circuited. Workspace smoke runs must not fill with the perf hint.
- **Never touch the JAX path.** Use NumPy on the observed positions and the stored floats only. Add
  nothing to `solve()` or the likelihood, and no `jax.debug`.

## Evidence (phase 4a, RAL job 356367)

Source: `lens/autolens_profiling/results/breakdown/point_source_image/solver_config_sweep_hpc_ral_cpu_fp64.json`.
Ledger: `lens/autolens_profiling/results/notes/point_source_cpu_campaign.md`, section "Phase 4a".

- Extent-only speed-ups at scale 0.2 against the ±9.9″ default: ±6″ 1.52×, ±4″ 1.78×, ±3″ 2.05×,
  ±2.5″ 2.24×. All are complete on 200 prior + 200 stress draws, with log L identical to the default.
  Step-0 rows: 11 859 → 4 428 → 2 075 → 1 197 → 848.
- The images the workspace prior needs reach max |coord| 1.78″ and radius 1.81″. The broad stress
  set reaches 2.30″ / 2.52″. Real galaxy-scale lenses can go further (larger θ_E, offset centres),
  which is why the human rejected a tight default, and why the warning must key off **the user's own
  data**.

## Tests

- PyAutoLens unit tests: positions inside, near the edge, and outside the grid (warns); a grid more
  than 3× oversized (info); test_mode silence; no JAX import in the check; a multi-dataset case.
- autolens_workspace_test: one script (or an assertion in `point_source/jax_likelihood/image_plane.py`)
  shows the check fires on a deliberately small grid and is silent on the default. Its log L pins
  must not move.

## Out of scope

Changing any solver default (extent, scale, `MAX_CONTAINING_SIZE`); cluster solvers (epic
`cluster-pointsolver-speed`, though the check should behave sensibly there: warn on edge, and the
oversize hint is probably never triggered).
