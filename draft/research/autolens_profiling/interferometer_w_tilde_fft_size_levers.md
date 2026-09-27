# Interferometer W~ curvature matrix is FFT-bound on the mask extent: pruned padded FFT and real-space pixel scale on the A100

Type: research
Target: autolens_profiling
Repos:
- autolens_profiling
- PyAutoArray
Themes:
- interferometer
- pixelization
- likelihood-profiling
- jax-gpu
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: draft
Consequence: glance
Witness: `results/breakdown/interferometer/jvla/delaunay_hpc_a100_fp64_fft_prune.json` has a pruned-vs-library F row at alma, alma_high and jvla. The pruned F agrees with the library F to max rel diff ≤ 1e-12 and the figure of merit to ≤ 1e-6 nats. The file also has an F-vs-real-space-pixel-scale row at jvla (0.01 / 0.015 / 0.02 / 0.025″) with the log-evidence shift against the 0.01″ reference.
Review-minutes: 10
Unattended: ready
Lane: local-dev
Epic: interferometer-likelihood-campaign
Filed: 2026-09-27

Follow-up to autolens_profiling#320, lever 2
(`results/notes/interferometer_mesh_a100_breakdown_2026_09.md`, "Ranked levers" §2).

## Why

On the A100 the W~ curvature matrix F = Aᵀ W~ A is 36–42 % of the sparse-path pixelized
likelihood at alma, 66–73 % at alma_high and 91–92 % at jvla (510 of 563 ms, Delaunay-1500).
Its cost is set by the mask extent M = y·x (70² / 140² / 280² / 700² at sma → jvla), not by
N_vis.

- The block-size sweep is flat (alma B = 32–512: 17.8–19.3 ms).
- The kernel split puts the FFT apply at 71–85 % of F.
- So F is **FFT-bound** on the (B, 2y, 2x) `rfft2` / `irfft2` pair.

The extent is already the mask bounding box (PyAutoArray `mask/mask_2d.py:746-776`
`extent_index_for_masked_pixel`), and the (2y, 2x) pad is the minimum for a linear
correlation. Only two things are left to change: how much of the padded transform is computed,
and how big the extent is.

## What

1. **Pruned padded transform (measurement first, harness-only).**
   `InterferometerSparseOperator.apply_operator` (PyAutoArray
   `inversion/inversion/interferometer/inversion_interferometer_util.py:1099-1151`) pads each
   (B, y, x) block to (B, 2y, 2x) and runs full 2-D `jnp.fft.rfft2` / `irfft2` (`:1145-1150`).
   Only the top-left y × x quadrant of the input is non-zero, and only the top-left y × x of the
   output is kept (`:1150`).
   - Write a harness copy of `curvature_matrix_diag_from` (`:1171-1253`) whose apply is
     separable: `rfft` along x on the y non-zero rows (x padded to 2x), zero-pad y, `fft` along
     y, multiply by `Khat`, `ifft` along y and keep y rows, `irfft` along x with `n = 2x`,
     keep x.
   - That removes up to ~25 % of the FFT work. The bound is ≤ ~15–20 % of F (~90 ms at jvla,
     ~3 ms at alma).
   - Measure it against the library F inside the same fused jit at alma / alma_high / jvla,
     Delaunay and rect. One cuFFT 2-D call may beat four 1-D calls, so record a no-go honestly.
2. **Real-space pixel scale at jvla (measurement, science-gated).** jvla at 0.01″ is a 700²
   extent. Re-run the jvla Delaunay-1500 cell at real-space pixel scales 0.015 / 0.02 / 0.025″
   (mask radius fixed at 3.5″; `instruments/interferometer.py` jvla entry). Record F, the full
   call and the log-evidence / reconstruction shift against 0.01″. Predicted: 2× coarser gives
   ~4× smaller M, putting F near the alma_high row (~67 ms). Whether the science tolerates it is
   the question, not the speed. The mask-radius half (2.0 / 3.5 / 5.0″) is in task 3/3's
   decision matrix on CPU (`draft/research/autolens_profiling/interferometer_mesh_breakdown_numba_cpu_decision_matrix.md`);
   do not duplicate it.
3. Verdict in a note section. If (1) wins by ≥ 10 % of F at jvla with a ≤ 1e-12 F match, file
   the PyAutoArray change (the NumPy branch `:1155-1169` gets the same pruning via
   `scipy.fft`). If (2) holds the 0.5-nat bar at a coarser scale, file a workspace docs prompt
   for interferometer real-space grid guidance.

## Not in scope

The fp32 FFT arm (slower on the A100 and fails the bar at jvla, #320), block size (flat), and
mixed precision (does not reach F).
