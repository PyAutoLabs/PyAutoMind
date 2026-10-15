# Reuse one Cholesky factor of F+H for the reconstruction solve and the log det (numpy, non-positive-only path)

Type: feature
Target: PyAutoArray
Repos:
- PyAutoArray
Difficulty: small
Autonomy: safe
Priority: high
Status: formalised
Consequence: glance
Witness: on the Aris 125x125 interferometer setup (Delaunay + AdaptSplit, use_positive_only_solver=False, numba route) one likelihood call drops by >=15% at 1,405 vertices and >=35% at 2,947 vertices, with reconstruction unchanged to 1e-10 relative and log_det_curvature_reg_matrix_term unchanged to 1e-9
Review-minutes: 3
Unattended: ready

Profiled 2026-10-15 (session 3e3dea38, PyAutoArray main 17caf228) on Aris's SPT2319-55 data with
`use_positive_only_solver=False`: the numpy path factorizes the same SPD matrix `F + H` twice per
likelihood call — `np.linalg.solve` (LU) in `inversion_util.reconstruction_positive_negative_from`
(called from `AbstractInversion.reconstruction`, abstract.py ~760) and `np.linalg.cholesky` in
`_log_det_symmetric_from` for `log_det_curvature_reg_matrix_term`. Together 31% of the call at 1,405
vertices (100 + 70 ms of 0.63 s) and 72% at 2,947 vertices (976 + 741 ms of 2.0–2.4 s). The
positive-only path already reuses its factor (`log_det_from_passive_cholesky_from`); the non-positive
path does not.

Do: when `use_positive_only_solver=False` on the numpy backend, compute one `scipy.linalg.cho_factor`
of `F + H`, solve with `cho_solve`, and take the log det as `2 * sum(log(diag))` of the same factor
(keep the existing `LinAlgError` test-mode guard and the `slogdet` opt-in; JAX path unchanged).
Measured on the saved matrices: 65 ms vs 113+81 ms (1,405) and 612 ms vs 948+654 ms (2,947);
solution relative change 7e-14 / 2e-11; log det identical; non-PD still raises. Optionally fold in
an in-place `F + H` add to drop one S×S copy (10–30 ms). Do NOT use float32 (0.027 nats log-det
error at 2,947; cond(F+H) up to 7e12). Add a test pinning solve + log det against the two-factorization
values. Evidence: session 3e3dea38 scratchpad `report_aris_speedups.md` + `aris_research/la.py`
(temporary); campaign https://github.com/PyAutoLabs/PyAutoPulse/issues/62.
