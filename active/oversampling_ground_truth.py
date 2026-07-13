# RETIRED 2026-07-09 (reconcile pass): companion of oversampling_design.md; oversampling series shipped (PyAutoArray#353 et al). Historical.
"""
Brute-force numerical ground truth for oversampled PSF convolution.

Phase 1 deliverable of `feature/autoarray/oversampling.md` (see
`oversampling_phase_1_design.md` and PyAutoLabs/PyAutoArray#353).

Defines, with an implementation independent of `autoarray.operators.convolver`,
what "convolve at over-sample size s then bin to image resolution" means:

1. The scene is evaluated on a uniform fine raster with pixel scale
   `ps / s` covering the same physical extent as the native image
   (fine-pixel centres coincide with autoarray's uniform sub-pixel centres).
2. Only fine pixels whose parent image pixel is unmasked or in the blurring
   region carry flux (matching the Convolver's masked-embedding semantics).
3. The PSF is the same analytic profile sampled at the fine pixel scale on an
   odd-sized kernel of fixed physical radius, normalized to sum to 1.
4. Direct (loop) 2D convolution on the fine raster, zero-padded ("same").
5. The convolved fine raster is binned to image resolution by the mean of
   each s x s block (matching `OverSampler.binned_array_2d_from`).
6. Values are read out at the unmasked pixels in row-major (slim) order.

At s=1 this must agree with `Convolver.convolved_image_via_real_space_np_from`
to machine precision (parity check, run if autoarray is importable). The s=2
values are the reference numbers phase-2 unit tests and the phase-3 workspace
test assert against.

Run:  python oversampling_ground_truth.py
"""

import numpy as np

# ----------------------------------------------------------------------------
# Configuration (all numbers that define the ground truth)
# ----------------------------------------------------------------------------

SHAPE_NATIVE = (11, 11)  # native image shape
PIXEL_SCALES = 1.0  # arcsec / pixel
MASK_RADIUS = 3.5  # circular mask radius, arcsec

SRC_SIGMA = 1.2  # Gaussian source width, arcsec
SRC_CENTRE = (0.3, -0.4)  # (y, x) arcsec — off-centre to break symmetry
SRC_NORM = 1.0  # peak-style normalization factor (1 / (sigma sqrt(2 pi)))

PSF_SIGMA = 0.8  # Gaussian PSF width, arcsec
PSF_RADIUS = 2.0  # kernel half-width, arcsec (5x5 kernel at ps=1)

REPORT_SLIM_INDICES = (0, 17, 36)  # slim pixels whose values are reported


def centres_1d(n: int, ps: float) -> np.ndarray:
    """Coordinates of pixel centres for an n-pixel axis of pixel scale ps,
    ordered top-left first (y decreasing / x increasing convention)."""
    return (np.arange(n) - (n - 1) / 2.0) * ps


def gaussian_2d(y, x, sigma, centre=(0.0, 0.0)):
    r2 = (y - centre[0]) ** 2 + (x - centre[1]) ** 2
    return (1.0 / (sigma * np.sqrt(2.0 * np.pi))) * np.exp(-0.5 * r2 / sigma**2)


def native_masks():
    """Circular unmasked region + blurring region for the native grid.

    unmasked[i, j] is True where the pixel-centre radius <= MASK_RADIUS.
    blurring[i, j] is True for masked pixels within the PSF kernel footprint
    of an unmasked pixel (matching Mask2D.derive_mask.blurring_from).
    """
    ny, nx = SHAPE_NATIVE
    ys = -centres_1d(ny, PIXEL_SCALES)  # y decreases with row index
    xs = centres_1d(nx, PIXEL_SCALES)
    yy, xx = np.meshgrid(ys, xs, indexing="ij")
    unmasked = np.sqrt(yy**2 + xx**2) <= MASK_RADIUS

    k = int(2 * (PSF_RADIUS / PIXEL_SCALES) + 1)  # native kernel size (odd)
    half = k // 2
    blurring = np.zeros_like(unmasked)
    for i in range(ny):
        for j in range(nx):
            if not unmasked[i, j]:
                continue
            y0, y1 = max(0, i - half), min(ny, i + half + 1)
            x0, x1 = max(0, j - half), min(nx, j + half + 1)
            blurring[y0:y1, x0:x1] = True
    blurring &= ~unmasked
    return unmasked, blurring


