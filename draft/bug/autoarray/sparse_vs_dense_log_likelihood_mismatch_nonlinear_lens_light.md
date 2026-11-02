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
