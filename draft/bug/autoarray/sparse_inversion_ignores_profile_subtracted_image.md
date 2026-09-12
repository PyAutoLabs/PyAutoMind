# Sparse (w-tilde) inversion fits the unsubtracted image when a regular light profile is on the tracer

Type: bug
Target: autoarray
Repos:
- PyAutoArray
Themes:
- inversion
- sparse-operator
- correctness
Difficulty: medium
Autonomy: supervised
Priority: high
Status: formalised
Consequence: judge
Review-minutes: 15
Unattended: ready
Witness: a regression test with a regular light profile + pixelized source where the sparse-operator and dense inversions agree on D, chi-squared and log_evidence to 1e-10
Filed: 2026-09-12

## Symptom

`InversionImagingSparse.psf_weighted_data` reads `dataset.sparse_operator.weight_map`,
which is `data / noise**2` baked at `apply_sparse_operator` time from the ORIGINAL image.
`FitImaging.galaxies_to_inversion` swaps `data` for `profile_subtracted_image` in the
`DatasetInterface` but passes the operator through unchanged, so the sparse data vector
`D` never sees the subtraction.

Measured 2026-09-11 (400-px rectangular mesh, true-Sersic regular lens light + pixelized
source; reproducer
`~/Code/PyAutoLabs-wt/matrix-free-pixelized-likelihood/_session_2026-09-11_artefacts/lens_light_probe/check_dv.py`):

| leg | inversion class | chi2 | log_evidence |
|---|---|---|---|
| sparse (`apply_sparse_operator`) | `InversionImagingSparse` | 154083 | −38713 |
| dense | `InversionImagingMapping` | 16239 | +31051 |

`max|D_sparse − D_dense| / max|D_dense| = 19.8`. The control with no regular light profile
agrees to 2.2e-16, so all-linear models — and today's production GPU runs, which fit the
plain dataset — are unaffected. Any `apply_sparse_operator` user with a regular lens light
(SLaM after light[1] with the light fixed, foreground-subtracted fits) is silently wrong.

## Fix

Build `psf_weighted_data` from the interface's (subtracted) data — rebuild or pass the
subtracted weight map into the operator rather than reading the one baked from the original
image — and add the regression test named in the witness. Check whether the interferometer
sparse path has the same seam.
