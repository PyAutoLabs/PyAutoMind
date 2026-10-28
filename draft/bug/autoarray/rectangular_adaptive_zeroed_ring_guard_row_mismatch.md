# Rectangular adaptive meshes: zeroed_pixels ring zeroes a live row and misses a dead guard row

Type: bug
Target: autoarray
Repos:
- PyAutoArray
Themes:
- pixelization
Difficulty: small
Autonomy: supervised
Priority: normal
Status: formalised
Consequence: judge
Epic: cluster-strong-lensing
Filed: 2026-10-28

Found during Source & Cluster arc phase 4a (PyAutoArray#659); human said "file this yes" (2026-10-28).

On the adaptive rectangular meshes (RectangularBilinearAdapt*, RectangularRTUAdapt*) the guard ring is
lopsided in y. Node rows map to unit-CDF `U_y = (n_y - r - 1)/(n_y - 3)` (mesh_geometry/rectangular.py
`edges_transformed`), so rows 0 and 1 are dead guard rows (U_y > 1, no data mapped), while row n-1
(U_y = 0 edge) is LIVE. Columns are symmetric (0 and n-1 are guards). The `zeroed_pixels` outer-ring
edge zeroing assumes a symmetric one-pixel guard ring, so it forces live row n-1 to zero and leaves dead
guard row 1 unzeroed (free to take arbitrary values only constrained by regularization).

Work: confirm with a mapping-matrix column-sum per row; decide the right fix (make the node layout
symmetric, or make the zeroed set match the true guard rows) and its effect on reconstructions,
regularization and the phase-4a area tests
(test_autoarray/inversion/pixelization/mesh_geometry/test_areas_for_magnification.py, which pins guard
cells = zero area/zero mapping but deliberately not this mismatch). Measure likelihood/μ change on
autolens_workspace_test scripts/imaging/mesh_magnification.py.
