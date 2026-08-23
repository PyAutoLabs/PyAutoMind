# Numba PSF gathers derive the y/x kernel shifts from the wrong kernel axes

Type: bug
Target: autoarray
Repos:
- @PyAutoArray
Difficulty: low
Autonomy: supervised
Priority: medium
Status: formalised
Filed: 2026-08-21 (backfilled from git)

Found 2026-08-21 while fixing
`draft/bug/autoarray/numba_first_call_garbage_psf_weighted_data.md` (the
out-of-bounds gather in `psf_weighted_data_from`). Split out under the
one-prompt-one-task rule: separate defect, separate blast radius.

## Symptom

Both numba PSF gathers in
`autoarray/inversion/inversion/imaging_numba/inversion_imaging_numba_util.py`
compute their kernel half-widths from the **transposed** kernel axes:

```python
kernel_shift_y = -(kernel_native.shape[1] // 2)   # shape[1] is x
kernel_shift_x = -(kernel_native.shape[0] // 2)   # shape[0] is y
```

at `psf_weighted_data_from` (line ~48) and `psf_precision_value_from`
(line ~294). The y shift must come from `shape[0]` and the x shift from
`shape[1]`.

The zero-padded numpy twin
(`imaging/inversion_imaging_util.py:psf_weighted_data_from`) gets it right and
is the reference:

```python
Ky, Kx = kernel_native.shape
ph, pw = Ky // 2, Kx // 2
```

## Reachability

Harmless for square kernels (`shape[0] == shape[1]`), which is the common
case and why no test catches it. It is **not** unreachable: kernels are
validated as *odd* in each axis, not square — `exc.KernelException("Convolver
Convolver must be odd")` in `operators/convolver.py:268` and
`structures/grids/uniform_2d.py:1153` check parity only. A non-square odd PSF
(e.g. 3x5) therefore mis-centres the gather, sampling the weight map / noise
map off-centre along both axes.

With the bounds guard now in place the mis-centred reads are clipped rather
than reading uninitialized memory, so this is a silent wrong-answer bug, not
a crash or a garbage-value bug.

## Fix

Swap the two right-hand sides in both functions. Fix them **together** — they
must agree on kernel orientation, and correcting only one would make the
`psf_weighted_data` and `psf_precision_operator` paths disagree.

## Acceptance

Extend the numba-vs-numpy equivalence test added by the OOB fix
(`test_autoarray/inversion/inversion/imaging/test_inversion_imaging_util.py::
test__psf_weighted_data_from__unmasked_pixels_on_array_edge`) to a non-square
odd kernel (e.g. 3x5). It passes today only because that test uses a square
kernel; with a non-square kernel the two implementations diverge.
