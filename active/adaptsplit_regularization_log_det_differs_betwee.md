# AdaptSplit regularization log-det differs between numba and JAX backends

Type: bug
Target: PyAutoArray
Repos:
- PyAutoArray
Difficulty: large
Autonomy: supervised
Priority: high
Memory: reading-queue.md; wiki/lensing/sources/dark-matter-substructure.md; wiki/galaxies/sources/massive-ellipticals.md
Status: formalised
Issued: 2026-10-15
Consequence: glance
Witness: at identical parameters on the Aris interferometer setup, numba and JAX log_det_regularization_matrix_term agree to <1e-3 (currently 2443.22 vs 2561.98), with a unit test pinning the value on an ill-conditioned AdaptSplit matrix
Review-minutes: 3
Unattended: ready

At identical parameter vectors, the NumPy/numba and JAX likelihoods of a Delaunay + `AdaptSplit`
interferometer inversion differ by ~20-270 in log likelihood (old 125x125 mask, 1405-5526 vertices)
and ~1 on a 512x512 mask. Chi-squared, curvature matrix, data vector and curvature log-det are
identical; the whole difference is `log_det_regularization_matrix_term` (e.g. 2443.22 numba vs
2561.98 JAX). The AdaptSplit regularization matrix is extremely ill-conditioned (entries sum to
~1.4e-5), so its log-determinant is backend dependent. JAX eager vs jit agree to 1e-8.

Consequence: log evidences are not comparable across backends; a user mixing backends across
pipeline phases (or comparing models) gets inconsistent evidences. Also ~1 in 4 random draws is
non-positive-definite: numba raises LinAlgError (resample), JAX returns -inf — same behaviour
should be checked for consistency.

Do: locate where each backend computes the regularization log-det (Cholesky vs slogdet, jitter /
diagonal regularisation, dtype), decide the numerically correct value (e.g. compare to an
mpmath/high-precision reference on a small matrix), make both backends compute it the same robust
way, and add a regression test. Consider whether AdaptSplit's matrix construction itself should be
better conditioned.

Evidence: scratchpad /tmp/claude-1000/-home-jammy-Code-PyAutoLabs/50c8c6cd-6ac2-47c2-9290-7ee73f9c4315/scratchpad/aris/PROGRESS3.md, PROGRESS4.md, step7/bench.py (--check mode), step8/. PyAutoArray ccddfba6.

<!-- formalised by the Intake (Conception) Agent on 2026-10-15 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/aaade95e-3f22-4661-b77d-365d91380803/scratchpad/intake3/adaptsplit_logdet.md -->
