# Magnification at a point: document it in every source_science.py and the guides

Type: docs
Target: autolens_workspace
Repos:
- autolens_workspace
Themes:
- cluster
- point-source
Difficulty: medium
Autonomy: safe
Priority: high
Status: draft
Consequence: glance
Witness: Every one of the eleven `scripts/*/source_science.py` (imaging, group, multi_galaxy, interferometer and their multi_gaussian_expansion / pixelization feature variants) carries a `__Magnification At A Point__` section that calls `al.LensCalc.from_tracer(tracer=tracer).magnification_2d_via_hessian_from(grid=al.Grid2DIrregular([...]))` at chosen (y,x) coordinates and prints the result; `guides/lens_calc.py` has a `__Magnification At A Point__` section after `__Hessian__`; `point_source/fit.py` prints `fit.positions.signed_magnifications_at_positions` and `fit.positions.magnifications_at_positions`; every edited script runs clean under `PYAUTO_SMALL_DATASETS` (or its existing smoke mode) and `notebooks/` are regenerated for the edited scripts.
Review-minutes: 3
Unattended: ready
Epic: cluster-strong-lensing
Phase: 5b
Parent: draft/feature/autolens/point_magnification_api.md
Depends-on: https://github.com/PyAutoLabs/PyAutoLens/pull/798 (phase 5a; new ResultPoint / signed accessors are pending-release — use only the released `LensCalc.magnification_2d_via_hessian_from` in the eleven source_science scripts; the point_source scripts may use the new fit accessors only behind the library-first gate, i.e. after #798 merges, and the PR stays pending-release until that library release).
Filed: 2026-10-23

## Original user request (verbatim)

> Ability to get Magnification at a point in source science scripts, important for clusters
> and then extend to multi plane for clusters. It is common for lens modeling codes to give
> the magnification at a point in the image plane. PyAutoLens may do that but its not
> documented clearly, and should be in all source_science.py examples and the point source
> package.

Human direction 2026-10-23: "make sure this is documented somewhere in autolens_workspace if
users are gonna use it, I guess its source_science but also one of the guides?"

## Bounded phase-5b task (autolens_workspace only)

1. **Eleven `source_science.py` scripts** (`imaging`, `imaging/features/multi_gaussian_expansion`,
   `imaging/features/pixelization`, `group`, `group/features/multi_gaussian_expansion`,
   `group/features/pixelization`, `multi_galaxy`, `multi_galaxy/features/multi_gaussian_expansion`,
   `multi_galaxy/features/pixelization`, `interferometer`, `interferometer/features/pixelization`):
   add one `__Magnification At A Point__` section (after the existing overall-magnification
   section) that (a) explains point magnification = 1/det(A) from the Hessian at an image-plane
   coordinate, its sign = image parity, and that it is distinct from the flux-ratio / area
   magnification computed above; (b) computes it with the existing released API
   `al.LensCalc.from_tracer(tracer=tracer).magnification_2d_via_hessian_from(grid=al.Grid2DIrregular([(y, x), ...]))`
   at two or three chosen coordinates on the lensed arcs; (c) where the script already loads
   `positions.json` (the two pixelization variants), also evaluates it at those multiple-image
   positions; (d) for `group` and `multi_galaxy`, states that all mass profiles in the tracer
   enter the Hessian, mirroring the existing "impact of extra galaxies" paragraph. Add the
   bullet to each script's top-of-file contents/summary list. Supplied coordinates only, never
   a forward `PointSolver` call.
2. **`guides/lens_calc.py`**: add `__Magnification At A Point__` after `__Hessian__` (the
   `magnification_2d_via_hessian_from` call on a `Grid2DIrregular`, sign/parity note, pointer
   to `guides/advanced/multi_plane.py` "Trap (b)" for `plane_j` in multi-plane systems; update
   the `__Contents__` list).
3. **`guides/advanced/multi_plane.py`**: the `plane_j` magnification section already exists;
   add one sentence cross-referencing that point fits and `ResultPoint` apply the same
   `plane_j` selection automatically. No restructuring.
4. **`point_source/fit.py`** (and the results paragraph of `point_source/modeling.py`): one
   short `__Magnification At The Multiple Images__` section printing
   `fit.positions.signed_magnifications_at_positions` and `magnifications_at_positions`, and
   noting `result.signed_magnifications_at_positions` on a finished fit (phase 5a, PyAutoLens#798).
   This item depends on #798 being merged (library-first gate); if it is not merged when this
   task runs, implement items 1–3, leave item 4 out, and say so in the PR.
5. Regenerate the notebooks for every edited script with the workspace's generator; run each
   edited script in its smoke mode and the workspace `smoke_tests.txt` subset that covers them.

Out of scope: library edits, HowToLens, autolens_workspace_test, posterior-draw errors
(phase 7), maps (phase 8), any solver, optimisation, profiling or robustness work.
