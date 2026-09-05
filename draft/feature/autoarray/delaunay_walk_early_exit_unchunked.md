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
Status: draft
Consequence: judge
Witness: the A100 Delaunay breakdown's "Triangulation + interpolation" row (26.6 ms, `results/breakdown/imaging/delaunay_hpc_a100_fp64.json`, `--split-setup`) drops to under 8 ms unbatched with `EXPECTED_LOG_EVIDENCE_HST` unchanged, the walk parity tests pass, and the FD certification still passes
Review-minutes: 30
Unattended: ready
Filed: 2026-09-05

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
