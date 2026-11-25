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
