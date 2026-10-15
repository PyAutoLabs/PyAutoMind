# Interferometer numba route gate should scale with mask size

Type: feature
Target: PyAutoArray
Repos:
- PyAutoArray
- autolens_profiling
Difficulty: large
Autonomy: supervised
Priority: normal
Memory: wiki/galaxies/sources/massive-ellipticals.md; wiki/lensing/sources/dark-matter-substructure.md; wiki/galaxies/sources/cosmos-survey.md
Status: formalised
Issued: 2026-10-15
Consequence: glance
Witness: on both the Aris 125x125 (5,496 px) and 512x512 (91,507 px) masks, the default routing picks the faster of numba direct_conv vs NumPy FFT curvature at every tested vertex count (1.4k-5.7k), asserted by a routing test
Review-minutes: 3
Unattended: ready

The factory (`autoarray/inversion/inversion/factory.py` ~L245) routes a NumPy single-mapper
interferometer inversion to the numba `direct_conv` curvature route only when mean non-zeros per
source column <= `interferometer_numba_nnz_per_source_max` (default 60, measured on one reference
geometry). On a 512x512 mask (91,507 masked pixels) the measured crossover is ~140-150 nnz/column:
at 2,577 vertices (106 nnz/col) the default sends numba to the FFT route at 44.1 s vs 34.2 s for
direct_conv (1.29x slower). Measured (s/call, 1 thread):

| vertices (nnz/col) | FFT route | direct_conv |
|---|---|---|
| 1,459 (188) | 28.3 | 38.4 |
| 2,577 (106) | 44.1 | 34.2 |
| 5,746 (48) | 97.3 | 41.2 |

FFT cost scales ~linearly with source pixels (blocks of 128 FFTs over the 682x682 extent) and with
extent size; direct_conv scales with total non-zeros x kernel work. A fixed nnz/column constant
cannot be right for both small and large masks.

Do: replace the fixed gate with a cost model using quantities known at routing time (source pixels
S, total nnz, extent / FFT grid shape), calibrated on the existing measurements (old 125x125 mask
crossover ~60 Delaunay / ~77 rectangular, autolens_profiling#226; this 512x512 data), keeping a
user override. Add tests for the routing decision. Re-measure on both masks.

Evidence: /tmp/claude-1000/-home-jammy-Code-PyAutoLabs/50c8c6cd-6ac2-47c2-9290-7ee73f9c4315/scratchpad/aris/PROGRESS3.md, PROGRESS4.md, step7/, step8/. PyAutoArray ccddfba6.

<!-- formalised by the Intake (Conception) Agent on 2026-10-15 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/aaade95e-3f22-4661-b77d-365d91380803/scratchpad/intake3/interferometer_numba_route_gate.md -->
