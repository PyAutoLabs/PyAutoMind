## Shipped — 2026-11-09

Sparse (w-tilde) imaging inversion now builds its data vector from the inversion's own (profile-subtracted) data and
noise-map instead of `sparse_operator.weight_map` baked from the original image.

- PR: https://github.com/PyAutoLabs/PyAutoArray/pull/681 (merged c020cc2); issue https://github.com/PyAutoLabs/PyAutoArray/issues/680
- Fix: gather-only `psf_weighted_data_via_slim_from` via a static [N, Ky, Kx] neighbour slim-index table. A first
  scatter (`.at[].set`) version reproducibly hung the rectangular_mge.py vmap likelihood on CPU and was replaced.
- Witness: sparse vs dense agree on D, chi-squared, log_evidence to 1e-10 with a regular light profile (NumPy, JAX
  eager, jax.jit); no-profile control unchanged. End-to-end al.FitImaging: sparse log_evidence -69075 (main) -> +277.98,
  matching dense to 1e-13.
- Interferometer sparse path: no seam (subtracted sparse_dirty_image / data_term already passed and honoured).
- Unit suite 2298 passed / 1 skipped / 4 xfailed at PR time; CI 3/3 legs green.
- Process: ran in parallel with magnification-maps-wiring's PyAutoArray claim under explicit human override (2026-11-08).

- pending-release: PyAutoArray@https://github.com/PyAutoLabs/PyAutoArray/pull/681

## Original prompt

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
Consequence: glance
Review-minutes: 3
Unattended: ready
Witness: a regression test with a regular light profile + pixelized source where the sparse-operator and dense inversions agree on D, chi-squared and log_evidence to 1e-10
Filed: 2026-09-12
Issued: 2026-11-08
Issue: https://github.com/PyAutoLabs/PyAutoArray/issues/680

## Symptom

`InversionImagingSparse.psf_weighted_data` reads `dataset.sparse_operator.weight_map`,
which is `data / noise**2` baked at `apply_sparse_operator` time from the ORIGINAL image.
`FitImaging.galaxies_to_inversion` swaps `data` for `profile_subtracted_image` in the
`DatasetInterface` but passes the operator through unchanged, so the sparse data vector
`D` never sees the subtraction.

Measured 2026-09-11 (400-px rectangular mesh, true-Sersic regular lens light + pixelized
source; reproducer
`~/Code/PyAutoLabs/tmp/matrix_free_247_session_artefacts/_session_2026-09-11_artefacts/lens_light_probe/check_dv.py`):

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
