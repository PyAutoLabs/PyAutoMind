# Re-measure the numba interferometer crossover in situ, through the library dispatch

Type: research
Target: autolens_profiling
Repos:
- autolens_profiling
Themes:
- numba-cpu
- interferometer
- profiling
Difficulty: medium
Autonomy: supervised
Priority: medium
Status: formalised
Consequence: judge
Review-minutes: 20
Unattended: ready
Epic: numba-interferometer-revisit
Filed: 2026-09-08

Workspace half of `interferometer-numba-cpu-direct-conv` (PyAutoArray#543, library PR
#545, stacked on #544). The library now ships the `direct_conv` kernel as
`InversionInterferometerSparseNumba`, selected by `inversion_interferometer_from` when
`xp is np`, the preconditions hold, and the mapper's mean non-zeros per source column is
at or below `Settings.interferometer_numba_nnz_per_source_max` (default `60.0`).

## Step 0 — required fix before any measurement

`autolens_profiling/scripts/interferometer/likelihood_breakdown/datacube/delaunay.py:1011`
calls

```python
return sparse_operator.curvature_matrix_diag_from(rows=rows, cols=cols, vals=vals, S=S)
```

inside `compute_curvature_matrix_sparse`, which is handed to `jit_profile` with traced
JAX arrays and **no `xp` argument**. Since PyAutoArray#544 the method's signature is
`curvature_matrix_diag_from(self, rows, cols, vals, *, S, xp=np)` and the default takes
the NumPy branch, which fails on `np.asarray(<tracer>)`. Pass `xp=jnp` there.

Then audit the sibling call sites for the same omission and fix any that are also inside
a `jit`:

- `likelihood_breakdown/delaunay_numba.py:433` — `jax.jit(lambda r, c, v: operator.curvature_matrix_diag_from(r, c, v, S=source_pixels))`
- `likelihood_breakdown/pixelization_numba.py:425` — same shape
- the rest of `likelihood_breakdown/datacube/*.py` and every script under
  `likelihood_runtime/` (`delaunay.py`, `mge.py`, `pixelization.py`, `datacube/`)

Nothing downstream of this prompt runs until step 0 is green.

## What

Re-run the `delaunay_numba.py` arms of the numba-interferometer pack through the **library
dispatch** rather than the standalone prototype pack, and confirm the crossover this
machine actually shows.

- Point the profiling arms at `aa.Inversion(...)` / the factory, so what is timed is the
  routed `InversionInterferometerSparseNumba` — not
  `scripts/misc/numba_interferometer/kernels.py`'s own copy of the kernel. With `xp=np`
  and the preconditions met, the factory returns the numba class at or below the gate.
- Sweep the geometry across the gate by varying source-pixel count / mesh so the mean
  non-zeros per source column crosses ~60 (Delaunay) and ~77 (rectangular), driving the
  route with `Settings(interferometer_numba_nnz_per_source_max=...)` — `0` pins the FFT
  route, a large value pins the numba route — so both arms run on identical inputs.
- Run at both the **sma** and **alma** dataset scales, so the crossover is confirmed
  across the uv-count range the pack already covers.
- Record wall time per likelihood evaluation for each route at each geometry, and report
  the measured crossover against the `autolens_profiling#226` verdict's §2 numbers
  (~60 / ~77), which were taken on the prototype pack rather than the library path.
- **Record the numbers in the #226 verdict note as a new section**, so the verdict of
  record carries the in-situ measurement beside the prototype one it is being compared
  against.

## Why

The shipped default (`60.0`) is a **machine-dependent constant** carried over from the
prototype measurements. Nothing has yet confirmed that the library path — which pays the
mapper's own triplet construction and the `kernel_index_arrays` marshalling inside the `F`
step — crosses in the same place as the pack, and the gate is what decides whether real
fits get the 2-7x win or silently lose to the FFT route.

## Done when

- Step 0's `xp=jnp` fix is merged (or carried in the same PR) and the touched scripts run.
- A results note under `autolens_profiling/results/notes/` reports the per-route timings,
  the measured crossover for both mesh families at sma and alma, and whether `60.0` is the
  right default on this machine (with a recommended value if not).
- The #226 verdict note carries a new section holding those in-situ numbers.
- If the library-path crossover differs materially from the pack's, a follow-up prompt
  against PyAutoArray to retune the packaged `general.yaml` default.

## Notes

- The prototype pack (`scripts/misc/numba_interferometer/`) stays as the reference
  implementation; this is a re-measurement of the shipped path, not a re-derivation.
- `NUMBA_NUM_THREADS` is baked in at numba's import, so a thread-scaling arm must set it
  before the first call into `direct_conv_parallel_kernel()`. The parallel kernel is
  selected by `general.yaml -> numba -> parallel`, which is `false` in the packaged
  config, so a parallel arm must set that too.
