Symmetric row-restricted `direct_conv` interferometer curvature kernel (PyAutoArray#635),
lever L2 of the PyAutoPulse campaign `interferometer_large_mask_aris`
(https://github.com/PyAutoLabs/PyAutoPulse/issues/62). Merged 2026-10-17, library first:

- **Library** — https://github.com/PyAutoLabs/PyAutoArray/pull/636 (MERGED): new serial-numba
  `curvature_direct_conv_symmetric` (columns ranked by ascending `ymin`, row-restricted
  convolution, ranked-CSC gather + mirror; every entry bit-identical to `curvature_direct_conv`),
  routed when the work fraction f ≤ `interferometer_direct_conv_symmetric_max_work_fraction`
  (default 0.7; 0 disables); the route cost model scales `t_dc` by min(1, κf), κ = 1.32;
  non-finite mapping weights fall back to the full kernel. Parallel path unchanged.
- **Write-up** — https://github.com/PyAutoLabs/autolens_profiling/pull/425 (MERGED):
  `results/notes/interferometer_direct_conv_symmetric_2026_10.md` (decision rule, tall-column
  insight, RAL real-data Aris SPT2319-55 witness 1.49×/1.53×/1.58× at 1,459/2,577/5,746
  vertices with log L to round-off, FFT-arm caveat ~1.02× over the previous default at 1,459)
  and the `interferometer_likelihood` campaign journal entry.

Human decisions: 2026-10-16 (on #635) rank by `ymin` and raise the gate 0.5 → 0.7;
2026-10-17 interferometer CPU work is closed — the remaining L2 scratch (scripts, patches,
logs, result JSON copies) was archived out of the worktree; RAL copies and the PRs hold the
evidence.


## Original prompt

# direct_conv curvature kernel: convolve only the rows later-ranked columns need, then mirror

Type: feature
Target: PyAutoArray
Repos:
- PyAutoArray
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: formalised
Issued: 2026-10-16
Consequence: glance
Witness: on the Aris 512x512 geometry (extent 341², ~91k masked pixels, 1,428–5,712 vertices) the numba direct_conv curvature matrix reproduces the library's upper triangle exactly (full-matrix difference = the library's own F asymmetry, ~1e-15 relative) and is >=1.6x faster at 2,540 and 5,712 vertices on a quiet core (RAL, ABBA spread <=1.01); the #632 route model is recalibrated on the new timings. Revised 2026-10-16 by the human after RAL 411833 measured 1.76x / 1.74x / 1.66x (PyAutoPulse#62 comment 6213885428); original witness asked >=1.8x at 2,577 and <=1e-15.
Review-minutes: 3
Unattended: ready

Profiled 2026-10-15 (session 3e3dea38, main 17caf228): at 512x512 the numba `curvature_direct_conv`
kernel is 96–98% of a likelihood call (34 s at 2,577 vertices, 41 s at 5,746). F is symmetric, so each
column's convolution only needs the extent rows spanned by columns ranked after it (sort columns by y),
clipped to the mask's x-range; gather only the upper triangle (CSC layout, 32 vs 63 ms at 1,405) and
mirror. Exact to 2e-16 (prototype `aris_research/kern.py::kC`, temporary). Work fraction on paper
0.60x at 125x125, 0.42x at 512x512. Measured: 125x125 1.10x / 0.82x (gather+mirror overhead cancels —
not worth it there); 512 synthetic (341², 91k px, 1,428 vtx, nnz 274k) 2.5x uncontended (63 → 25 s)
but only 1.03–1.10x under load 5. Quiet-core re-measure (RAL 411833, 2026-10-16, main e59d5fa9): 1.76x / 1.74x /
1.66x at S 1,428 / 2,540 / 5,712, library 22–24 s per call — the 2–2.5x was not reproduced. If it holds, direct_conv likely beats FFT at 1,459 vertices too (28.3 s FFT), so the
#632 cost-model constants need refitting (extent-dependent kernel work). Keep a kill switch; large
extents only (gate on extent size or let the route model decide). Campaign
https://github.com/PyAutoLabs/PyAutoPulse/issues/62; related Pulse task
interferometer_fixed_mapper_curvature_preload (the bigger win for fixed-lens source_pix[1] phases).
