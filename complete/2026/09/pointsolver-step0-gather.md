# Point-source (single-source) CPU speed-up campaign — phase 4b: step-0 containment without the (N,3,2) triangle gather

Phase 4b replaced the JAX PointSolver's step-0 `vertices[indices]` materialisation with a structured containment test on the static lattice. It shipped whole: a library change in PyAutoArray plus a data PR in autolens_profiling. The follow-ups it leaves are carried in `draft/research/autolens_profiling/pointsolver_cpu_speed_campaign_remainder.md`.

- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/579
- completed: 2026-09-27
- parent: complete/2026/09/point-source-cpu-p4.md (phase 4a; was `active/pointsolver_cpu_speed_phase_4.md`, issue autolens_profiling#314)
- library-pr: https://github.com/PyAutoLabs/PyAutoArray/pull/580
- workspace-pr: https://github.com/PyAutoLabs/autolens_profiling/pull/330
- pending-release: PyAutoArray@https://github.com/PyAutoLabs/PyAutoArray/pull/580

## Shipped

- The human ran `/prm` on 2026-09-27 and both PRs merged:
  - [PyAutoArray#580](https://github.com/PyAutoLabs/PyAutoArray/pull/580) merged at `4383ea81a06aea5820c950386b5bcf294dc9929b` (branch head `c13b2d73`). It is labelled `pending-release`, so it is **not yet released**.
  - [autolens_profiling#330](https://github.com/PyAutoLabs/autolens_profiling/pull/330) merged at `81af10f7505a9fda97aebdd6aed4f65b510cf9ab` (branch head `cc46e659`).
  - At close-out, both branch heads were proven ancestors of `origin/main`.
- **Library:** four step-0 containment routes sit behind the module switch `array._STEP0_CONTAINMENT`. The default is `structured`, and all four routes are bit-identical on every route tested. The PR also fixes the WIP bug (`type(shape) is Point`).
- **Tests:** a step-0 route bit-identity fuzz, refinement tests and an HLO guard (no `(N,3,2)` gather), each red on main before the fix. Suites: PyAutoArray 1732 passed, PyAutoLens 758 passed + 1 xfail. Targeted smoke 31/31.
- **autolens_profiling:** the harness gained `--step0-route`, instrument fixes and a backend-aware fiducial, plus laptop, EPYC, A100 and RAL 8490H rows and a "Phase 4b" ledger section. The WALL-BASIS rows of the step-0 submits were fixed after the first lint run went red.

## Evidence

- **Quotable row: RAL Xeon 8490H, job 357321, CPU fp64.** `structured` against the gather:
  - 1.44x faster on a single call and 2.27x at vmap-16
  - containment time −60 %
  - compile time +8.6 %
  - temp memory −47 %
  - `all_gates_pass`
  - The node was loaded (load ~200), so compare ratios, not absolute ms, against phase 4a.
- **Supplementary rows:** EPYC 1.62x; A100 1.00x (no change on GPU); laptop 1.38x.
- **Heart:** YELLOW twice with no RED: first for manifest drift, then for a stale/incomplete rehearsal. The human acknowledged it both times.

## Follow-ups (carried in the remainder draft)

- `nopad` is dead weight in `_STEP0_CONTAINMENT` and can be deleted in a later library cleanup.
- The RAL scratch copies `/mnt/ral/jnightin/autolens_profiling_wt/pointsolver-step0-gather` and `/mnt/ral/jnightin/autolens_profiling_wt/PyAutoArray_pointsolver-step0-gather` were deliberately left in place.
- A quiet-node 8490H re-run is needed if absolute ms against phase 4a are ever wanted.

## Original prompt

# Point-source CPU speed-up phase 4b — cut the step-0 triangle gather / containment in the JAX PointSolver

Type: feature
Target: autoarray
Repos:
- PyAutoArray
- PyAutoLens
- autolens_profiling
Themes:
- point-source
- profiling
- jax-compile
Difficulty: medium
Autonomy: supervised
Priority: high
Status: formalised
Consequence: judge
Review-minutes: 20
Unattended: ready
Epic: point-source-cpu-speed
Filed: 2026-09-26
Issued: 2026-09-26
Issue: https://github.com/PyAutoLabs/PyAutoArray/issues/579
Parent: complete/2026/09/point-source-cpu-p4.md (was active/pointsolver_cpu_speed_phase_4.md; issue autolens_profiling#314)

## Goal

Remove, or sharply cut, the **≈ 0.9 ms `vertices[indices]` materialisation at step 0** of the JAX
`PointSolver`. On the released code it is ≈ 49 % of the single-source likelihood. This is a pure
code lever. The solver geometry (±9.9″ / 0.2″ / 1e-3, `MAX_CONTAINING_SIZE` 15) does **not**
change, and the result must stay **bit-identical**:

- image sets and counts;
- the fiducial simple solved log L `7.743201200876812`;
- `jax.grad`;
- `vmap`.

Human decision (2026-09-26): this is phase 4b, first of the phase-4a follow-ups.

## Evidence (phase 4a, RAL CPU, Xeon 8490H `euclid-ral-compute-10-4`, 8 CPUs, fp64, JAX 0.10.2)

Ledger: `lens/autolens_profiling/results/notes/point_source_cpu_campaign.md`, section "Phase 4a".

- **Re-baseline, job 356365** (`results/breakdown/point_source_image/image_plane_hpc_ral_cpu_fp64_p4.json`,
  5 runs): fused solved median 2.095 ms. Step 0 is **66 %** of the call. Refinement steps 1–7 are 15 %,
  β\* 8 %, magnification 7 % and χ² 4 %. The phase-3 FLOP estimate (refinement ≈ 60 %) was wrong in
  wall time. That cell's own step-0 "ray trace vs containment" split counts the gather as trace, so
  do not quote it.
- **Sweep, job 356367** (`results/breakdown/point_source_image/solver_config_sweep_hpc_ral_cpu_fp64.json`,
  key `step0_split.control`): the control is 1.824 ms and step 0 is 1.48 ms (81 %). It divides into:
  - ray trace of the 11 859 static-lattice vertices: **0.27 ms**;
  - containment: **1.21 ms** (66 % of the likelihood). This is `containing_indices`: the gather +
    `Point.mask` + `jnp.where`.
  - Of the containment, the gather that materialises the `(23 283, 3, 2)` triangle array alone is
    **≈ 0.90 ms** (`triangle_materialisation_ms`).
- Under ±2.5″/0.4 (243 rows), containment is 0.06 ms, which shows how much of the cost is the
  23 283-triangle size of the lattice.
- **Why this lever over shrinking the grid:** it recovers most of the extent/scale speed-up (the
  best admissible config, ±2.5/0.4, was 2.37× and 5.55× at vmap-16) with **no completeness risk and no
  default change**. The extent became a workspace choice, per `draft/feature/autolens/pointsolver_extent_sanity_check.md`
  and `draft/feature/autolens_workspace/pointsolver_grid_extent_per_package.md`.
- Revisions measured: PyAutoArray `3de624b5`, PyAutoLens `86054bbc`, autolens_profiling `6c45fec`.
  The point-source path is byte-identical to 2026.9.26.1.

## Candidate mechanisms (choose by measurement)

1. **Exploit the regular step-0 lattice.** Step 0 is the static phase-3 lattice
   (`static_vertex_table`, PyAutoArray `autoarray/structures/triangles/coordinate_array.py`; wired in
   PyAutoLens `AbstractSolver._initial_triangles`). Each triangle's vertices are fixed offsets into
   the lattice. Compute containment by row/column arithmetic or strided slicing of the traced
   vertex table instead of the fancy-index gather. For example, evaluate the barycentric / sign test
   on the up- and down-triangles of each lattice row as two dense slices.
2. **A fused containment kernel.** Do the sign test on the index arrays directly, so XLA never
   materialises the `(N, 3, 2)` array. Check the optimised HLO for the gather's disappearance.
3. Anything else that removes the materialisation while keeping the kept set **bit-identical**.
   Beware: phase 3's tie study showed that a changed float path at step-0 vertices moves the kept set.
   Pin the tie test `test_static_lattice_jax.py::test__source_on_a_step_0_vertex_returns_the_two_true_images`.

## Protocol (as phase 3)

- A red control on main, then an **interleaved A/B**: fresh closures + `jax.clear_caches()`,
  20 rounds × 20 calls, rotated round-robin, bootstrap 90 % CI.
- The harness is `lens/autolens_profiling/scripts/point_source_image/likelihood_breakdown/solver_config_sweep.py`.
  Its `step0_split` prefixes (source centre / `jnp.sum(plane.vertices)` / materialised triangles /
  `containing_indices`) are the before/after instrument, and its 200 prior + 200 stress completeness
  draws are the regression set. Add a library route beside `control`.
- Gates: bit-identical log L on the stream and on the fiducial, positions, image counts, grad, and
  vmap 1 / 4 / 16. Also compile no worse than +20 %, and no memory regression.
- RAL CPU pinned to an 8490H node (check `sinfo -p ral -N -o "%N %T %C"`; `idle*` nodes are
  unreachable), plus **an A100 no-regression row**. The A100 is launch-bound (phase 3), so expect ~1×.
- Library-first ship: PyAutoArray → PyAutoLens → autolens_profiling data PR.

## Traps

- **PyAutoArray is currently claimed by task `interferometer-transform-real-scatter`.** Check the
  claim at `start_dev` (run `worktree_check_conflict`, not a grep). A parallel claim is fine only if
  the file sets are disjoint.
- JAX caches jaxprs on function identity. A monkeypatch A/B needs a distinct function object and
  `jax.clear_caches()` before each compile.
- `jax.grad` through an `AnalysisPoint` needs `autofit.jax.register_model(model)`; without it the
  gradient is silently all-zero.
- Fix, or at least do not quote, `image_plane.py`'s step-0 prefix split. It counts the gather as ray
  trace.
