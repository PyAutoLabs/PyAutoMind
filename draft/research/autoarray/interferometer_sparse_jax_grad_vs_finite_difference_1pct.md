# Sparse interferometer inversion: jax.grad of the log-evidence terms w.r.t. the regularization coefficient differs from a central finite difference by 1.3 % (UNVERIFIED — may be the FD step choice)

Type: research
Target: autoarray
Repos:
- @PyAutoArray
Themes:
- interferometer
- jax-grad
- pixelization
Difficulty: small
Autonomy: supervised
Priority: low
Status: formalised
Consequence: glance
Witness: A sweep of the central finite-difference step (1e-3 .. 1e-8) and PRNG / fixture seeds on the repro below shows either the grad-vs-FD gap collapsing to < 1e-6 relative at some step (then close as FD-step artefact, record the step), or a persistent gap attributable to a named term (fast_chi_squared, regularization_term, log_det_curvature_reg_matrix_term, log_det_regularization_matrix_term — differentiate each separately) with the responsible op identified.
Review-minutes: 3
Filed: 2026-09-27

## Finding (unverified)

Seen 2026-09-27 while verifying PyAutoArray#581 / PR #582 (cache curvature_matrix / data_vector on
the interferometer inversions). The gap is **pre-existing**: it is bit-identical on PyAutoArray
main 14d63360 (before the change) and on the PR branch, so the caching change did not cause it.
It may well be nothing more than the FD step choice (eps = 1e-5, single step, not swept) or the
positive-only solver's active set making the objective only piecewise-smooth in the coefficient.

- jit value 138.40994245566733; vmap over coeff [0.5, 1.0, 2.0] consistent with jit
- jax.grad = 0.010915517807006836, central FD (eps 1e-5) = 0.010776940939649647 → rel gap 0.01286

## Repro (scratch script, JAX_PLATFORMS=cpu, jax_enable_x64)

- `aa.Mask2D.circular(shape_native=(12, 12), pixel_scales=1.0, radius=4.0)`, 64 visibilities,
  `rng = np.random.default_rng(11)`: data `rng.normal(size=(64, 2))`, unit noise,
  uv `rng.normal(size=(64, 2))`, `TransformerDFT`.
- `dataset.apply_sparse_operator(nufft_precision_operator=dataset.psf_precision_operator_from(method="numpy"), use_jax=True)`.
- `RectangularUniform(shape=(4, 4))` interpolator on `overlay_grid_from(shape_native=(4, 4), grid=grid.over_sampled)`,
  `xp=jnp`; `Mapper(regularization=aa.reg.Constant(coefficient=c), xp=jnp)`.
- `inv = aa.InversionInterferometerSparse(dataset=..., linear_obj_list=[mapper], xp=jnp)`;
  f(c) = `fast_chi_squared + regularization_term + log_det_curvature_reg_matrix_term - log_det_regularization_matrix_term`.
- Compare `jax.jit(jax.grad(f))(1.0)` against `(f(1+eps) - f(1-eps)) / (2 eps)`, eps = 1e-5.

## What

Sweep the FD step and differentiate each term separately; check whether the reconstruction's
positive-only active set changes across [c - eps, c + eps]. Close as FD artefact if the gap
collapses; otherwise route the named term to a bug prompt.
