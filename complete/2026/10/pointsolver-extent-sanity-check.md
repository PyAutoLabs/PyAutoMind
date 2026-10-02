# PointSolver extent sanity check — complete

- completed: 2026-10-02
- issue: https://github.com/PyAutoLabs/PyAutoLens/issues/763
- epic: point-source-cpu-speed
- pending-release: PyAutoLens@https://github.com/PyAutoLabs/PyAutoLens/pull/764

## Shipped

- PyAutoLens#764: `0dd420877e18da8e94cbb3dfb5dbe97ad34eb45c` — NumPy-only diagnostic once at AnalysisPoint construction; warning for observed positions near/outside the grid using margin `2 * scale + 3 * position sigma`; oversized-grid INFO suppressed in test/small-dataset mode.
- autolens_workspace_test#338: `5140a56e9f6ee37d65effd82964cec0ab7ac5f7d` — construction warning plus unchanged image-plane likelihood pin and repeated JIT/vmap parity; registered in smoke.
- autolens_profiling#363: `134695058dd16752ddb3d9bad747422ff0173ee5` — campaign page and full ledger.

Every claimed branch has zero commits ahead of origin/main after merge. No extent, scale, MAX_CONTAINING_SIZE or likelihood-path default changed. Observed-position coverage is explicitly not a proof of image completeness across the model prior. Cluster work remains separate.

## Validation

27 focused NumPy tests passed; full library suite 820 passed, 1 expected failure. All 33 distinct workspace smoke scripts have passing evidence after the documented environment recovery; final new-script run 56.2 s under the unchanged 300 s cap. All 8 GitHub CI jobs passed across library docs, Python 3.12/3.13/no-JAX tests, workspace changes and Python 3.12/3.13 smoke, and profiling lint.

The initial local smoke error was a missing __Env__ heading. A concurrent environment rebuild caused 21 missing-package failures, all recovered. One subsequent timeout coincided with a host scheduling/suspension delay; the unchanged script passed its bounded retry. Original reports are retained in the task root.

## Human decisions and release

Human acknowledged the reported Heart YELLOW development checkpoint through “prm and continue”. Library and campaign PRs merged first. Human subsequently instructed “can you merge and well do release after”, explicitly permitting workspace merge before the library release. The workspace release gate is discharged by that instruction; the library pending-release obligation above remains. No release was started.

## Follow-up and retention

Next bounded epic member: `draft/feature/autolens_workspace/pointsolver_grid_extent_per_package.md`, choosing per-package galaxy-scale extents with fresh correctness/performance evidence. No next phase issued in this close-out. The broad timing-noise audit remains autolens_profiling#362.

Task worktree retained pending the human's cleanup choice: roughly 884 KB of generated smoke datasets and 20 KB of aggregator output, plus validation logs. The earlier inference worktree/data remain preserved under the separate explicit instruction.

## Neighbour reconciliation

`/intake reconcile draft/feature/autolens_workspace` found no suspects. The
`draft/feature/autolens` scan flagged eight existing Source & Cluster / COOLEST /
magnification prompts; none is implemented by this extent diagnostic, so all
remain filed. Revisit via `/intake reconcile draft/feature/autolens` as separate
work. No sibling prompt retired by resemblance.

