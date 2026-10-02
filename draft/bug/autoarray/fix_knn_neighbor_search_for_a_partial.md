# Fix KNN neighbor search for a partial final point block

Type: bug
Target: PyAutoArray
Repos:
- PyAutoArray
- autolens_workspace_test
Difficulty: small
Autonomy: supervised
Priority: high
Status: formalised
Issued: 2026-10-02
Issue: https://github.com/PyAutoLabs/PyAutoArray/issues/609
Consequence: glance
Witness: At N=130 with point_block=128, exact tail-node queries select indices128/129 with zero distance; eager/JIT results match a brute-force oracle at block boundaries for both KNN variants.
Review-minutes: 5
Unattended: ready

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
