## reuse-cholesky-factor
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/633
- completed: 2026-10-15
- library-pr: https://github.com/PyAutoLabs/PyAutoArray/pull/634
- merge: e59d5fa901e54bf3d9931890067bc3447a5c1232 (head 02aa2e48), merged 2026-10-15T23:27:18Z
- pending-release: PyAutoArray@https://github.com/PyAutoLabs/PyAutoArray/pull/634
- shipped: one cached `scipy.linalg.cho_factor` of a copy of F+H now serves both `reconstruction` (via `cho_solve`) and `log_det_curvature_reg_matrix_term` (2·Σlog diag). It applies only on NumPy, with the positive-only solver off and `log_det_method` cholesky. Every other configuration keeps the old path, and so does a factorization failure or a non-finite diagonal. Error semantics are unchanged. 10 new tests.
- not-done: the optional in-place F+H add was skipped, because `curvature_reg_matrix` and `curvature_matrix` are reused elsewhere and an in-place add would corrupt them. Scope merged = scope filed except this optional item.
- witness: PASS as reworded. solve+log-det went 144.5→50.9 ms at 1,405 vertices and 1,268→373 ms at 2,947. The full likelihood call is −22–24% at 1,405 and −51% at 2,947. The log det is bit-identical and logL agrees to ≤1.1e-11 relative. The reconstruction agrees within conditioning: 1.6e-3 relative at 2,947 vertices, where cond(F+H)=7.7e14, and the new solve is closer to the refined reference than the old LU solve.
- witness-rewording: the filed clause "reconstruction unchanged to 1e-10 relative" cannot be met at cond(F+H)=7.7e14, because no two backward-stable solvers agree to 1e-10 there. The clause was reworded to "within conditioning, closer to the refined reference". The human accepted the reworded witness by merging unchanged (shadow row merged-unchanged, 2026-10-15).
- edge (reviewer non-finding): for a numerically singular matrix with tiny positive pivots, Cholesky now succeeds and returns a huge solution, where the LU used to raise. chi² rejects that sample either way.
- gate: tests PyAutoArray 2065 passed/4 xfailed, PyAutoGalaxy 1357, PyAutoLens 832/1 xfailed · smoke 165/165 · independent Opus review CLEAN (6 claims basis-cited) · Heart RED under the recorded live-human development override (session 3e3dea38, AskUserQuestion 'L1 now under override (Recommended)', 2026-10-15; reasons as listed on PyAutoArray#626; permitted commit/push/PR-open, with merge by human /prm).
- campaign: PyAutoPulse#62 (https://github.com/PyAutoLabs/PyAutoPulse/issues/62), task `interferometer_large_mask_aris`. This came out of the 2026-10-15 CPU speed-up research on Aris's SPT2319-55 data.
- where-to-pick-up: (1) L2 draft `draft/feature/autoarray/direct_conv_symmetric_row_restriction.md` is unstarted and needs a quiet-core measurement first. (2) The existing Pulse task `interferometer_fixed_mapper_curvature_preload`. (3) The project-pointer draft `draft/docs/autolens_profiling/decision_matrix_note_gate_wording.md`.

## Original prompt

# Reuse one Cholesky factor of F+H for the reconstruction solve and the log det (numpy, non-positive-only path)

Type: feature
Target: PyAutoArray
Repos:
- PyAutoArray
Difficulty: small
Autonomy: safe
Priority: high
Status: formalised
Issued: 2026-10-15
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
