# CurvatureMask / FourthOrderMask regularization: measure and normalise their null space

Type: bug
Target: autoarray
Repos:
- PyAutoArray
Themes:
- regularization
- evidence
Difficulty: small
Autonomy: supervised
Priority: low
Status: formalised
Consequence: judge
Review-minutes: 5
Witness: the spectrum of H for CurvatureMask and FourthOrderMask is measured on rectangular fixtures; if they are intrinsic, log det H uses the pseudo-determinant over their full null space and test_intrinsic_log_det.py pins it.
Filed: 2026-11-09

## Context

PyAutoArray#682 (PR #683) normalises log det H with the pseudo-determinant for schemes whose H has the constant vector
as an exact null mode (`has_constant_null_mode`), measured for Constant/ConstantSplit/Adapt/AdaptPower/AdaptSplit/
AdaptSplitPower. CurvatureMask and FourthOrderMask were left unchanged: as higher-order difference operators they may
have a larger null space (constant plus linear trends), which grounding one pixel does not remove. Measure their
spectra; if they are intrinsic, extend the pseudo-determinant to the full null space (ground as many pixels as its
dimension, or deflate the measured null basis) and add them to the flag test.
