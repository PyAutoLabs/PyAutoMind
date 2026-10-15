## Summary

Shipped the library phase of #628: the NumPy single-mapper interferometer inversion's
numba-vs-FFT curvature routing now scales with mask size via a two-constant cost model,
replacing the fixed 60 nnz/col gate that mis-routed the Aris 512x512 mask (2,577 vertices,
106 nnz/col → FFT at 44.1 s vs 34.2 s direct_conv).

- pending-release: PyAutoArray@https://github.com/PyAutoLabs/PyAutoArray/pull/632

## What shipped (PyAutoArray#632, merged 2026-10-15, 17caf228)

- Cost model: `t_fft = c_fft·S·pocketfft-work(padded 2ny×2nx)`, `t_dc = c_dc·nnz·ny·nx`,
  c_fft 7.62e-10, c_dc 1.77e-09 — least squares on 9 paired timings (6 bake-off cells from
  autolens_profiling#226 + 3 Aris 512 points); right route at all 9, measured/predicted ratio
  residuals 0.68–1.47.
- `interferometer_numba_nnz_per_source_max` packaged default `null` = cost model; positive =
  hard gate; 0 = numba off.
- New `interferometer_route` setting (None | "numba" | "fft") to force a route.
- `_use_interferometer_numba` takes `extent_shape`; missing extent under the cost model → FFT.
- The #625 DelaunayNN routing pin now asserts the cost model's choice (numba) instead of the
  gate value 60.

## Decision taken (PR labelled decision-taken)

FFT work term = pocketfft cost_guess (factorisation-aware) instead of N log N. Rejected: N log N
(fit-on-all mis-routes Aris 512 at 2,577 vtx — the original bug; fit-on-512 mis-routes two
bake-off cells) and a per-mask-size table. Revert: config
`interferometer_numba_nnz_per_source_max: 60.0`.

## Extent correction

Mask extents are 341² (Aris 512) and 83² (Aris 125); 682 was the padded FFT grid. Aris-125
crossover ≈309 nnz/col because 166 is an awkward FFT length (Bluestein); Aris-512 crossover
≈166 (measured 106–188).

## Witness

PASS — routing test on both mask geometries + live routing-only check: 512 → FFT/numba/numba
at 1,459/2,577/5,746 vtx, 125 → numba at 1,405/2,947/5,526; timings from the prompt table, not
re-run.

## Gate

Tests PyAutoArray 2055 passed/4 xfailed, PyAutoGalaxy 1357, PyAutoLens 832/1 xfailed; smoke
165/165; independent Opus review FINDINGS (1 low doc-only) → fixed 46befdb4 → CLEAN. Heart RED
`release validation FAILED (stage integrate)` at ship — shipped under the live human's
development-only override (session 3e3dea38; commit/push/PR-open); merged by the human via
/prm, answered "merged-unchanged".

Campaign: https://github.com/PyAutoLabs/PyAutoPulse/issues/62 (task `interferometer_large_mask_aris`).

## Scope merged vs filed

Partial by design: the library phase (PyAutoArray) shipped; the phase-2 workspace record
(autolens_profiling re-measurement) did NOT ship and was never claimed. It is re-filed as
`draft/feature/autolens_profiling/interferometer_route_gate_phase2_remeasure.md`.

## Where to pick up

Phase 2: `draft/feature/autolens_profiling/interferometer_route_gate_phase2_remeasure.md` —
re-measure both Aris masks' routing table with the default cost model and record it in the
#226 format (the three autolens_profiling scripts that set the gate explicitly keep hard-gate
meaning). This also covers the campaign's owed Aris after-measurements (PyAutoPulse#62).

## Original prompt

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
