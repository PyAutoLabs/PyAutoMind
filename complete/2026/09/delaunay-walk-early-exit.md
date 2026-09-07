## delaunay-walk-early-exit
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/530 (closed completed 2026-09-07)
- completed: 2026-09-07
- library-pr: https://github.com/PyAutoLabs/PyAutoArray/pull/531 (merged 2026-09-07T23:07Z, `pending-release`)
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace_test/pull/306 (merged)
- workspace-pr: https://github.com/PyAutoLabs/autolens_profiling/pull/224 (merged)
- pending-release: PyAutoArray@https://github.com/PyAutoLabs/PyAutoArray/pull/531
- scope: |
    Phase 1 of the prompt, complete. Phase 2 was deliberately NOT re-filed — see `phase-2` below.
- shipped: |
    `pix_indexes_delaunay_walk_from` (`autoarray/inversion/mesh/interpolator/delaunay.py`) is split into
    `_nearest_vertex_seed_from` — the chunked nearest-vertex argmin, now the *only* chunked stage and still
    the memory guard for the `(chunk, N)` intermediate under `vmap` — and `_walk_from_seed`, a
    `jax.lax.while_loop` over all `Q` queries at once with cond
    `(step < DELAUNAY_WALK_STEPS) & any(~done & ~outside)`. The wrapper's public signature and its
    `return_simplex_indexes` contract are unchanged; `DELAUNAY_WALK_STEPS` is now a safety cap, not a trip
    count. `jax_delaunay` locates the data grid and the `ConstantSplit` split-cross points in one
    concatenated call, so one walk runs per likelihood instead of two. The JAX branch `stop_gradient`s
    `query_points`/`points` (`lax.while_loop` has no reverse-mode rule; the locator returns integer indices
    whose derivative is zero away from measure-zero re-wiring, and every differentiable downstream quantity
    — barycentric weights, dual areas, split points, Sibson weights — is recomputed from the traced
    arrays). The NumPy `scipy_delaunay` path, and therefore the numba CPU likelihood, is untouched by
    construction; `sibson.py` (DelaunayNN) inherits the walk gain but not the concatenation.
    autolens_workspace_test gains `scripts/misc/jax_assertions/delaunay_walk.py`, registered in
    `smoke_tests.txt`; autolens_profiling gains the A100 A/B results and
    `results/notes/delaunay_walk_early_exit.md`.
- witness: |
    PASSED, by 2.1x. The witness was: the params→H prefix of
    `autolens_profiling/results/breakdown/imaging/delaunay_hpc_a100_fp64.json` (`--split-setup`) drops by
    ≥ 18 ms unbatched, `EXPECTED_LOG_EVIDENCE_HST` unchanged, walk parity passes, FD certification passes.
    (The witness line was amended mid-task from "Triangulation + interpolation drops 26.6 → under 8 ms" to
    the params→H prefix; see `caveat` below for why either row alone is no longer interpretable.)
    Measured on `euclid-ral-gpu-2`, jobs 342315–342320, one same-node 14-minute window, control
    `bcd15cd9` vs feature `6152bdf0`, HST / Hilbert-1500 / MGE-60 / `ConstantSplit` fp64, ms per call:
    params→H prefix **45.149 → 7.228 (6.25x, −37.9 ms)**; full pipeline single JIT **93.463 → 60.355
    (1.55x)**; Triangulation+interpolation 30.563 → 5.970; at `vmap` 16 the prefix is 7.555 → 5.139 and the
    full pipeline 41.945 → 39.520. `EXPECTED_LOG_EVIDENCE_HST` unchanged on every leg — 29110.920858
    (Delaunay, 342315/342316) and 29144.581944 (DelaunayNN, 342317/342318), `pinned_drift: []`, nothing
    re-pinned. DelaunayNN, which shares the walk but not the concatenation: 178.971 → 144.789 ms prefix.
