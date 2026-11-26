# Hilbert image mesh: make it depend only on the mask, not the image frame

Type: bug
Target: autoarray
Repos:
- PyAutoArray
- autolens_workspace_test
- autogalaxy_workspace_test
Difficulty: medium
Autonomy: supervised
Priority: high
Consequence: judge
Community: https://github.com/PyAutoLabs/.github/discussions/43
Filed: 2026-11-17
Status: fixed in PyAutoArray#718 (open, 2026-11-26) — retire when it merges

Agreed by the human in the /community chat on 2026-11-17. Separate from PyAutoArray#675
(Sam's FFT-frame trim), which was reworked to live inside `ConvolverState` so the
dataset's native frame never changes — shipped in PyAutoArray#699
(`complete/2026/11/convolver-fft-frame-from-mask.md`). This task fixes the Hilbert side regardless.

## Problem

`autoarray/inversion/mesh/image_mesh/hilbert.py` `image_and_grid_from` should depend only on
the mask (radius, centre, the fixed Hilbert curve) and the adapt image's values. It
depends on the native frame size in two ways:

1. It interpolates the adapt image with `scipy.interpolate.griddata(method="linear")` over
   `Grid2D.uniform(shape_native=(shape_nnn, shape_nnn))`. A Delaunay triangulation of a regular
   lattice is degenerate (each square can split along either diagonal), so qhull's choice, and
   hence the interpolated value between pixel centres, changes with the frame size. Measured
   2026-11-17 on `autolens_workspace_test/dataset/imaging/jax_test` (0.3"/px, 2.6" mask): native
   values identical on the overlap, but values between nodes differ (0.349 vs 0.369, 0.375 vs
   0.250) between a 100x100 and a 30x30 frame.
2. `shape_nnn = np.shape(image.native)[0]` assumes a square image; a non-square native array
   gets a wrong grid.

The inverse-transform sampling (weight_power 3.5, Hilbert-order CDF) amplifies small
interpolation changes into large mesh changes: the PR #675 smoke run saw mesh points move by
up to ~0.9" and `scripts/imaging/jax_likelihood/delaunay.py` go -532.30 -> -472.13
(delaunay_mge 732.07 -> 731.55) from the frame size alone.

## Proposed fix

Interpolate on the regular grid directly (bilinear, e.g. `scipy.ndimage.map_coordinates(order=1,
cval=0)` or `RegularGridInterpolator`) using the array's own scaled geometry (both dimensions,
pixel scales, origin), so the result is identical for any frame that contains the mask.

## Evidence that pinned values WILL change

A quick bilinear prototype (verified equal to griddata at pixel nodes) changed the pinned
`autolens_workspace_test/scripts/imaging/jax_likelihood/delaunay.py` log-likelihood from
-532.29584351 to -2235.0161. That is far larger than expected for an interpolation change, so
the task must first check whether the Hilbert sampling is fragile (mesh quality, clustering,
points at the mask edge) before re-pinning anything. ~20 workspace_test scripts use
`image_mesh.Hilbert` (imaging/interferometer/multi_dataset jax_likelihood, jax_grad,
jax_assertions, visualization) in autolens_workspace_test and autogalaxy_workspace_test.

## Done when

- Hilbert mesh identical (to rounding) for the same mask on frames of different size, and
  correct on non-square frames; unit tests for both.
- The likelihood change is understood and judged (plots of the mesh before/after), and the
  pinned values are re-pinned with a one-line reason, in a workspace_test PR after the library PR.

## 2026-11-26: fixed in PyAutoArray#718 (human's choice: opt-in for `Hilbert`)

Measured first on `main` (cda647d3): padding a lens's frame by 10-20 pixels moved `HilbertSNR` points
by up to 6-9 image pixels (mean 0.3-0.8 px; `Hilbert(3.5)` 4-5 px), and a non-square frame raised
`ValueError: different number of values and points`. PyAutoArray#718 adds
`image_and_grid_from(..., frame_independent=True)`: bilinear `scipy.ndimage.map_coordinates(order=1)`
on the image's own shape, pixel scales and origin. Same mesh in any frame (to 1e-9, square or not),
exact on a linear image. The human chose: `HilbertSNR` uses it by default; `Hilbert` keeps the
original `griddata` unless `frame_independent=True`, so no pinned value moves and no workspace_test
re-pin is needed. On real lenses the bilinear mesh differs from the griddata one by a mean of
0.35-0.62 px. Retire this prompt in the /prm close-out of PyAutoArray#718.
