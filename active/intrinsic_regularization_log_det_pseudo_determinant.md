# Intrinsic regularization log det H is set by the 1e-8 jitter: use the pseudo-determinant

Type: bug
Target: autoarray
Repos:
- PyAutoArray
Themes:
- inversion
- regularization
- evidence
- jax-gradients
Difficulty: medium
Autonomy: supervised
Priority: high
Status: formalised
Consequence: judge
Review-minutes: 10
Witness: for every intrinsic scheme (Constant, ConstantSplit, Adapt, AdaptPower, AdaptSplit, AdaptSplitPower) log det H equals the pseudo-determinant (sum log P_b + log det of H grounded on one pixel per block) independently of the jitter; autolens_workspace_test jax_grad/delaunay.py log det H eager/jit agree to 1e-10 (1.2e-8 on main); unit test pins has_constant_null_mode to the measured spectrum of every scheme.
Filed: 2026-11-09
Issued: 2026-11-09
Issue: https://github.com/PyAutoLabs/PyAutoArray/issues/682

## Symptom

Found while investigating PyAutoArray#609 (comment https://github.com/PyAutoLabs/PyAutoArray/issues/609#issuecomment-6726735167).
The smoothness schemes build H whose rows sum to zero by construction, so the constant vector is a null mode
held up only by the net 1e-8 diagonal jitter. Measured (Delaunay and rectangular fixtures): lambda_min(H) = 1.000e-8
with eigenvector exactly 1/sqrt(P) for Constant, ConstantSplit, Adapt, AdaptPower, AdaptSplit, AdaptSplitPower;
zeroth/kernel schemes have lambda_min ~ O(1). log det H therefore contains log(1e-8 + O(eps*||H||)), and at large
coefficients (AdaptSplit outer=10, ||H|| ~ 3e4) rounding moves it by ~1e-4 relative: Delaunay + AdaptSplit on main
shows log det H eager/jit drift 1.2e-8 (figure of merit 1.6e-9), and once #609 is fixed KNN + AdaptSplit fails
jax_grad/knn.py (eager/jit 3.9e-9 vs the 1e-10 bar, AD vs FD off 1-3%).

## Fix

Treat H as the precision of an intrinsic GMRF: normalise with the pseudo-determinant over the non-constant modes.
For a symmetric H with null vector 1/sqrt(P), pdet(H) = P * det(H with one row/column deleted), which stays sparse and
static-indexed under jit. Gate per scheme with an explicit `has_constant_null_mode` attribute (False by default;
zeroth-term subclasses explicitly False; CurvatureMask/FourthOrderMask unchanged — higher-order operators may have
larger null spaces, follow-up). Approved by the maintainer 2026-11-09 to change likelihood values: every fit using
these six schemes shifts log evidence by a constant +0.5*ln(1e8) = +9.21 nats per regularized mapper; parameter
inference unchanged except noise removal. Ships BEFORE the #609 KNN fix (two-PR decision, 2026-11-08).
