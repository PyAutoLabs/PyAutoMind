## simple-cluster-profiling
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/536
- completed: 2026-11-28
- workspace-pr: https://github.com/PyAutoLabs/autolens_profiling/pull/537
- mind-pr: https://github.com/PyAutoLabs/PyAutoMind/pull/608
- summary: Simple now uses the reviewed gallery's velocity-dispersion dPIE model and its five-plus-two observed catalogue in both cluster likelihoods. The six-image b0 runs are archived. The cache guard validates the scaling catalogue with the consuming reader. Local CPU JAX FP64 warm medians: source plane 0.518 ms; image plane 8.918 ms on the standard 1″ grid, which recovers only six of seven images and so is diagnostic. A paired run of the full solved image-plane likelihood measured 11.778 ms at 1″ against 51.101 ms at 0.25″, which recovers all seven within 0.01″: 4.34× the cost, for one model and two solved source centres. The results are in results/cluster/image_plane/simple/jax_cpu_na_fp64/local_laptop/experiments/starting_grid_spacing. The production solver settings are unchanged. The default grid is chosen in Cluster usability phase 3.2, and phase 3.5 (Pandora profiling) was blocked on this PR. While shipping, the R6 lazy-sparse default broke the fixed-light "drop" test; that was fixed separately in autolens_profiling#539 (record complete/2026/11/fixed-light-dense-r6.md).

## Original prompt

# Simple cluster CPU profiling

Type: research
Target: autolens_profiling
Epic: cluster-usability
Consequence: judge
Issued: 2026-11-25
Issue: https://github.com/PyAutoLabs/autolens_profiling/issues/536

> ok great, update the Cluster usability epic with the MACS J0416 merges and the 331 live Eyes figures, then let’s move on to profiling, starting with Simple

Use the existing source-plane and image-plane benchmarks on a fresh Simple dataset. Preserve the existing cache, validate the member table with its consuming reader and test missing, empty, malformed and valid inputs. Record first-call and warmed CPU timings, solver settings and NumPy agreement. Put the comparison in Science scratch for review.

Use the reviewed gallery’s velocity-dispersion dPIE model and its five-plus-two observed catalogue for Simple. Preserve the earlier six-image measurements as historical evidence and distinguish numerical parity from image recovery.
