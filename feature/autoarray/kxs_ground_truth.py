"""
Brute-force ground truth for the k×s evaluation/convolution coupling.

Phase 1 of `oversampling_kxs_coupling.md` (PyAutoLabs/PyAutoArray#362).
Extends `oversampling_ground_truth.py` (same scene, same conventions):

Mechanism: each image pixel is evaluated on its own adaptive sub-grid of
size k_i·s (integration accuracy from adaptive sampling), the evaluated
block is partially binned by the mean of each (k_i)² group down to a uniform
s×s block (one fine image at the convolution resolution), the fine image is
PSF-convolved at s exactly as in the parent series, and the result is binned
s→1 to image resolution.

Pinned outputs: the adaptive-evaluation results phases 2–3 assert against.
Consistency requirements verified here:
  1. k_i = 1 everywhere reduces EXACTLY to the parent s=2 reference values.
  2. The partial bin is exact: feeding the manually pre-binned fine image
     through the parent pipeline gives identical numbers (by construction —
     printed as a cross-check of the index arithmetic).

Run:  python kxs_ground_truth.py
"""

import numpy as np

SHAPE_NATIVE = (11, 11)
PIXEL_SCALES = 1.0
MASK_RADIUS = 3.5
SRC_SIGMA = 1.2
SRC_CENTRE = (0.3, -0.4)
PSF_SIGMA = 0.8
PSF_RADIUS = 2.0
S = 2  # convolve over sample size

# Adaptive evaluation pattern: k_i = 2 (evaluate at 4x4 per pixel) within
# radius 2.0" of the source centre, else k_i = 1 (evaluate at 2x2 = s).
K_INNER, K_OUTER, K_RADIUS = 2, 1, 2.0

REPORT_SLIM_INDICES = (0, 17, 36)


def centres_1d(n, ps):
    return (np.arange(n) - (n - 1) / 2.0) * ps


def gaussian_2d(y, x, sigma, centre=(0.0, 0.0)):
    r2 = (y - centre[0]) ** 2 + (x - centre[1]) ** 2
    return (1.0 / (sigma * np.sqrt(2.0 * np.pi))) * np.exp(-0.5 * r2 / sigma**2)


def native_masks():
    ny, nx = SHAPE_NATIVE
    ys = -centres_1d(ny, PIXEL_SCALES)
    xs = centres_1d(nx, PIXEL_SCALES)
    yy, xx = np.meshgrid(ys, xs, indexing="ij")
    unmasked = np.sqrt(yy**2 + xx**2) <= MASK_RADIUS

    k = int(2 * (PSF_RADIUS / PIXEL_SCALES) + 1)
    half = k // 2
    blurring = np.zeros_like(unmasked)
    for i in range(ny):
        for j in range(nx):
            if unmasked[i, j]:
                blurring[
                    max(0, i - half) : i + half + 1, max(0, j - half) : j + half + 1
                ] = True
    blurring &= ~unmasked
    return unmasked, blurring, (yy, xx)


def pixel_block_binned_to_s(i, j, k_i, s):
    """
    Evaluate the source on pixel (i, j)'s adaptive (k_i*s x k_i*s) sub-grid and
    partially bin to an (s x s) block by the mean of each (k_i x k_i) group.
    """
    n = k_i * s
    ps_f = PIXEL_SCALES / n
    y0 = (SHAPE_NATIVE[0] - 1) / 2.0 * PIXEL_SCALES - i * PIXEL_SCALES
    x0 = -(SHAPE_NATIVE[1] - 1) / 2.0 * PIXEL_SCALES + j * PIXEL_SCALES
    offs = (np.arange(n) - (n - 1) / 2.0) * ps_f
    yy = y0 - offs[:, None] * np.ones(n)[None, :]
    xx = x0 + np.ones(n)[:, None] * offs[None, :]
    vals = gaussian_2d(yy, xx, SRC_SIGMA, SRC_CENTRE)
    return vals.reshape(s, k_i, s, k_i).mean(axis=(1, 3))


def fine_image_from(k_map, s):
    """The uniform s-resolution fine image of the masked scene, with each
    pixel's block produced by adaptive evaluation + partial bin."""
    ny, nx = SHAPE_NATIVE
    unmasked, blurring, (yy, xx) = native_masks()
    region = unmasked | blurring

    fine = np.zeros((ny * s, nx * s))
    for i in range(ny):
        for j in range(nx):
            if not region[i, j]:
                continue
            fine[i * s : (i + 1) * s, j * s : (j + 1) * s] = pixel_block_binned_to_s(
                i, j, int(k_map[i, j]), s
            )
    return fine, unmasked


def convolve_and_bin(fine, s):
    ps_f = PIXEL_SCALES / s
    kf = int(2 * round(PSF_RADIUS / ps_f) + 1)
    kc = centres_1d(kf, ps_f)
    kyy, kxx = np.meshgrid(-kc, kc, indexing="ij")
    kernel = gaussian_2d(kyy, kxx, PSF_SIGMA)
    kernel = kernel / kernel.sum()

    half = kf // 2
    nyf, nxf = fine.shape
    padded = np.zeros((nyf + 2 * half, nxf + 2 * half))
    padded[half : half + nyf, half : half + nxf] = fine
    blurred = np.zeros_like(fine)
    for i in range(nyf):
        for j in range(nxf):
            blurred[i, j] = np.sum(
                padded[i : i + kf, j : j + kf] * kernel[::-1, ::-1]
            )

    ny, nx = SHAPE_NATIVE
    return blurred.reshape(ny, s, nx, s).mean(axis=(1, 3))


def main():
    ny, nx = SHAPE_NATIVE
    ys = -centres_1d(ny, PIXEL_SCALES)
    xs = centres_1d(nx, PIXEL_SCALES)
    yy, xx = np.meshgrid(ys, xs, indexing="ij")
    r_src = np.sqrt((yy - SRC_CENTRE[0]) ** 2 + (xx - SRC_CENTRE[1]) ** 2)

    # 1) k=1 reduction: must equal the parent s=2 reference exactly.
    k_ones = np.full(SHAPE_NATIVE, 1)
    fine, unmasked = fine_image_from(k_ones, S)
    out = convolve_and_bin(fine, S)[unmasked]
    expected = {
        "sum": 2.796562184524787e00,
        0: 3.726289901353439e-02,
        17: 2.025075336159483e-01,
        36: 1.090767109119494e-02,
    }
    assert abs(out.sum() - expected["sum"]) < 1e-12
    for idx in REPORT_SLIM_INDICES:
        assert abs(out[idx] - expected[idx]) < 1e-12
    print("k=1 reduction: EXACT match to parent s=2 reference")

    # 2) Adaptive reference: k_i = 2 inside K_RADIUS of the source, else 1.
    k_map = np.where(r_src <= K_RADIUS, K_INNER, K_OUTER)
    fine, unmasked = fine_image_from(k_map, S)
    out = convolve_and_bin(fine, S)[unmasked]

    print(f"\n=== adaptive k(x) in {{{K_INNER},{K_OUTER}}}, s={S} ===")
    print(f"n_unmasked        = {out.size}")
    print(f"sum over mask     = {out.sum():.15e}")
    for idx in REPORT_SLIM_INDICES:
        print(f"blurred[slim {idx:3d}] = {out[idx]:.15e}")

    d = np.abs(out.sum() - expected["sum"])
    print(f"\nadaptive vs k=1 |sum diff| = {d:.3e} (nonzero = finer integration matters)")


if __name__ == "__main__":
    main()
