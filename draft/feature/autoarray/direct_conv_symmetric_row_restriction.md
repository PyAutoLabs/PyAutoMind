# direct_conv curvature kernel: convolve only the rows later-ranked columns need, then mirror

Type: feature
Target: PyAutoArray
Repos:
- PyAutoArray
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: formalised
Consequence: glance
Witness: on the Aris 512x512 setup (91,507 masked pixels, extent 341², 1,459–5,746 vertices) the numba direct_conv curvature matrix is bit-identical (<=1e-15 relative) and >=1.8x faster at 2,577 vertices on an unloaded core; the #632 route model is recalibrated on the new timings
Review-minutes: 3
Unattended: ready

Profiled 2026-10-15 (session 3e3dea38, main 17caf228): at 512x512 the numba `curvature_direct_conv`
kernel is 96–98% of a likelihood call (34 s at 2,577 vertices, 41 s at 5,746). F is symmetric, so each
column's convolution only needs the extent rows spanned by columns ranked after it (sort columns by y),
clipped to the mask's x-range; gather only the upper triangle (CSC layout, 32 vs 63 ms at 1,405) and
mirror. Exact to 2e-16 (prototype `aris_research/kern.py::kC`, temporary). Work fraction on paper
0.60x at 125x125, 0.42x at 512x512. Measured: 125x125 1.10x / 0.82x (gather+mirror overhead cancels —
not worth it there); 512 synthetic (341², 91k px, 1,428 vtx, nnz 274k) 2.5x uncontended (63 → 25 s)
but only 1.03–1.10x under load 5 — so the gain is 2–2.5x UNCONFIRMED and must be re-measured on a
quiet core first. If it holds, direct_conv likely beats FFT at 1,459 vertices too (28.3 s FFT), so the
#632 cost-model constants need refitting (extent-dependent kernel work). Keep a kill switch; large
extents only (gate on extent size or let the route model decide). Campaign
https://github.com/PyAutoLabs/PyAutoPulse/issues/62; related Pulse task
interferometer_fixed_mapper_curvature_preload (the bigger win for fixed-lens source_pix[1] phases).