- verification: |
    `pytest test_autoarray/` 1452 passed, including 3 new NumPy-only tests in `test_delaunay_walk.py`
    (seed vs `cKDTree.query`; walk converges to `find_simplex` from a deliberately far seed; wrapper
    shapes/dtypes on an odd `Q`). New parity script `delaunay_walk.py` 17/17 PASS (12.8 s direct, 12.4 s
    through `run_python`): exact parity vs `scipy find_simplex` + cKDTree on uniform, blob-ring and
    1,500-vertex production-like lensing meshes for both the data grid and the 4N split points; `jax.jit`
    == eager past the 1,024-wide seed-chunk boundary and on an odd short set; `jit(vmap)` == per-member;
    `jax.grad` runs and matches central FD. FD certification
    `scripts/imaging/jax_grad/delaunay.py` PASSED (rel err 7.4e-6 … 1.1e-3 under rtol 1e-2).
    CPU no-regression gate (the user's constraint): JAX CPU params→H prefix 179.31 → 106.45 ms (1.68x),
    every after-rep below every before-rep, pin PASSED 5/5 both sides; numba control `delaunay_numba.py`
    TOTAL 0.325 → 0.297 s with the pin passing — it never enters the walk.
- caveat: |
    The H row changed meaning with this change. Before it, a breakdown prefix stopping at step 6 never
    asked for the `ConstantSplit` split points, so XLA dead-code-eliminated the second walk out of the
    interpolator prefix and its whole cost landed in the H row's subtraction. With the concatenated locate
    the split walk runs *inside* prefix 6, so H reads 13.555 → 0.225 ms purely by re-attribution and a
    small negative would have been equally legitimate. **Compare `regularization_matrix_prefix_s`
    (params→H) across library versions, never "Triangulation + interpolation" or "H" alone.** Recorded in
    the breakdown script's docstring in autolens_profiling#224. The NumPy/scipy path still charges the
    split walk to H.
- phase-2: |
    Deliberately NOT re-filed, and not backlog. Phase 2 of the prompt (static image-plane seed + one-shot
    fan test, Mapper/AdaptImages plumbing) was gated on Phase 1 leaving the row above a few ms; it does
    not. After this PR the Delaunay params→H prefix is 7.23 ms unbatched and **5.14 ms per call at
    `vmap` 16 — ~13% of the 39.5 ms batched per-evaluation cost** — so Phase 2's remaining headroom on
    this cell is a few ms per call for a change that reaches into Mapper/AdaptImages plumbing.
    The cheaper cut is the one Delaunay just took, applied to DelaunayNN, which still spends 144.8 ms
    unbatched / 24.4 ms per call at `vmap` 16 in the same prefix because `sibson.py:522` / `:648` still
    call `pix_indexes_delaunay_walk_from` twice. Filed instead as
    `draft/feature/autoarray/sibson_single_concatenated_walk.md`.
- follow-ups: |
    - `draft/feature/autoarray/sibson_single_concatenated_walk.md` — concatenate sibson.py's two walk
      calls (the DelaunayNN half of this gain).
    - The breakdown script's H-row attribution is documented, not fixed; a cleaner per-stage attribution
      for `--split-setup` remains open in autolens_profiling.
- traps: |
    - `lax.while_loop` has no reverse-mode rule: the locator must `stop_gradient` its float inputs, and
      under `vmap` the loop runs to the slowest lane in the batch (so batched wins are smaller than
      unbatched ones — 1.47x vs 6.25x here).
    - A profiling row can change *meaning* without changing code in the profiler: dead-code elimination
      decides which prefix a cost is charged to. An A/B on a single breakdown row is only valid if the
      prefix boundaries still mean the same thing on both sides.
    - The A/B legs deliberately did not touch the shared `/mnt/ral/jnightin/PyAuto` install (live
      subhalo-validation and Euclid DR1 CPU runs were on it); each leg prepended its own PyAutoArray
      checkout to `PYTHONPATH` and printed `autoarray.__file__` + `git rev-parse HEAD` into its SLURM log.
- heart-ack: 2026-09-07 in-session, YELLOW with no RED reasons — "workspace validation not passing (5 failed, 2 timeout, cloud#34099198772)" plus stale "release validation incomplete: no rehearsal for current source"; organism-scope, and the failing autolens_test delaunay legs do not exercise the walk and were already fixed on autolens_workspace_test main that day (078e445, 4103234).
- notes: |
    Source of truth for every number above:
    `autolens_profiling/results/notes/delaunay_walk_early_exit.md` (on main via #224), plus the
    A100 verification comment on PyAutoArray#530.

## Original prompt

# JAX Delaunay point location: early-exit walk, unchunked loop, static image-plane seed

Type: feature
Target: autoarray
Repos:
- PyAutoArray
- autolens_profiling
Themes:
- jax-gpu
- delaunay
- profiling
- performance
Difficulty: medium
Autonomy: supervised
Priority: high
Status: active
Consequence: judge
Witness: the A100 Delaunay breakdown's params→H prefix (`--split-setup`, `results/breakdown/imaging/delaunay_hpc_a100_fp64.json`; Tri+interp + H row sum, since the single concatenated walk moved the split-point walk into the Tri+interp prefix) drops by at least 18 ms unbatched (baseline Tri+interp 26.6 ms → target under 8 ms equivalent) with `EXPECTED_LOG_EVIDENCE_HST` unchanged, the walk parity tests pass, and the FD certification still passes
Review-minutes: 30
Unattended: ready
Filed: 2026-09-05
Issued: 2026-09-07
Issue: https://github.com/PyAutoLabs/PyAutoArray/issues/530

Original request (verbatim):

> give me a prompt to work on this Target 1: point location is a fixed-trip loop over chunks

## The measurement

On the A100 the HST Delaunay imaging likelihood (1500 Hilbert vertices, 15,361 data
pixels, MGE-60 lens, ConstantSplit) costs 97 ms per evaluation, of which the four-way
`--split-setup` decomposition attributes 26.6 ms to "Triangulation + interpolation"
(`autolens_profiling/results/notes/preopt_breakdown_baseline.md`). The qhull host callback
is a few ms of that at most (1500 points, `pure_callback`, `vmap_method="sequential"`). The
rest is the JAX-side point location in
`PyAutoArray/autoarray/inversion/mesh/interpolator/delaunay.py`,
`pix_indexes_delaunay_walk_from`, and it is latency, not FLOPs:

- The walk is `jax.lax.fori_loop(0, DELAUNAY_WALK_STEPS, ...)` with
  `DELAUNAY_WALK_STEPS = 128` (module constant at line 75, loop at line 252). A fixed-trip
  `fori_loop` cannot exit early. Seeded from the nearest vertex the walk resolves in a
  handful of steps, so well over 95% of the 128 iterations are no-ops that still launch a
  gather, a cross-product batch, an argmin and three `where`s each.
- Queries are processed in chunks of `DELAUNAY_LOCATE_CHUNK = 1024` (line 69) through
  `jax.lax.map` (line 279), which is sequential: 16 chunks for the data grid and 6 more for
  the 6000 ConstantSplit split-cross points (`jax_delaunay` calls the walk twice). That is
  roughly 22 x 128 = 2,800 dependent walk steps per likelihood.
- The chunking exists only to bound the `(chunk, N)` nearest-vertex distance intermediate
  under `vmap` (184 MB per replica at full Q; ~12 GB at batch 64). It is a memory guard
  that happens to serialise the latency-bound part.

Nautilus at `n_batch=256` gave 51 ms per eval against 62 ms at `n_batch=16`, so batching
barely amortises this today. `DelaunayNN` (`interpolator/sibson.py`) seeds its cavity walk
from `pix_indexes_delaunay_walk_from(..., return_simplex_indexes=True)`, so it inherits
every gain here. `interpolator/knn.py` is a separate approach and out of scope.

## Phase 1: early exit, and chunk only the argmin

1. Replace the `fori_loop` with a `jax.lax.while_loop` whose predicate is
   `(step < DELAUNAY_WALK_STEPS) & jnp.any(~done & ~outside)`. The 128 cap stays as the
   safety bound; the typical exit is under ten steps. Under `vmap` the loop runs to the
   slowest lane, which is fine.
2. Split the two jobs the chunk loop currently does. Keep the nearest-vertex argmin
   chunked (it is the memory hazard, and a `lax.map` over 16 single-argmin chunks is cheap),
   then run the walk once over all Q queries with no `lax.map`. The walk's working set is
   O(Q), not O(Q x N).
3. Keep the NumPy path (`xp is np`, used by the unit tests) behaviourally identical; it
   already early-exits.
4. Prove parity: the JAX walk must return the same `(Q, 3)` mappings and simplex indexes as
   `scipy.spatial.Delaunay.find_simplex` on the existing test meshes and on a 1500-vertex
   Hilbert mesh traced through a few mass models (reuse the geometry from
   `autolens_profiling/scripts/misc/jax_assertions/delaunay_nn_caps.py`). Points exactly on
   a shared edge may legitimately resolve to either adjacent triangle; the barycentric
   weights agree because the opposite vertex gets weight zero, so compare mapping matrices,
   not triangle ids, in that case.

## Phase 2: static image-plane seed and one-shot fan test

The image-plane mesh is fixed per fit by the adapt image, and ray tracing is continuous
away from critical curves, so each data pixel's nearest image-plane mesh vertex is a
near-perfect source-plane seed. Precomputing that index once per fit (in the `Mapper` /
`AdaptImages` layer, where `image_plane_mesh_grid` is known) removes the brute-force
`(Q, N)` argmin and its memory hazard entirely, which also retires the chunking. Then have
the qhull callback also return a padded vertex-to-incident-triangle table (cap around 12,
audit the actual max the way `delaunay_nn_cap_audit.md` did) so most queries resolve with
one vectorised barycentric test over the seed's fan; the `while_loop` walk from Phase 1
handles only the residual near critical curves and outside the hull. Split-cross points
have no image-plane parent pixel; seed them at their parent vertex (they are offsets from
it) and let the fan test cover them.

Phase 2 changes the interpolator's inputs (a seed array), so it touches
`InterpolatorDelaunay`, `InterpolatorDelaunayNN`, the `Mapper` constructor path and
`FitImaging` plumbing. Land Phase 1 first and re-measure; Phase 2 is only worth its
plumbing if Phase 1 leaves the row above a few ms.

## Gradient contract (do not relax)

Point location is integer-valued; its derivative is zero almost everywhere and it is
already wrapped by `stop_gradient` semantics through the frozen connectivity tables
(`_jax_delaunay_tables` docstring). The barycentric weights are recomputed from the traced
points after location exactly as now, so `jax.grad` through the likelihood is unchanged.
Re-run the FD certification `autolens_workspace_test/scripts/imaging/jax_grad/delaunay.py`
after each phase.

## Verification on the A100

Use the `delaunay-nn-breakdown` tooling (autolens_profiling#219): rerun
`scripts/imaging/likelihood_breakdown/delaunay.py --config-name hpc_a100_fp64
--split-setup --vmap-batch 16` and the `delaunay_nn.py` sibling from a RAL worktree with
`HPCPullPyAuto` pointed at the feature branch. Report the four-way split unbatched and per
call under vmap, the H row, and the single-JIT runtime cell, against the 2026-09 baselines.
Pins (`EXPECTED_LOG_EVIDENCE_HST` in both scripts) must pass unchanged; a shift means a
mapping changed and is a bug, not a re-pin. Note the symmetric knife-edge lesson from
PyAutoLens#721: if a positions-threshold or point-solver pin elsewhere moves, bisect
before re-pinning.
