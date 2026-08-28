# sparse-interferometer-unequal-sigma-guard

Follow-up from #499 close-out. `InterferometerSparseOperator` builds `W~ = Re(FᴴWF)` from the
real-part sigma only (`psf_precision_operator_from` → `noise_map_real`), exact only when every
visibility has `sigma_real == sigma_imag`; unequal sigmas made the sparse curvature matrix
silently disagree with the dense path (5e-16 → 5e-10..3e-2 relative).

## Shipped
- PyAutoArray#503 — `Interferometer.apply_sparse_operator` raises `DatasetException` (count of
  offending visibilities, max relative difference, both workarounds); docstring Precondition notes;
  two tests (unequal raises, equal-non-uniform passes). Only entry point that sees a noise map.

## Decision — general two-operator extension: NOT doing it
Exact unequal-sigma curvature expands to a translation-invariant term (today's kernel reweighted
by (wr+wi)/2) plus a pixel-SUM-indexed term ½(wr−wi)cos(φ_i+φ_j); the latter needs a second,
sum-indexed kernel and assembly path in both JAX and numba (2x setup, 2x Khat, ~2x FFTs). No known
dataset has per-part-unequal sigma (simulator constant; measurement-set weights are scalars).
Guard is the right cost/benefit; revisit only if such a dataset appears.

## Original prompt

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
