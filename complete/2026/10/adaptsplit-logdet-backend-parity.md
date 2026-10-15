## adaptsplit-logdet-backend-parity
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/627
- completed: 2026-10-15
- library-pr: https://github.com/PyAutoLabs/PyAutoArray/pull/631
- merge: 0377eeaafec8fc1c4ccd289fbfb7e8c24a32fad3 (head da5f6cef; commits f052e381 fix + da5f6cef test guard)
- pending-release: PyAutoArray@https://github.com/PyAutoLabs/PyAutoArray/pull/631
- root-cause: the numba and JAX backends built different AdaptSplit H matrices, not different log-dets. `adaptive_pixel_signals_from` counted zero-weight mapping entries, and scipy and the JAX Delaunay walk pick different triangles for data points lying exactly on a vertex or edge, so the zero-weight entries landed on different pixels. Every log-det factorization agreed to 2e-8 on the same H.
- fix: new `exclude_zero_weight_mappings` keyword on `adaptive_pixel_signals_from`, driven by an interpolator class attribute: True on InterpolatorDelaunay / InterpolatorDelaunayNN, False on the base interpolator and KNN.
- decision: the first independent review returned FINDINGS — KNNBarycentric clips negative weights to exactly 0 region-wide, so excluding zero weights there would change whole-region signals and add a discontinuity. The human chose (b) 'Delaunay only (Recommended by review)' on 2026-10-15 (https://github.com/PyAutoLabs/PyAutoArray/issues/627#issuecomment-6200058449); the second review on f052e381 was CLEAN.
- witness: PASS — synthetic ill-conditioned AdaptSplit: H parity 3.6e-15, log-dets 2.1e-9 apart, both within 1.7e-9 of a 50-digit reference; Aris not re-run.
- behaviour-note: evidence values change on Delaunay / DelaunayNN meshes when data points sit exactly on mesh vertices or edges. KNN, KNNBarycentric and rectangular meshes are bit-identical.
- ci-note: the first CI run (38795253065) went red on the no-JAX leg because the new KNN test lacked `importorskip("jax")`; fixed by da5f6cef before merge.
- out-of-scope: the absolute 1e-8 jitter in the split regularization builders makes the log-det round-off-dominated at max(coeff)^4 ≳ 1e6. Separate work, unfiled. Scope merged = scope filed except this note.
- gate: tests PyAutoArray 2039 passed/4 xfailed, PyAutoGalaxy 1357, PyAutoLens 832/1 xfailed · smoke 151/151 · review CLEAN (independent Opus, f052e381) · Heart RED under the recorded live-human development override (session 3e3dea38; reasons on the active.md row / #626; permitted commit/push/PR-open, merge separate — merged by human /prm 2026-10-15) · witness PASS.
- campaign: PyAutoPulse#62, task `interferometer_large_mask_aris`.
- where-to-pick-up: #628 (interferometer-numba-route-gate) is next on the PyAutoArray claim, then #629 (delaunaynn-wide-row-overhead) by the human's ordering.

## Original prompt

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
