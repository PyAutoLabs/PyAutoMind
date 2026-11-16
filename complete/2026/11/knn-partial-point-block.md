## knn-partial-point-block
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/609
- library-pr: https://github.com/PyAutoLabs/PyAutoArray/pull/684 (MERGED 2026-11-09, stacked on PyAutoArray#683)
- completed: 2026-11-09
- released: PyAutoArray 2026.11.12.1 (tag contains the merge)
- closed-out: 2026-11-15 by a health-review session — the fix shipped outside the Mind workflow, so the planned.md entry outlived its closed issue and failed PyAutoMind Registry Reconcile daily (2026-11-11 → 2026-11-15).
- summary:
  - `get_interpolation_weights` sliced each point block with `lax.dynamic_slice`, which clamps the last partial block's start to N - B: the N mod B tail vertices were never searched and earlier vertices came back under the tail indices, so split-regularization rows lost their self term.
  - Fix pads the point array to whole blocks so every slice starts at bi * B (padded rows already masked). Brute-force oracle tests at block boundaries (eager + jit, k=3 and k=10, both KNN interpolators); the numerics audit's strict xfail witness was promoted to a passing regression in `test_numerics_audit.py`.
  - Needed PyAutoArray#683 (pseudo-determinant for intrinsic regularization log det H) first: the now-correct KNN split H exposed the jitter-held constant mode in jax_grad/knn.py (the 2026-10-29 finding).

## Original prompt

# Fix KNN neighbor search for a partial final point block

Type: bug
Target: PyAutoArray
Repos:
- PyAutoArray
- autolens_workspace_test
Difficulty: medium
Autonomy: supervised
Priority: high
Status: formalised
Issued: 2026-10-02
Issue: https://github.com/PyAutoLabs/PyAutoArray/issues/609
Consequence: judge
Witness: At N=130 with point_block=128, exact tail-node queries select indices128/129 with zero distance; eager/JIT results match a brute-force oracle at block boundaries for both KNN variants.
Review-minutes: 5
Unattended: ready
Lane: any

# Fix KNN neighbor search for a partial final point block

Type: bug
Target: autoarray
Repos:
- PyAutoArray
- autolens_workspace_test
Difficulty: small
Autonomy: supervised
Priority: high
Witness: At N=130 with point_block=128, exact tail-node queries select indices128/129 with zero distance; eager/JIT results match a brute-force oracle at block boundaries for both KNN variants.
Review-minutes: 5

Found while executing PyAutoArray#603, the approved final numerics audit. User authorization from the original audit prompt: "Any bug found is filed separately; this task is the audit, not the fixes."

In autoarray/inversion/mesh/interpolator/knn.py:get_interpolation_weights, lax.dynamic_slice clamps a requested final-block start when N is not divisible by point_block. For N=130 and default point_block=128, the last requested start128 actually slices from2. The code still labels candidate rows with start128 and masks only2 rows, excluding or mislabelling the true final nodes.

Minimal witness on untouched main: points (0,0) through (129,0), query exact points128 and129, k_neighbors3. Expected first neighbors128 and129 with zero distance. Actual selected indices are [127,126,125] for both, with distances[1,2,3] and[2,3,4]. Both InterpolatorKNearestNeighbor and InterpolatorKNNBarycentric share the selection path.

Fix in a separate task by padding point blocks and masking padded rows, or otherwise keeping slice start, point coordinates and emitted indices consistent. Test N below/equal/above block size and nonmultiples (including129/130/257), compare eager/JIT neighbor indices/distances with a brute-force oracle on unique-distance data, cover both interpolation variants, and promote the audit's strict expected-failure regression to ordinary passing coverage. Preserve memory-bounded block behavior and full-block results. No production repair is part of audit#603.

<!-- formalised by the Intake (Conception) Agent on 2026-10-02 from file:.worktrees/autoarray-bundle-1/scratch/knn-tail-bug.md -->


## Finding 2026-10-29 (arc phase 4b, PyAutoArray#665) — NOT a mechanical fix

The padded-slice fix (patch on https://github.com/PyAutoLabs/PyAutoArray/issues/609#issuecomment-6509071399)
passes a brute-force oracle eagerly and under jit, but breaks autolens_workspace_test
`scripts/imaging/jax_grad/knn.py` variant B (KNearestNeighbor + AdaptSplit inner=0.1 outer=10):
eager/jit drift 2e-9 to 6e-9, and autodiff vs finite differences off 1–3% on 3 parameters. The bug hid the zeroed
circle-edge ring (appended last); fixing it makes those nodes neighbours. Human split it out of 4b.
Size is now medium (investigation first). Consequence should be judge, not glance: the fix changes
KNN likelihoods for nearly every mesh (N is rarely a multiple of 128).
