# Sparse interferometer W~ path silently assumes equal real/imag noise sigma

Type: bug
Target: PyAutoArray
Repos:
- PyAutoArray
- workspaces
Difficulty: medium
Autonomy: supervised
Priority: normal
Issued: 2026-08-28
Status: formalised

# Sparse interferometer W~ path silently assumes equal real/imag noise sigma

Type: bug
Target: PyAutoArray
Repos:
- PyAutoArray
Difficulty: medium
Autonomy: supervised
Priority: normal

## Problem

`InterferometerSparseOperator` builds the real-space operator `W~ = Re(F^H W F)` from a single
NUFFT precision operator. That reduction is only exact when every visibility has equal real and
imaginary noise sigma. With `sigma_real != sigma_imag` the sparse `InversionInterferometerSparse`
curvature matrix disagrees with the dense `InversionInterferometerMapping` path even on the
single-mapper route: measured 5e-16 relative with equal sigmas vs 5e-10 to 3e-2 with unequal
sigmas (geometry dependent). Pre-existing, not introduced by #500. `SimulatorInterferometer` and
real datasets satisfy the equality, so it is latent — but nothing guards it.

## Fix

1. Raise a clear `InversionException` (or in `Interferometer.apply_sparse_operator`) when the noise
   map has unequal real/imag sigma for any visibility, with a unit test. Do this first.
2. Assess extending the operator to the general case (two precision operators, real- and
   imag-weighted, combined in `apply_operator`) — only if the cost is modest; otherwise the guard stands.

## Context

Found 2026-08-28 while shipping #499 / #500. The `misc/jax_assertions/fit_interferometer_sparse_operator.py` parity
scripts in both test workspaces document the limitation in their
docstrings and deliberately use equal-sigma noise maps; they need no change.

<!-- formalised by the Intake (Conception) Agent on 2026-08-28 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/b766a19b-260c-4b56-8d19-072fa9a34b28/scratchpad/intake_unequal_sigma.md -->
