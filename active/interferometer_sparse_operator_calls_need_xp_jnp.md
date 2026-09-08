# Interferometer profiling cells break under `jit` after PyAutoArray#544 — pass `xp=jnp`

Type: bug
Target: autolens_profiling
Repos:
- @autolens_profiling
Themes:
- interferometer
- profiling
Difficulty: easy
Autonomy: supervised
Priority: high
Epic: numba-interferometer-revisit
Filed: 2026-09-08
Issued: 2026-09-08
Issue: https://github.com/PyAutoLabs/autolens_profiling/issues/239

Regression surfaced by our own library change, not a user report.

## What broke

PyAutoArray#544 (merged `39d3024c`) gave `InterferometerSparseOperator`'s methods an
`xp=np` parameter so a NumPy fit never imports JAX. Every profiling call site that passes
**traced JAX arrays inside a `jit`** without `xp` therefore now takes the NumPy branch and
dies on `np.asarray(tracer)`.

Reproduced on `main` (7 visibilities, 4x4 extent, `batch_size=4`):

```
no xp   -> TracerArrayConversionError: The numpy.ndarray conversion method __array__()
           was called on traced array with shape int32[20]
xp=jnp  -> ok, (5, 5)
```

## Call sites

| File | Line | Shape |
|---|---|---|
| `scripts/interferometer/likelihood_breakdown/datacube/delaunay.py` | 1011 | `compute_curvature_matrix_sparse` closure, called under `block()` |
| `scripts/interferometer/likelihood_breakdown/delaunay_numba.py` | 433 | `jax.jit(lambda r, c, v: operator.curvature_matrix_diag_from(...))` |
| `scripts/interferometer/likelihood_breakdown/pixelization_numba.py` | 425 | same shape as above |
| `scripts/misc/numba_interferometer/kernels.py` | 544 | `jax_curvature_callable`'s `@jax.jit _curvature` — the pack's JAX arm |

## Fix

Pass `xp=jnp` at each site (all four already import `jax.numpy as jnp` in scope). Sweep
`scripts/interferometer/likelihood_runtime/` and the remaining `datacube/*.py` for the same
call shape — any `sparse_operator.*` method reached with traced arrays needs the kwarg.

Do **not** change the library default: `xp=np` is the correct default for the CPU path
(that is the point of #544), and the JAX arms are the callers that must say so.

## Acceptance

- Every `sparse_operator.*` call that runs under `jit` in this repo passes `xp=jnp`.
- The pack's parity suite (`pytest scripts/misc/numba_interferometer/ -q`) stays green, and
  the JAX arm in `kernels.py` runs rather than raising.
- Named as step 0 of `draft/research/autolens_profiling/interferometer_numba_library_dispatch_insitu.md`;
  that prompt's step 0 can be struck once this lands.