def ground_truth(s: int):
    """Blurred image at the unmasked pixels (slim, row-major) for over-sample
    size s, via brute-force fine-raster convolution."""
    ny, nx = SHAPE_NATIVE
    ps_f = PIXEL_SCALES / s
    nyf, nxf = ny * s, nx * s

    unmasked, blurring = native_masks()
    scene_region = unmasked | blurring

    # Fine raster of the scene: evaluate the source only where the parent
    # image pixel carries flux in the Convolver's masked embedding.
    ysf = -centres_1d(nyf, ps_f)
    xsf = centres_1d(nxf, ps_f)
    yyf, xxf = np.meshgrid(ysf, xsf, indexing="ij")
    scene_fine = SRC_NORM * gaussian_2d(yyf, xxf, SRC_SIGMA, SRC_CENTRE)
    parent_ok = np.repeat(np.repeat(scene_region, s, axis=0), s, axis=1)
    scene_fine = np.where(parent_ok, scene_fine, 0.0)

    # PSF sampled at the fine pixel scale, odd kernel, fixed physical radius.
    kf = int(2 * round(PSF_RADIUS / ps_f) + 1)
    kc = centres_1d(kf, ps_f)
    kyy, kxx = np.meshgrid(-kc, kc, indexing="ij")
    kernel = gaussian_2d(kyy, kxx, PSF_SIGMA)
    kernel = kernel / kernel.sum()

    # Direct "same" convolution with zero padding, plain loops.
    half = kf // 2
    padded = np.zeros((nyf + 2 * half, nxf + 2 * half))
    padded[half : half + nyf, half : half + nxf] = scene_fine
    blurred_fine = np.zeros((nyf, nxf))
    for i in range(nyf):
        for j in range(nxf):
            window = padded[i : i + kf, j : j + kf]
            blurred_fine[i, j] = np.sum(window * kernel[::-1, ::-1])

    # Bin down: mean of each s x s block.
    blurred = blurred_fine.reshape(ny, s, nx, s).mean(axis=(1, 3))

    return blurred[unmasked], kernel


def autoarray_parity(gt_slim: np.ndarray) -> None:
    """Compare the s=1 ground truth against the installed Convolver."""
    import autoarray as aa

    mask = aa.Mask2D.circular(
        shape_native=SHAPE_NATIVE, pixel_scales=PIXEL_SCALES, radius=MASK_RADIUS
    )
    unmasked, _ = native_masks()
    assert np.array_equal(np.array(mask), ~unmasked), "mask conventions differ"

    k = int(2 * (PSF_RADIUS / PIXEL_SCALES) + 1)
    kc = centres_1d(k, PIXEL_SCALES)
    kyy, kxx = np.meshgrid(-kc, kc, indexing="ij")
    kernel = aa.Array2D.no_mask(
        values=gaussian_2d(kyy, kxx, PSF_SIGMA), pixel_scales=PIXEL_SCALES
    )
    convolver = aa.Convolver(kernel=kernel, normalize=True, use_fft=False)

    grid = aa.Grid2D.from_mask(mask=mask, over_sample_size=1)
    blurring_mask = mask.derive_mask.blurring_from(kernel_shape_native=(k, k))
    blurring_grid = aa.Grid2D.from_mask(mask=blurring_mask, over_sample_size=1)

    def eval_on(grid_obj, grid_mask):
        vals = SRC_NORM * gaussian_2d(
            np.array(grid_obj)[:, 0], np.array(grid_obj)[:, 1], SRC_SIGMA, SRC_CENTRE
        )
        return aa.Array2D(values=vals, mask=grid_mask)

    image = eval_on(grid, mask)
    blurring_image = eval_on(blurring_grid, blurring_mask)

    convolved = convolver.convolved_image_via_real_space_np_from(
        image=image, blurring_image=blurring_image
    )

    diff = np.max(np.abs(np.array(convolved) - gt_slim))
    print(f"parity vs Convolver (s=1): max |diff| = {diff:.3e}")
    assert diff < 1e-12, "s=1 ground truth does not match the Convolver"


def main():
    results = {}
    for s in (1, 2):
        gt, kernel = ground_truth(s)
        results[s] = gt
        print(f"\n=== over-sample size s={s} (fine kernel {kernel.shape}) ===")
        print(f"n_unmasked           = {gt.size}")
        print(f"sum over mask        = {gt.sum():.15e}")
        for idx in REPORT_SLIM_INDICES:
            print(f"blurred[slim {idx:3d}]    = {gt[idx]:.15e}")

    d = np.abs(results[2] - results[1])
    print(f"\ns=2 vs s=1: max |diff| = {d.max():.3e}, mean |diff| = {d.mean():.3e}")

    try:
        import autoarray  # noqa: F401

        have_aa = True
    except ImportError:
        have_aa = False
        print("\nautoarray not importable — skipping Convolver parity check")

    if have_aa:
        print()
        autoarray_parity(results[1])


if __name__ == "__main__":
    main()
