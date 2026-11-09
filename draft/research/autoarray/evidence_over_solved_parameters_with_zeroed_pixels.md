# Should the evidence log-dets run over the solved parameters when edge pixels are zeroed?

Type: research
Target: autoarray
Repos:
- PyAutoArray
Themes:
- evidence
- inversion
Difficulty: medium
Autonomy: supervised
Priority: low
Status: formalised
Consequence: judge
Review-minutes: 10
Witness: a written recommendation (with measured evidence shifts across Delaunay/KNN/rectangular meshes with zeroed rings) on whether log det(F+H) and log det H should be restricted to solve_ids_to_keep.
Filed: 2026-11-09

## Question

With `use_positive_only_solver` and `use_edge_zeroed_pixels`, the reconstruction is solved on the kept parameters with
the edge ring fixed to zero, but `log_det_curvature_reg_matrix_term` and `log_det_regularization_matrix_term` run over
all parameters including the zeroed ones. The evidence of the solve actually performed integrates over the kept
parameters only, with conditional prior precision `H_kk` (the zeroed ring then anchors the constant mode). This was
option "K" in the PyAutoArray#609 investigation: prototyped, it passes jax_grad/knn.py but shifts evidences by
model-dependent amounts (+27.2 / +15.0 nats measured). Decide whether it is the correct evidence and, if so, file the
change. Context: https://github.com/PyAutoLabs/PyAutoArray/issues/609#issuecomment-6726735167 ; the
pseudo-determinant (#682) is already in place for the constant mode.
