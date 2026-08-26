# slam_source_pix_nn pairs reg.Adapt with a Delaunay-family mesh and cannot jit

Type: bug
Target: autolens_profiling
Repos:
- autolens_profiling
Difficulty: small
Autonomy: supervised
Priority: high
Status: formalised

`_slam_source_pix_nn_model` (`scripts/misc/searches/_setup.py:1425`) builds
`al.mesh.DelaunayNN` with `regularization=af.Model(al.reg.Adapt)`. That
combination cannot run under `jax.jit`.

PyAutoArray documents the rule in
`autoarray/inversion/regularization/constant.py`: on the Delaunay mesh family
(`Delaunay`, `DelaunayNN`, `KNearestNeighbor`, `KNNBarycentric`) the neighbors
come from a direct `scipy.spatial.Delaunay` call on the traced source-plane
mesh grid, so a non-split scheme raises `TracerArrayConversionError` under
jit/grad — **use a split-family scheme there**.

TRACEBACK (RAL 340210 tasks 5 and 6, ~52 s each, 2026-08-25) enters through
the regularization, not the mesh interpolator:

    linear_obj.py:171            regularization_matrix
      regularization/adapt.py:251      regularization_matrix_from
        mesh/mesh_geometry/delaunay.py:151   neighbors
          scipy/spatial/_qhull.pyx:1874      Delaunay.__init__

Every sibling target obeys the rule and runs: `delaunay_nn` is DelaunayNN +
`ConstantSplit` (completed, 3,230 s, logZ 30591.09); `knn` is KNearestNeighbor
+ free `AdaptSplit`; `slam_source_pix` is `RectangularRTUAdaptImage` + `Adapt`,
which is fine because the rectangular family has analytic neighbors.
`slam_source_pix_nn` is the only one that crosses the boundary.

FIX: use `al.reg.AdaptSplit` — the adapt-family split scheme — in
`_slam_source_pix_nn_model`. One line. Then resubmit the two reference rows
(`InferenceRefs_v1`, issue #161), which are the only thing this blocks.

DECISION OWED BEFORE THE FIX LANDS. `_setup.py:1428` records the W4 human call
as "same free `al.reg.Adapt` regularization ... so the mesh choice is isolated
with the regularization scheme held fixed", i.e. the target exists to compare
RTU vs DelaunayNN *at fixed regularization*. Moving this arm to `AdaptSplit`
changes mesh AND regularization, so the pair no longer isolates the mesh. Two
ways out, and it is a science call, not an implementation one:

  (a) give `slam_source_pix` a matching `AdaptSplit` variant so the comparison
      is restored at split regularization; or
  (b) accept the confound and record it on both targets' `notes` and in
      `targets/REFS_V1_HARVEST.md`.

NOT a PyAutoArray defect. An earlier read of this failure blamed
`autoarray/inversion/mesh/interpolator/sibson.py:555` and proposed writing a
jit-safe Sibson path; that was wrong — the call site was guessed from a grep
rather than read off the traceback above, and no library change is needed.
