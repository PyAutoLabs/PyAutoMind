# Final numerics audit of every mesh interpolator

Type: test
Target: autoarray
Repos:
- PyAutoArray
- autolens_workspace_test
Difficulty: large
Autonomy: supervised
Priority: high
Status: formalised
Filed: 2026-08-26

One last systematic round of numerics testing across **every** `@PyAutoArray`
mesh interpolator, to establish that no further bugs of the class
`PyAutoArray#490` exposed are still hiding.

## Why now

#490 found that `InterpolatorRectangular` had mirrored bilinear **row** weights
for ~11 months, and that a 1-ULP change could flip a cell assignment because
`ix_up = ceil(g)` collapsed on the CDF's clip plateau. Neither was caught by the
existing suite. The reason is the important part:

- **Partition of unity held throughout.** Weights summed to 1 to 2.2e-16 in
  every broken version, so any plausibility check passed.
- **The mirroring was *consistent*,** so the likelihood surface stayed smooth
  and every FD/AD gradient check passed.
- **Likelihood is nearly blind to it.** With a pixelized source the inversion
  solves for the source values, so a geometrically wrong mapping is still a
  valid basis — the solved-for source absorbs the error.

It took a 1-ULP eager/jit divergence in a different repo to expose it. That is
not a reproducible detection strategy, which is why this audit is worth doing
deliberately rather than waiting for the next accident.

## The tests that DO discriminate (validated in #490)

These caught every broken historical version and are the template:

1. **Linear reproduction.** `sum_i w_i * node_i == query`, in index space. A
   correct bilinear scheme is exact for linear functions; any *consistent*
   mis-pairing satisfies partition of unity but fails this. Measured: the
   pre-#490 code failed by 0.999968 in the row axis while the column axis was
   exactly 0.000000 — the asymmetry immediately localises the defect.
2. **Continuity across integer boundaries.** Sweep a coordinate across every
   interior cell boundary; the interpolant must not jump. Measured: pre-#490
   jumped by 5.999 (a two-row flip).
3. **Convergence under refinement.** Interpolate a smooth function and refine
   the mesh; error must fall (~O(h²) for bilinear). Query **where the data is**,
   not uniformly — an adaptive mesh deliberately leaves sparse regions coarse,
   and judging it there measures the wrong thing.
4. **Ground-truth source recovery.** Where a truth source exists, compare the
   reconstruction against it (Pearson r, normalised RMS). This is the only
   measure that discriminated correct from mirrored on physical data.
5. **Known-good control.** Run the same harness against an interpolator not
   under test (`rectangular_uniform.py` served this role) and require it to be
   **bit-identical** across the change — it proves the harness isolates what it
   claims to.

## Scope — every interpolator

`autoarray/inversion/mesh/interpolator/`:

- `rectangular.py` — `InterpolatorRectangular` (**done** in #490; include it so
  the suite is uniform)
- `rectangular_uniform.py` — `InterpolatorRectangularUniform`
- `delaunay.py` — `InterpolatorDelaunay` (note: the only `jax.pure_callback`
  family in the chain — qhull triangulation)
- `delaunay_nn.py` — `InterpolatorDelaunayNN`
- `sibson.py` — natural-neighbour
- `knn.py` / KNN barycentric — `InterpolatorKNearestNeighbor`

For each: which of tests 1-5 apply (barycentric schemes reproduce linears too;
nearest-neighbour does not, so it needs a different invariant), then implement
and land the applicable ones as permanent regression tests.

## Specific suspicions worth checking first

- **Any `floor`/`ceil`/`argmin`/`searchsorted` on a value that can land exactly
  on a boundary.** #490's trigger was `clip(F_q, 0, 1)` manufacturing exactly
  integer indices *systematically*. Look for other saturating transforms feeding
  a discretisation.
- **Corner/weight pairing in every barycentric or bilinear scheme** — the #490
  defect was purely a pairing error, invisible to partition of unity.
- **`KERNEL_CDF_DEFAULT_KNOTS = 64` does not scale with `mesh_pixels`.**
  Measured in #490: the knot-table inverse that places mesh nodes drifts from
  the exact forward transform as the mesh refines — max `|g_roundtrip - ix|` was
  0.0055 (n=16), 0.0238 (n=32), **0.101** (n=64) index units. Harmless at
  production mesh sizes but wrong in principle; decide whether `n_knots` should
  scale.
- **Guard-node conventions.** `grid_over_index ∈ [1, n-2]` means flat rows 0-1
  and cols 0, n-1 are never referenced. Confirm every interpolator agrees with
  its mesh geometry about which nodes are live — a mismatch there is exactly the
  kind of silent off-by-one this audit is for.

## Acceptance

- Each interpolator has permanent tests for whichever of 1-5 apply to it.
- Every new test is demonstrated to **fail** against a deliberately-broken
  variant — a regression test that passes either way is worthless, and that is
  precisely how the #490 defect survived a commit literally named
  "fixed mappings and weights".
- Any bug found is filed separately; this task is the audit, not the fixes.

## Related

- `PyAutoArray#490` — the fix and its regression tests (the template).
- `autolens_workspace_test#279` — how it surfaced.
- `draft/test/workspaces/mesh_magnification_correctness.md`
- `draft/test/workspaces/physical_model_check_when_speeding_up_smoke.md`

<!-- formalised by the Intake (Conception) Agent on 2026-08-26 from user-intake -->
