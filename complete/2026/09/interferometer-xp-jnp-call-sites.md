Regression fix: the four `autolens_profiling` call sites that reach
`InterferometerSparseOperator.curvature_matrix_diag_from` with traced JAX arrays under
`jax.jit` now pass `xp=jnp`.

## Why it broke

PyAutoArray#544 (merged `39d3024c`, this session) gave the sparse operator's methods an
`xp=np` parameter so a NumPy fit never imports JAX. That default is a *behaviour switch*, not
an additive parameter: every caller that relied on the old unconditional JAX backend was
re-routed to the NumPy branch, which calls `np.asarray` on a tracer and raises
`TracerArrayConversionError`. PyAutoArray's own 1486 tests and all three CI legs were green —
the breakage lived entirely in this sibling repo.

## Sites fixed

| File | Site |
|---|---|
| `scripts/interferometer/likelihood_breakdown/datacube/delaunay.py` | `compute_curvature_matrix_sparse` |
| `scripts/interferometer/likelihood_breakdown/delaunay_numba.py` | jitted lambda |
| `scripts/interferometer/likelihood_breakdown/pixelization_numba.py` | jitted lambda |
| `scripts/misc/numba_interferometer/kernels.py` | `jax_curvature_callable` |

A repo-wide sweep confirmed these are the only `sparse_operator.*` calls in `scripts/`.

## Verification

- Root cause reproduced on `main`: `TracerArrayConversionError` without the kwarg, correct
  array with it.
- `pytest scripts/misc/numba_interferometer/ -q` → 35 passed.
- The pack's JAX arm now runs and matches `curvature_fft_numpy` at `max|Δ| = 7.11e-15` on
  peak `9.82e+01` (on a valid symmetric preload; a random preload disagrees only because the
  library symmetrises `0.5*(C + Cᵀ)` and the reference does not).
- `AUTOLENS_PROFILING_SMOKE=1` exits 0 on both breakdown scripts; `datacube/delaunay.py`
  compiles; `lint` green.

## Decisions

- The library default stays `xp=np` — that is the point of #544, and the JAX arms are the
  callers that must say so.
- `black` was deliberately **not** run: these files are not black-clean on `main` and this
  repo's CI does not enforce it, so a formatter pass turned a 20-line fix into ~180 lines of
  churn on the first attempt and was reverted.
- Incidental `results/simulators/interferometer_sma_summary_*` regeneration (timing noise from
  running the pack tests in a fresh worktree) was reverted, not committed.

Closes the last loose end of the retired epic `numba-interferometer-revisit`; it was step 0 of
`draft/research/autolens_profiling/interferometer_numba_library_dispatch_insitu.md`, now
struck. Upstream: PyAutoArray#542 / PR #544.

- heart-ack: 2026-09-08 in-session, reasons "workspace validation not passing (5 failed, 2 timeout, cloud#34099198772 …)" and "release validation incomplete: no rehearsal for current source" — organism-scope, neither names autolens_profiling nor these tests

## Original prompt

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
