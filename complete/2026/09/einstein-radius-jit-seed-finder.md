- issue: https://github.com/PyAutoLabs/PyAutoGalaxy/issues/614
- completed: 2026-09-11
- library-pr: https://github.com/PyAutoLabs/PyAutoGalaxy/pull/615
- library-pr: https://github.com/PyAutoLabs/PyAutoLens/pull/735
- merged: PyAutoGalaxy 6459e1d (PR #615), PyAutoLens ae64a65 (PR #735) — library-first order honoured (#615 then #735, both 2026-09-11)
- pending-release: PyAutoGalaxy@https://github.com/PyAutoLabs/PyAutoGalaxy/pull/615
- pending-release: PyAutoLens@https://github.com/PyAutoLabs/PyAutoLens/pull/735
- closed-out: 2026-09-11 from a web session (`/prm` on the MCP surface; no task worktree — session clones only)

**Summary.** `LensCalc.einstein_radius_jit_from` no longer needs a caller-supplied `init_guess`. A private helper (`_seed_via_coarse_grid_argmin`) evaluates the tangential eigen value on a coarse uniform grid (25×25, ±3 arcsec by default) straight from the raw Hessian tuple inside the JIT trace, masks non-finite cells and takes the cell of minimum `|eigen value|` as the single Newton seed. `seed_grid_shape` / `seed_grid_extent` are exposed so cluster fits can widen the search without leaving the traceable path; an explicit `init_guess` still works unchanged. PyAutoLens then dropped the hardcoded 4-seed fan at ±1 arcsec from `autolens/analysis/latent.py::effective_einstein_radius` (and its `jax.numpy` import) and calls the seedless form.

**Scope shipped vs filed.** The prompt's third leg — dropping the same fan from `euclid_strong_lens_modeling_pipeline/util.py` — is obsolete, not deferred: that fan had already migrated into PyAutoLens's latent, which is where #735 removed it. Nothing remains to re-file. The Feature Agent's 4-phase split was overridden: the whole change is ~40 lines plus tests, so the header difficulty is re-sized `medium` here.

**Verification (from the PR bodies).** PyAutoGalaxy: `test_autogalaxy/.../deflections` 41 passed (was 37); full suite 1,195 passed; JAX and numpy paths agree on centred and off-centre lenses; soft-fail case exercised. PyAutoLens: `test_autolens/analysis/test_latent.py` 37 passed (the latent stubs `LensCalc`, so the real JIT path is exercised only downstream). Remaining witness: once both libraries release, the Euclid pipeline's `tests/test_compute_latent_variable.py::test_effective_einstein_radius` re-validates the latent against the Phase B baseline (~2.10 arcsec under `PYAUTO_TEST_MODE=1`).

**Traps / notes.**
- **Release ordering is real, not label theatre.** #735 against a PyAutoGalaxy without #615 raises `TypeError` from the seedless call, and the latent's `except (ValueError, AttributeError)` does not catch it. Unit tests cannot see this (they stub `LensCalc`). The two `pending-release` lines above carry that obligation until `/review_release` clears them on a release that shipped both.
- `argmin` yields one seed, so a model with several critical curves finds only the global minimum. Accepted by design; multi-curve callers pass `init_guess` explicitly.
- Not released as of close-out: the nightly of 2026-09-11 is the first that can carry both merges; the two prior nights stopped at Stage 3 on a stale `test-results/` committed by autolens_workspace_test#311 (fixed by awt#313 on the workspace side and guarded durably by PyAutoHeart#225, see `complete/2026/09/release-integrate-discard-stale-result-files.md`).

**Follow-ups.** None filed. `draft/refactor/autogalaxy/critical_curves_dispatch_cluster.md` cites this task as the JAX-native seed-finder precedent; its reference is repointed to this record in the same close-out commit.

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
