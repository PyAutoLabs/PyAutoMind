## einstein-radius-jit-seed-finder
- issue: https://github.com/PyAutoLabs/PyAutoGalaxy/issues/614
- completed: 2026-09-11
- library-pr: https://github.com/PyAutoLabs/PyAutoGalaxy/pull/615
- library-pr: https://github.com/PyAutoLabs/PyAutoLens/pull/735
- pending-release: PyAutoGalaxy@https://github.com/PyAutoLabs/PyAutoGalaxy/pull/615
- pending-release: PyAutoLens@https://github.com/PyAutoLabs/PyAutoLens/pull/735
- summary: |
    `LensCalc.einstein_radius_jit_from` no longer needs a caller-supplied
    `init_guess`. A new private helper `_seed_via_coarse_grid_argmin` evaluates
    the tangential eigen value from the raw Hessian tuple on a coarse uniform
    grid (25x25, ±3" by default), masks non-finite cells (the odd-shaped grid
    puts a cell on the singular isothermal centre) and returns the argmin cell
    as the single Newton seed for `jax_zero_contour.ZeroSolver`. It is
    xp-generic — numpy in the unit tests, `jax.numpy` inside the trace — with
    no skimage and no Python control flow on traced values. `seed_grid_shape`
    / `seed_grid_extent` are exposed so off-centre or cluster-scale callers
    widen the search without leaving the JIT path. The explicit-seed path, the
    `(f, ZeroSolver)` closure cache (#434) and the jax_zero_contour-missing
    soft-fail are unchanged. PyAutoLens' `effective_einstein_radius` latent
    drops its hardcoded ±1" 4-seed fan (PyAutoLens#735, merged after #615).
- verification: |
    PyAutoGalaxy `test_deflections.py` 41 passed (was 37; signature lock
    flipped to `init_guess=None`, new numpy-only tests for centred / off-centre
    / radial seeds and the seedless soft-fail), full suite 1195 passed.
    PyAutoLens `test_latent.py` 37 passed. Ad-hoc JAX script (jax 0.11.1,
    jax_zero_contour 2.0.0): the helper traces under `jax.jit` and returns the
    same cell as numpy; seedless vs fan-seeded Einstein radius on an SIE agree
    to 4.1e-4 relative (1.18849 vs 1.18898; grid method 1.19706); off-centre
    SIE at (2.0, -1.5) with `seed_grid_extent=5.0` gives 0.971 for a 1.0"
    truth; a traced `einstein_radius` scalar round-trips (0.8 -> 0.793, 1.5 ->
    1.494); warm call 0.05 s, cold 4.0 s. CI: 4/4 checks green on each PR.
- traps: |
    (1) The prompt's workspace leg was obsolete before the task started: the
    hardcoded fan had already moved from `euclid_strong_lens_modeling_pipeline/
    util.py` into PyAutoLens `autolens/analysis/latent.py`, so the second PR is
    a PyAutoLens one, not a workspace one; `util.py` has no `init_guess`. (2)
    The declared `Difficulty: too-large` / `Unattended: needs-slicing` did not
    survive the code survey — the Feature Agent proposed a 4-phase split on
    that header; the actual change is one ~40-line helper, an optional
    argument and tests, shipped as two sequenced PRs the same day. Headers
    written at intake can be stale by the time the code is read; size from the
    code. (3) The off-centre model was meant to show the old fan failing. It
    did not: Newton walked onto the off-centre curve from the ±1" fan points
    (1.004 vs the seed finder's 0.971). The seed finder's case is that it
    needs no caller knowledge of where the lens is, not that the fan always
    fails; do not overclaim that in docs. (4) Both target-library files were
    already black-unclean at HEAD under black 26.3.1; a full reformat would
    have folded unrelated churn into the diff, so only added lines were
    black-clean — a hygiene item for `/hygiene`, not this PR. (5) A shallow
    session clone with a single-branch refspec has no `origin/feature/*` ref
    after a successful push, which trips the stop hook's "no remote branch"
    check; widen `remote.origin.fetch` to `+refs/heads/*:refs/remotes/origin/*`.
- notes: |
    Single-seed limitation is documented on both the helper and the method: a
    model with several distinct tangential critical curves is seeded on only
    one; those callers keep passing `init_guess`. Related but separate:
    `draft/refactor/autogalaxy/critical_curves_dispatch_cluster.md` (cluster
    phase 3) still routes the non-jit 25x25 seed scan through skimage — this
    task deliberately left `_init_guess_from_coarse_grid` and the plotter path
    alone. Shipped from a web-github session (session clones, no task
    worktree; Fable architect session, PyAutoGalaxy implementation delegated
    to an Opus subagent, PyAutoLens edit in-session).

## Original prompt

# `einstein_radius_jit_from`: replace static init_guess with a JAX-native seed finder

Type: refactor
Target: PyAutoGalaxy
Themes:
- jax-compile
Difficulty: too-large
Autonomy: supervised
Priority: high
Status: formalised
Consequence: judge
Review-minutes: 25
Unattended: needs-slicing
Filed: 2026-05-21 (backfilled from git)
Issued: 2026-09-11

Small follow-up to the Phase B work (PyAutoGalaxy #435, PyAutoFit #1288,
pipeline #15). Drops the requirement that callers pass a static
`init_guess` to `LensCalc.einstein_radius_jit_from(...)`.

## What `init_guess` does today

`einstein_radius_jit_from(init_guess, ...)` traces the tangential critical
curve using `jax_zero_contour.ZeroSolver.zero_contour_finder`. ZeroSolver
needs **starting positions** for Newton's method — points near the
expected zero-crossing of the tangential eigen-value. From each starting
point ("seed"), Newton iterates onto the curve and then walks along it.
`init_guess` is a JAX array of shape `(n_seeds, 2)` giving `(y, x)` arc-sec
coordinates for those seed points.

In the existing `einstein_radius_via_zero_contour_from` path (non-jit),
the seeds are discovered automatically by `_init_guess_from_coarse_grid`:
evaluate the eigen-value on a coarse 25×25 grid, run `skimage`'s marching-
squares contour finder on the result, take the midpoint of each curve
segment. That approach uses `skimage` which is not JAX-traceable, so it
breaks `compute_latent_samples`' JIT trace — which is why
`einstein_radius_jit_from` requires the caller to provide `init_guess`
explicitly.

In the Euclid pipeline today, the workspace passes a hardcoded 4-seed
fan at ±1 arcsec from origin (`util.py`):

```python
init_guess = jnp.array([[1.0, 0.0], [0.0, 1.0], [-1.0, 0.0], [0.0, -1.0]])
```

This works for the Euclid use case (preprocessed lenses are centred and
have Einstein radii roughly 0.5–2 arcsec, all within Newton's basin from
any of those seeds). It fails for:

- Off-centre lenses (e.g. group / cluster fits where the lens isn't at
  origin).
- Lenses with Einstein radii outside the basin from `(±1, 0) / (0, ±1)`
  (very-strong or very-weak lenses).
- Non-Euclid pipelines that don't know they need to pass `init_guess`.

## What to do

Replace the required `init_guess` with a JAX-native seed finder that
runs inside the jit trace and doesn't need `skimage`.

**Sketch:**

```python
def einstein_radius_jit_from(
    self,
    init_guess=None,
    delta=0.05, N=500,
    pixel_scales=(0.05, 0.05),
    tol=1e-6, max_newton=5,
    seed_grid_shape=(25, 25),
    seed_grid_extent=3.0,
):
    import jax.numpy as jnp

    if init_guess is None:
        # JAX-native seed search: argmin |eigen_value| on a coarse uniform grid.
        # No skimage, no Python control flow that depends on traced values.
        pixel_scale = 2.0 * seed_grid_extent / seed_grid_shape[0]
        grid = aa.Grid2D.uniform(
            shape_native=seed_grid_shape, pixel_scales=(pixel_scale, pixel_scale),
        )
        eigen = self.tangential_eigen_value_from(grid=grid, xp=jnp)
        # Flatten + argmin on |eigen|
        flat_idx = jnp.argmin(jnp.abs(eigen.native if hasattr(eigen, "native") else eigen))
        iy, ix = jnp.unravel_index(flat_idx, seed_grid_shape)
        y = -seed_grid_extent + (iy + 0.5) * pixel_scale
        x = -seed_grid_extent + (ix + 0.5) * pixel_scale
        init_guess = jnp.array([[y, x]])
    init_guess = jnp.atleast_2d(jnp.asarray(init_guess))
    # ... rest of the existing body unchanged
```

**Implementation details to nail down:**

- `tangential_eigen_value_from(grid=grid, xp=jnp)` — verify it threads
  `xp=jnp` correctly all the way down through `convergence_2d_via_hessian_from`
  and `shear_yx_2d_via_hessian_from`. The Euclid validation we did during
  the parent task suggests this should work; double-check by running the
  pipeline's `start_here.py` with the new default.
- `eigen.native` vs raw — `tangential_eigen_value_from` returns an `aa.Array2D`
  under `xp=np` but a raw `jax.Array` under `xp=jnp` (per the existing
  `if xp is np` guard in that function). The helper above should handle
  both shapes.
- Single seed vs fan — `argmin` returns ONE seed (the global minimum).
  For most models that's sufficient (tangential critical curve is
  unique). For pathological models with multiple critical curves we'd
  miss the secondary ones — accept this limitation; multi-curve cases
  can still pass `init_guess` explicitly.
- Seed-grid extent and shape — pick a sensible default. 3 arcsec half-
  width covers Euclid range; cluster fits would need wider. Could expose
  as args (`seed_grid_extent`, `seed_grid_shape`) so callers can override
  without leaving the JIT-friendly path.

## Workspace cleanup

After the library lands, drop the hardcoded init_guess from
`euclid_strong_lens_modeling_pipeline/util.py`. The dispatch becomes:

```python
if self._use_jax:
    effective_einstein_radius = lens_calc.einstein_radius_jit_from()
else:
    effective_einstein_radius = lens_calc.einstein_radius_from(
        grid=self.dataset.grids.lp,
    )
```

## Verification

- Unit test: argmin-based seed matches the `_init_guess_from_coarse_grid`
  result to ~1 grid-cell width on an SIE tracer.
- End-to-end: re-run the Euclid pipeline's JAX-branch latent under
  `PYAUTO_TEST_MODE=1`. The `latent.effective_einstein_radius` value
  should match the Phase B baseline (~2.10 arcsec on the test dataset) to
  reasonable tolerance.
- Cluster check: when an off-centre lens model is used (manually set
  `lens.mass.centre = (2.0, -1.5)` or similar), confirm the new seed
  finder converges. The hardcoded `(±1, 0)` fan would fail this; the new
  default should succeed.

## Out of scope

- Replacing the legacy `_init_guess_from_coarse_grid` skimage call —
  that path stays for the non-JIT `einstein_radius_via_zero_contour_from`
  and the plotter, and is fine where it lives.
- Vmap compatibility — the new helper is still jit-only by design (per
  upstream `jax_zero_contour` ZeroSolver vmap warning).

## References

- PyAutoGalaxy #435 — parent task, added `einstein_radius_jit_from(init_guess, ...)`.
- `complete.md::euclid-einstein-radius-zero-contour` — context on why
  `init_guess` was required in the first place (skimage / find_contours
  blocking the JAX trace).
- `feedback_jax_closure_cache_busts` (memory) — relevant if benchmarking
  the new default's warm-call latency.

<!-- formalised retroactively by the Intake (Conception) Agent on 2026-07-08 -->
