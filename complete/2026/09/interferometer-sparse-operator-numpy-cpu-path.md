- Library: PyAutoArray
- Issue: https://github.com/PyAutoLabs/PyAutoArray/issues/542 (closed, completed)
- PR: https://github.com/PyAutoLabs/PyAutoArray/pull/544 (MERGED, merge commit `39d3024c`, head `c2469b9d`)
- Epic: numba-interferometer-revisit (phase 2), follow-up from `autolens_profiling#226`
- pending-release: PyAutoArray@https://github.com/PyAutoLabs/PyAutoArray/pull/544

## What shipped

`InterferometerSparseOperator` no longer forces every caller through JAX. The operator now
keeps the **raw preload** and builds its transform lazily, per branch: `Khat`
(`jnp.fft.rfft2`, built under `ensure_compile_time_eval` so it folds at trace time) for the
JAX branch, `khat_np` (`scipy.fft.rfft2`) for the NumPy branch. Neither is built until the
branch that needs it is taken, so a NumPy fit never touches JAX.

Six methods on the operator take an explicit `xp`
(`autoarray/inversion/inversion/interferometer/inversion_interferometer_util.py`), and
`InversionInterferometerSparse` passes `xp=self._xp`
(`.../interferometer/sparse.py`) — so the `xp` the dataset/fit was built with propagates all
the way through `apply_operator`, `curvature_matrix_diag_from` and
`curvature_matrix_off_diag_from`. The JAX branch is byte-for-byte the code that was there
before; the NumPy branch uses `scipy.fft` for the convolution and `scipy.sparse` for the
projection (the NumPy-stack counterpart of the JAX route's `segment_sum`).

The Delaunay `col=-1` padding is now **dropped explicitly** on the NumPy branch. On the JAX
route the padding column was absorbed silently by out-of-bounds scatter semantics; scipy has
no such behaviour, so relying on it would have folded the pad row into a real source pixel.

Diff: 5 files, +926/-37 — the util module (+366 changed), `sparse.py`,
`dataset/interferometer/dataset.py`, and two test modules (+583).

## Evidence

- **No JAX on the NumPy path, tested rather than asserted.** A subprocess test builds and
  runs a NumPy interferometer fit and asserts `jax` never appears in `sys.modules`. That is
  the guard that keeps a future lazy import from quietly re-introducing the dependency.
- **Parity:** NumPy vs JAX agree to `<= 5e-16` relative on `F`; the end-to-end curvature
  matrix agrees at `2.8e-14`. Both are pinned as tests, well inside the prompt's `rtol=1e-10`
  gate.
- **Speed:** 3.8x faster than the JAX-CPU route on a 40x40 / S=400 probe, measured against
  the post-`rfft2` baseline (PyAutoArray#540) rather than the pre-`rfft2` table in the prompt.
- **CI:** all three legs green on head `c2469b9d` — `unittest (3.12)`, `unittest (3.13)`,
  `unittest-nojax`. `MERGEABLE` / `CLEAN` re-verified immediately before the merge.

## Downstream

PyAutoLens `potential_correction` callers that build interferometer inversions with `xp=np`
now take the NumPy application path. Same numbers (parity above), one fewer import; no API
change and nothing for a caller to update.

## Heart ack carried from the active.md row

- heart-ack: 2026-09-08 in-session, reasons "workspace validation not passing (5 failed,
  2 timeout, cloud#34099198772: autolens notebooks/multi_dataset/modeling.ipynb, autolens
  scripts/multi_dataset/modeling.py, autolens_test scripts/imaging/delaunay.py, +4 more)"
  and "release validation incomplete: no rehearsal for current source" — neither touches the
  PyAutoArray interferometer sparse operator.

## Follow-ons still open

- **Task 4, `interferometer-numba-cpu-direct-conv` (PyAutoArray#543)**, is stacked on this
  branch: its `feature/interferometer-numba-cpu-direct-conv` was cut from this branch's tip
  and its PR was not yet open when #544 merged, so GitHub's auto-retarget did not apply. Its
  PR is opened against `main` directly.

## Original prompt

# `InterferometerSparseOperator` has no NumPy path — a CPU user is forced through JAX

Type: feature
Target: autoarray
Repos:
- PyAutoArray
Themes:
- interferometer
- numpy-cpu
- likelihood-profiling
Difficulty: medium
Autonomy: supervised
Priority: medium
Epic: numba-interferometer-revisit
Filed: 2026-09-07
Issued: 2026-09-08
Issue: https://github.com/PyAutoLabs/PyAutoArray/issues/542

Follow-up from `autolens_profiling#226` (phase 2 of `numba-interferometer-revisit`);
numbers in `autolens_profiling/results/notes/numba_interferometer_verdict.md`.

## What

`InterferometerSparseOperator.apply_operator`, `curvature_matrix_diag_from` and
`curvature_matrix_off_diag_from`
(`autoarray/inversion/inversion/interferometer/inversion_interferometer_util.py`) all
`import jax.numpy` inside the method body. There is no `xp=np` branch: a user without a GPU
still runs the interferometer curvature through JAX, and `InversionInterferometerSparse`
inherits that whatever `xp` the fit was built with.

That is not only an unwanted dependency — it is slower. On identical inputs, a NumPy/scipy
`rfft2` convolution with a `scipy.sparse` projection (the NumPy-stack counterpart of the JAX
route's `segment_sum`) beats the library's JAX-CPU route at every geometry measured:

| geometry | mesh | JAX-CPU (`fft2`) | NumPy (`rfft2`) | saving |
|---|---|---|---|---|
| sma | Delaunay S=1500 | 1.5239 s | 1.2660 s | 1.20× |
| alma | Delaunay S=1500 | 5.5156 s | 4.3951 s | 1.26× |
| alma_high | Delaunay S=1500 | 12.9655 s | 11.0346 s | 1.18× |
| sma | rect S=784 | 0.8510 s | 0.7361 s | 1.16× |
| alma | rect S=784 | 2.9317 s | 2.6557 s | 1.10× |
| alma_high | rect S=784 | 6.2817 s | 4.8414 s | 1.30× |

(Some of that gap is the `rfft2` change filed separately as
`interferometer_apply_operator_rfft2.md`, which shipped on 2026-09-08 — PyAutoArray#540,
record `complete/2026/09/interferometer-apply-operator-rfft2.md`. The real-FFT-first
sequencing constraint is therefore already satisfied; measure this one against the
post-`rfft2` baseline, not the numbers in the table above.)

## Scope

- An `xp`-aware application path so `xp=np` uses `scipy.fft` and `scipy.sparse` and never
  imports JAX; the JAX branch stays exactly as it is.
- The reference implementation to port is
  `autolens_profiling/scripts/misc/numba_interferometer/kernels.py::curvature_fft_numpy`,
  which is pinned to the numba reference kernel at `rtol=1e-10` in that pack's
  `test_parity.py`.
- Parity gate: the NumPy and JAX branches must agree at `rtol=1e-10` on `F` with `atol`
  scaled by `max|F|`.
- Worth checking at the same time whether `apply_sparse_operator(use_jax=False)` should
  imply the NumPy application path (today it only affects how the preload is *built*, not
  how the operator is *applied*, which is a surprising split).
