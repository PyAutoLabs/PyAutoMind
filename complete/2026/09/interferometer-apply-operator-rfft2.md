# interferometer-apply-operator-rfft2

- Library: PyAutoArray
- Issue: https://github.com/PyAutoLabs/PyAutoArray/issues/538 (closed, completed)
- PR: https://github.com/PyAutoLabs/PyAutoArray/pull/540 (MERGED, merge commit `7a4cb700`, head `a67828e3`)
- Epic: numba-interferometer-revisit (phase 2), follow-up from `autolens_profiling#226`
- pending-release: PyAutoArray@https://github.com/PyAutoLabs/PyAutoArray/pull/540

## What shipped

`InterferometerSparseOperator.apply_operator`
(`autoarray/inversion/inversion/interferometer/inversion_interferometer_util.py`) no
longer zero-pads a **real** batch to `(2y, 2x)` and pushes it through the complex
`jnp.fft.fft2` / `jnp.fft.ifft2` pair with a `.real` at the end. It now uses the exact
real-transform pair `jnp.fft.rfft2` / `jnp.fft.irfft2`, which computes the same result
exactly — not approximately — over roughly half the spectrum.

`Khat` is built the same way: `jnp.fft.rfft2(nufft_precision_operator)`, so it carries
shape `(2y, x + 1)` rather than `(2y, 2x)`. The operator is real, so the second half of
its transform was always the conjugate mirror of the first.

Diff: 2 files, +116/-29 —
`inversion_interferometer_util.py` (+36 changed) and
`test_inversion_interferometer_util.py` (+109/-29).

## Evidence

- **Exactness pinned, not asserted.** The new path is pinned against the previous
  complex `fft2`/`ifft2` route at `rtol=1e-10`; the measured agreement is `2.8e-14`,
  four orders inside the tolerance. That test is the guard against a future "optimisation"
  that quietly changes the numbers.
- **Speed:** 1.27-1.61x measured over the complex path (`autolens_profiling#226`,
  `results/notes/numba_interferometer_verdict.md`).
- **CI:** all three legs green on head `a67828e3` — `unittest (3.12)`, `unittest (3.13)`,
  `unittest-nojax`. `MERGEABLE` / `CLEAN` re-verified immediately before the merge.

## Open verification item

The **A100 confirmation was not run before merge.** The human waived it at merge time, so
it is recorded here as outstanding rather than as done: the 1.27-1.61x figure is a CPU/
local measurement, and the GPU behaviour of the `rfft2` path (where the halved spectrum
changes the memory traffic, not just the flop count) has not been measured on an A100.
Pick this up with the epic's remaining phases or the next profiling sweep.

## Heart ack carried from the active.md row

- heart-ack: 2026-09-08 in-session, two reasons "workspace validation not passing (5 failed, 2 timeout, cloud#34099198772: autolens notebooks/multi_dataset/modeling.ipynb, autolens scripts/multi_dataset/modeling.py, autolens_test scripts/imaging/delaunay.py, +4 more)" and "release validation incomplete: no rehearsal for current source" — organism-scope; neither names PyAutoArray or a library test, and this branch changes no API and no numerical result

## Follow-ons still open

- `interferometer-preload-nufft-type1` (PyAutoArray#539 / PR#541) was stacked on this
  branch; GitHub retargeted it to `main` when #540 merged. Still open, closed out on its own.
- `draft/feature/autoarray/interferometer_sparse_operator_numpy_cpu_path.md` was filed to
  be sequenced after this one ("real-FFT first"); that sequencing constraint is now
  satisfied.

## Original prompt

# `InterferometerSparseOperator.apply_operator` pads real input to complex — use `rfft2`/`irfft2`

Type: feature
Target: autoarray
Repos:
- PyAutoArray
Themes:
- interferometer
- jax-performance
- likelihood-profiling
Difficulty: small
Autonomy: supervised
Priority: high
Epic: numba-interferometer-revisit
Filed: 2026-09-07
Issued: 2026-09-08
Issue: https://github.com/PyAutoLabs/PyAutoArray/issues/538

Follow-up from `autolens_profiling#226` (phase 2 of `numba-interferometer-revisit`); the
numbers are in `autolens_profiling/results/notes/numba_interferometer_verdict.md` and
`results/breakdown/interferometer/bakeoff_v2026.8.17.1.json`.

## What

`autoarray/inversion/inversion/interferometer/inversion_interferometer_util.py`
(`InterferometerSparseOperator.apply_operator`, ~689-728) zero-pads a **real** batch to
`(2y, 2x)` and applies the operator with complex `jnp.fft.fft2` / `jnp.fft.ifft2`, taking
the real part at the end. `Khat = jnp.fft.fft2(nufft_precision_operator)` is likewise the
complex transform of a real array. Both halve-able: the real-transform pair
`rfft2` / `irfft2` computes the same result exactly (not approximately) with roughly half
the spectrum and half the butterflies.

## Measured saving (single thread, i9-10885H, autoarray 2026.8.17.1)

Same synthetic inputs, same batch size (128), scipy stack, so the comparison isolates the
transform:

| geometry (extent) | mesh | complex `fft2` | real `rfft2` | saving |
|---|---|---|---|---|
| sma (70²) | Delaunay S=1500 | 1.7479 s | 1.2660 s | 1.38× |
| alma (140²) | Delaunay S=1500 | 6.5003 s | 4.3951 s | 1.48× |
| alma_high (280²) | Delaunay S=1500 | 17.7362 s | 11.0346 s | 1.61× |
| sma (70²) | rect S=784 | 1.0124 s | 0.7361 s | 1.38× |
| alma (140²) | rect S=784 | 3.3786 s | 2.6557 s | 1.27× |
| alma_high (280²) | rect S=784 | 6.9360 s | 4.8414 s | 1.43× |

`rfft2` on the NumPy stack also beats the library's own JAX-CPU route by 1.10-1.30× at every
one of those cells, i.e. the transform change is worth more than the backend.

## Scope

- Change `from_nufft_precision_operator` to cache `Khat = jnp.fft.rfft2(...)` and
  `apply_operator` to `rfft2` → multiply → `irfft2(s=(2y, 2x))` → crop.
- The parity gate is the existing interferometer inversion tests plus an explicit pin of
  `curvature_matrix` before/after at `rtol=1e-10`; the change is exact, so a loosened
  tolerance would be hiding a bug.
- GPU: the saving should hold or improve (half the FFT work and half the intermediate
  memory); confirm on the A100 before merging rather than assuming it.
- Nothing else in the interferometer path changes — the algebra is untouched.
