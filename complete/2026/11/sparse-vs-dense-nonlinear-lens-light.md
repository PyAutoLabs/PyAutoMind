## Retired — 2026-11-09 (covered by PyAutoArray#681)

Same root cause as PyAutoArray#680, fixed by https://github.com/PyAutoLabs/PyAutoArray/pull/681 (merged c020cc2):
`InversionImagingSparse.psf_weighted_data` read `sparse_operator.weight_map` (data/noise^2 of the ORIGINAL image), so a
non-linear lens light was never subtracted from the sparse data vector. The convolver "No blurring_image provided"
warning was incidental, not the cause.

Proof (this prompt's own witness setup: jax_test imaging, mask 3.5", os_lp=4 / os_pix=1, Sersic lens light,
20x20 rectangular adapt-image mesh + Constant reg, border relocator), retired under /prm authorization:

| library | mesh | dense FOM | sparse FOM | rel diff |
|---|---|---|---|---|
| main before #681 (e2b05f0) | RectangularBilinearAdaptImage | -782.2293572 | -50253.66735 | 6.3e+01 |
| main before #681 (e2b05f0) | RectangularRTUAdaptImage | -796.1245496 | -47847.60263 | 5.9e+01 |
| main after #681/#683 | RectangularBilinearAdaptImage | -773.0190134 | -773.0190134 | 1.2e-15 |
| main after #681/#683 | RectangularRTUAdaptImage | -786.9142058 | -786.9142058 | 5.8e-16 |

(The +9.21 shift in the dense values between rows is PyAutoArray#683, the pseudo-determinant.) Witness bar (<= 1e-8
relative) met.

- pending-release: PyAutoArray@https://github.com/PyAutoLabs/PyAutoArray/pull/681

## Original prompt

# Imaging sparse-operator path gives a very different log L from dense when the lens light is a non-linear light profile

Type: bug
Target: autoarray
Repos:
- PyAutoArray
Themes:
- source-reconstruction
Difficulty: medium
Autonomy: supervised
Priority: medium
Status: formalised
Consequence: judge
Witness: on autolens_workspace_test jax_test imaging with a standard (non-linear) Sersic lens light + rectangular pixelized source, `dataset.apply_sparse_operator()` and the dense path give the same figure of merit to <= 1e-8 relative (or the mismatch is shown to be a documented, raised-on misuse)
Review-minutes: 5
Unattended: never
Filed: 2026-11-02

Seen during PyAutoArray#671 (not chased). Repro `Science/scratch/rectangular_gradient_rtu_sparse_2026-11-02/repro.py` (no MGE env var → Sersic lens light): `jax_test` imaging, mask 3.5", os_lp=4 / os_pix=1, `RectangularBilinearAdaptImage` 20x20 + Constant reg, border relocator.

- dense log L −933.3, sparse log L −52010.3 (Bilinear); RTU 20x20 dense vs sparse similar gap.
- The sparse run warns `convolver.py:1053: UserWarning: No blurring_image provided. Only the direct image will be convolved.`
- With MGE (linear) lens light, dense and sparse agree exactly (658.576549), so the gap is in how the sparse path handles a non-linear lens-light image (blurring / subtraction), not in the mapper.

First step: compare the profile-subtracted image fed to the inversion on the two paths, and check whether the sparse path drops the blurring-region light.