## Original prompt

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
Status: active
Consequence: judge
Review-minutes: 20
Unattended: ready
Epic: point-source-cpu-speed
Filed: 2026-09-26
Issued: 2026-10-02
Issue: https://github.com/PyAutoLabs/PyAutoLens/issues/763
Parent: complete/2026/09/point-source-cpu-p4.md (issue autolens_profiling#314)

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

## Approved implementation — 2026-10-02

The preceding issued epic member is complete: `complete/2026/10/point-source-search-nautilus-leaf.md`, inference#17 and profiling#361 merged. Broad timing-noise audit is a separate issue, profiling#362.

### Proposed bounded implementation
1. Add a private NumPy-only diagnostic called once by `AnalysisPoint.__init__` in `autolens/point/model/analysis.py` when a solver and usable observed positions are present. Compare each position with the four stored solver bounds using margin `2 * initial scale + 3 * position sigma`. Warn when outside/within that margin; the message must explain that observed-position coverage does not guarantee completeness over the model prior.
2. Emit a softer INFO hint when both solver half-widths exceed three times the required observed-position envelope about the solver midpoint, including the same margin. Suppress the performance hint in test/small-dataset mode. No solver default or likelihood/JAX path changes. Handle solver=None, absent/empty positions and separate analyses independently.
3. Add NumPy unit cases in `test_autolens/point/model/test_analysis.py`: safe, near-edge, outside, asymmetric/offset bounds, noise-scaled margins, oversize hint, absent inputs, test-mode behavior and one diagnostic per construction. Verify the full library suite. Existing `autolens/analysis/result.py` constructs solvers from the dataset mask grid; no extra masked-data fallback is proposed for those paths.
4. Add one isolated workspace regression script beside `scripts/point_source/jax_likelihood/image_plane.py` to capture an undersized-grid warning and verify the established likelihood pin is unchanged, then run targeted point-source smoke. Library first, then workspace companion; keep the original campaign limits.

### Survey and guard
Canonical `PyAutoLens` and `autolens_workspace_test` are both clean on main. Proposed branch: `feature/pointsolver-extent-sanity-check`. PyAutoLens is unclaimed. At the original survey, `autolens_workspace_test` was claimed by critical-curves-dispatch-audit and the autoarray bundle. Those tasks have since merged (2026-10-02); the bundle claims are released. See `complete/2026/10/mesh-interpolator-numerics-audit.md`, `fit-util-masked-division.md`, and `mesh-geometry-transformed-areas.md` in the same completion folder. Re-survey current claims before new work. No issue/worktree/source edits started for this phase.

## Approval and coordination

Human: "I approve, continue" (2026-10-02), approving the implementation and coordinated disjoint workspace-test edits. Workspace work is restricted to a new point-source extent regression and its smoke registration/config; preserve other tasks' scripts and registrations. PyAutoLens tests use the existing `test_analysis_point.py` naming (the draft `test_analysis.py` path does not exist).

## Implementation progress — 2026-10-02

The approved diagnostic and 27 NumPy tests are implemented. Tests live in the new
`test_analysis_point_extent.py` alongside existing analysis tests. Standalone JAX
regression passes the existing likelihood pin and repeated jit/vmap log checks.
Full library and Heart isolated workspace smoke are running. Canonical campaign
page and full ledger updates are isolated in the task's `autolens_profiling`
worktree (only those two campaign files; no critical-curves overlap).

Heart refreshed YELLOW (85): manifest drift and absent release rehearsal. Human
acknowledgment requested before development PR opening.

## Validation complete; shipping checkpoint — 2026-10-02

- Full PyAutoLens suite: **820 passed, 1 xfailed**, 44 warnings, 1413.88 s.
- Focused new NumPy cases: **27 passed**.
- Workspace: **33 distinct smoke scripts have passing evidence**. The new script
  passed finally in **56.2 s** under the unchanged **300 s** cap.
- The initial new-script failure was a missing `__Env__` declaration heading,
  corrected without changing assertions or pins. A concurrent cache rebuild
  caused 21 missing-NumPy failures; all 21 passed after restoration. A subsequent
  new-script timeout coincided with a host-wide delay (30 s requested sleep took
  428 s; JAX heartbeat 30 → 438 s); the unchanged script passed the bounded retry.
- Evidence: task-root `library-tests.log`, `extent-tests.log`,
  `extent-smoke-profile.log`, `smoke-first-report.json`,
  `smoke-recovery-report.json`, `smoke-rerun-report.json`,
  `smoke-combined-summary.json`. The full smoke list is restored.
- No PR opened or source commit made: ship skills require acknowledgment of
  refreshed Heart **YELLOW (85)**. The request is pending. Source/ledger changes
  and drafted PR bodies are retained in the isolated task root.
- On acknowledgment: ship PyAutoLens first, then the workspace companion (with
  PyAutoLens release gate) and the campaign-record PR. Do not issue another phase.

## Shipped for review — 2026-10-02

Human instructed “prm and continue” after the Heart YELLOW checkpoint. That
acknowledges development shipping on the reported verdict; no release is
authorized. The readiness reasons remain manifest drift and missing rehearsal.

- Library: https://github.com/PyAutoLabs/PyAutoLens/pull/764 (`b9726f75a`).
- Workspace: https://github.com/PyAutoLabs/autolens_workspace_test/pull/338 (`3f81643`).
- Campaign record: https://github.com/PyAutoLabs/autolens_profiling/pull/363 (`44087ce`).

All three are mergeable but CI is pending. At judgment: library docs plus
Python 3.12, 3.13 and no-JAX tests in progress; workspace Python 3.12/3.13
smoke in progress (changes job passed); profiling lint in progress. No merge
or cleanup. Workspace retains its PyAutoLens release gate. Per workspace
AGENTS.md, judged once and stopped; no background waiter is armed. Resume prm
when checks finish, preserving the one-phase-at-a-time campaign rule.

## prm — partial merge, release checkpoint — 2026-10-02

Verified every job for the three exact PR heads: library docs, Python 3.12,
Python 3.13 and no-JAX tests (4); workspace changes plus Python 3.12/3.13 smoke
(3); profiling lint (1). All 8 completed successfully; all PRs CLEAN/MERGEABLE.
Heart freeze command returned `not frozen`.

- PyAutoLens#764 merged: `0dd420877e18da8e94cbb3dfb5dbe97ad34eb45c`.
- autolens_profiling#363 merged: `134695058dd16752ddb3d9bad747422ff0173ee5`.
- autolens_workspace_test#338 stays OPEN and green: recorded PyAutoLens release
  gate still applies. Latest published release `2026.10.2.1` at 09:29:37 UTC
  predates the 10:41:21 UTC library merge; no fetched tag contains the merge.

The ship-workspace release rule prevents merging the dependent workspace
change before the supporting library is released. No release authorization
is implied by prm. Keep issue #763, prompt, claims and all worktrees intact;
no cleanup or second campaign phase. Once a release contains #764, resume
prm to merge #338 and perform the full close-out.
