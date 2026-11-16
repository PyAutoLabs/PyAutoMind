## sibson-internal-edge-continuity
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/610
- library-pr: https://github.com/PyAutoLabs/PyAutoArray/pull/685 (MERGED 2026-11-09)
- completed: 2026-11-09
- released: PyAutoArray 2026.11.12.1 (tag contains the merge)
- closed-out: 2026-11-15 by a health-review session — the fix shipped outside the Mind workflow, so the planned.md entry outlived its closed issue and failed PyAutoMind Registry Reconcile daily (2026-11-11 → 2026-11-15).
- summary:
  - The Watson per-triangle decomposition formed a circle through the query and every cavity-triangle edge, including cavity-interior edges; on an internal edge that circle is collinear, so the code fell back to the seed triangle's barycentric row (square centre 0.5/0.5 instead of 0.25 x 4), and near one the cancelling terms were normalised before clipping (row sums 1.12).
  - Natural-neighbour areas are now summed from per-edge segment terms of the stolen regions (stored circumcentres on interior edges, the circle through q only on cavity-boundary edges); internal edges are never singular. Same algorithm in the NumPy/JAX and numba bodies; numba serial ~20% faster at HST size.
  - DelaunayNN magnification areas now integrate the Sibson basis (shared kNN quadrature): identity-lens magnification bias went from -2.65% to +0.04% once internal-edge weights were corrected.
  - Validation: independent Voronoi-clipping oracle (<=1e-10), square centre both diagonals and windings, hexagon 1/6, edge probes, affine/partition/support, hull limit, NumPy/numba/JAX-jit parity; the audit's 3 strict xfails promoted.

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
Consequence: glance
Witness: Square-symmetry center weights are 1/4 each; near-edge weights remain nonnegative, sum to one, and agree continuously from both sides under eager/JIT execution.
Review-minutes: 15
Unattended: ready
Lane: any

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
