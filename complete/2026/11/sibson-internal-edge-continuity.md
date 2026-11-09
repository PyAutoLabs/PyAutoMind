## Shipped — 2026-11-09

Sibson (natural-neighbour) weights at and near internal Delaunay edges fixed: natural-neighbour areas are summed from
per-edge segment terms of the stolen regions, with the circle through the query formed only on cavity-BOUNDARY edges,
so internal edges are never singular (the Watson per-triangle decomposition built a collinear circle there).

- PRs: https://github.com/PyAutoLabs/PyAutoArray/pull/685 (merged af80e69), https://github.com/PyAutoLabs/autolens_workspace_test/pull/359 (merged 5857d49); issue https://github.com/PyAutoLabs/PyAutoArray/issues/610
- Plan (approved 2026-11-09, split by repo, tier judge set by maintainer over declared glance): https://github.com/PyAutoLabs/PyAutoArray/issues/610#issuecomment-6739352308
- Same algorithm in `_sibson_single_from_tables` (NumPy/JAX) and `_sibson_numba` (parallel + serial). Hull-edge linear
  rule only on exact hull collinearity; round-off areas snapped to 0 before normalising; rows compacted (no -1 holes).
- Witness: square centre 1/4 x4 (both diagonals, both windings); internal-edge probes Lipschitz down to nextafter;
  partition/non-negative/affine; independent Voronoi-clipping oracle <= 1e-10; NumPy = numba = JAX-jit. 3 audit strict
  xfails promoted; thin-triangle test re-pinned to the correct (oracle-checked) behaviour.
- Also: DelaunayNN magnification areas now integrate the Sibson basis (shared kNN quadrature): mesh_magnification
  identity +0.04% (dual areas would have been -2.65% with the corrected weights).
- Numba serial kernel ~20% faster than before at HST size; parallel within noise.
- Follow-up: re-measure draft/bug/autoarray/sibson_serial_kernel_loses_allocation_hoisting.md on the new body.

- pending-release: PyAutoArray@https://github.com/PyAutoLabs/PyAutoArray/pull/685

## Original prompt

# Fix Sibson interpolation at internal edges

Type: bug
Target: PyAutoArray
Repos:
- PyAutoArray
- autolens_workspace_test
Difficulty: large
Autonomy: supervised
Priority: high
Status: formalised
Issued: 2026-10-02
Issue: https://github.com/PyAutoLabs/PyAutoArray/issues/610
Consequence: judge
Consequence-note: maintainer set judge (declared glance) on 2026-11-09 — DelaunayNN likelihood values change; plan https://github.com/PyAutoLabs/PyAutoArray/issues/610#issuecomment-6739352308
Witness: Square-symmetry center weights are 1/4 each; near-edge weights remain nonnegative, sum to one, and agree continuously from both sides under eager/JIT execution.
Review-minutes: 15
Unattended: ready

# Fix Sibson interpolation at internal edges

Type: bug
Target: autoarray
Repos:
- PyAutoArray
- autolens_workspace_test
Difficulty: large
Autonomy: supervised
Priority: high
Witness: Square-symmetry center weights are 1/4 each; near-edge weights remain nonnegative, sum to one, and agree continuously from both sides under eager/JIT execution.
Review-minutes: 15

Found during approved audit PyAutoArray#603. Original user instruction: "Any bug found is filed separately; this task is the audit, not the fixes."

In autoarray/inversion/mesh/interpolator/sibson.py:_sibson_single_from_tables, every on-edge query is replaced with seed-triangle barycentric weights, including internal edges where off-edge natural neighbors contribute. For square points [(-1,-1),(-1,1),(1,-1),(1,1)], query(0,0), independent symmetry requires four weights0.25 and interpolated y*x=0. Actual weights0.5 for opposite diagonal nodes yield1. Lattice mesh boundary sweep found jumps up to0.02680921 at +/-1e-8 around internal edge midpoints.

Near the square center at (+/-1e-8,0), cancellation yields returned positive weights summing1.123877166 and interpolated y*x=-1.123877166, with no overflow/degenerate flag. Code normalizes signed contributions before discarding negative weights. At epsilon0.01 weights sum1 and y*x is near0; error worsens at1e-6 and1e-8.

Plan a separate algorithmic repair preserving full natural-neighbor cavities at internal edges, using a hull-edge limiting rule only where appropriate, and robustly handling area cancellation before normalization/filtering. Validate independent symmetric and asymmetric reference fixtures, both-sided finite and nextafter edge probes, affine precision, partition/nonnegative support, eager/JIT parity and source recovery. Promote audit strict xfails after repair. No production fix is part of audit#603; shared worktrees remain claimed by the audit until shipping.

<!-- formalised by the Intake (Conception) Agent on 2026-10-02 from file:.worktrees/autoarray-bundle-1/scratch/sibson-edge-bug.md -->
