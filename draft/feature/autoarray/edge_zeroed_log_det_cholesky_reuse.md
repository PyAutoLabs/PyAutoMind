# Reuse the fnnls Cholesky factor for the log det when edge-zeroed pixels are solved out (rect mesh, autolens_profiling#332)

Type: feature
Target: autoarray
Repos:
- PyAutoArray
- autolens_profiling
Themes:
- inversion
- numba-cpu
Difficulty: small
Autonomy: supervised
Priority: low
Status: draft
Consequence: glance
Witness: on the alma rectangular 39² edge-zeroed system (1369 of 1521 solved), `log_det_curvature_reg_matrix_term` takes the factor-reuse path and is faster than the dense Cholesky (47.7 ms in #332), agreeing to <= 1e-8 nat; Delaunay (no subset) and every existing log-det test unchanged.
Review-minutes: 6
Lane: local-dev
Epic: interferometer-likelihood-campaign
Filed: 2026-09-27

## Context

`log_det_curvature_reg_matrix_term` (PyAutoArray `autoarray/inversion/inversion/abstract.py:998-1078`)
reads log det(F + H) off the fnnls Cholesky factor via `log_det_from_passive_cholesky_from`
(`autoarray/inversion/inversion/inversion_util.py:753`). It does so only if `_nnls_factor_ids_cover`
(`abstract.py:1081-1096`) sees the solve cover the whole reduced system (no subset, or the
identity subset).

With `use_edge_zeroed_pixels` the rectangular mesh solves a strict subset (`solve_ids_to_keep`,
`abstract.py:532`), so the check fails and the dense route runs. autolens_profiling#332
`levers.logdet` (alma r3.5) measured:

- Delaunay: reused 15.2 ms against dense 38.3 ms (Δ 0 nat).
- rect: reused 47.7 ms = dense 47.7 ms. The miss costs up to 2.7 % of the 1.76 s call.

## What

1. Determine which matrix the evidence log det is taken over when pixels are edge-zeroed: the
   subset system the factor covers, or the full reduced matrix. That decides whether the factor can
   be used directly or needs a block / Schur extension.
2. If it is equivalent, extend `_nnls_factor_ids_cover` / the fast path to the subset case. Add a
   unit test against the dense value.
3. Only 947 of the solved columns are passive at alma rect, so measure the realised gain before
   merging.
