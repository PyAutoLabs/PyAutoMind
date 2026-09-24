# HST GPU residue phase 4 — reuse the certified solve's Cholesky for `log det(F + λH)` (0.89 ms, 2.8 %)

Type: research
Target: autolens_profiling
Repos:
- autolens_profiling
Themes:
- profiling
- pixelization
- hpc-gpu
- inversion
Difficulty: large
Autonomy: supervised
Priority: high
Status: issued — autolens_profiling#303, plan approved 2026-09-24 (Opus start_dev), routed to start_workspace
Epic: hst-gpu-non-solver-residue
Phase: 4
Consequence: judge
Witness: On the A100 (HST, Delaunay N=1500, fp64, border relocator on, LIBRARY certified solver
with PDIP fallback under scalar `jax.jit` — the phase-B adopted default) one matched table of the
whole fused `AnalysisImaging.log_likelihood_function`: the unmodified library control beside a
harness-injected `log_det_curvature_reg_matrix_term` that reads the log determinant off the
certified solve's final masked Cholesky plus a bounded Schur complement over the fixed set, giving
whole-call ms, the traced log-det stage row (reconciling to the wall within 5 %, zero unjoined),
compile time and the log-likelihood pin against the library at <= 1e-9 relative (fiducial + seeded
draws), and a written verdict (lever / no lever). Only if the lever clears its pre-registered
threshold at the pin, a PyAutoArray prompt filed via /intake naming the exact change.
Review-minutes: 20
Unattended: needs-slicing
Filed: 2026-09-24
Issued: 2026-09-24

## Original request

"continue to phase 4, I will do the follow ups in other chats" — after certified-solver phase B
(autolens_profiling#300, PR #302) closed; phase 4 is lever 3 of
`draft/research/autolens_profiling/hst_gpu_non_solver_residue_programme.md`.

## Why

Phase 1 (`results/notes/hst_gpu_residue_phase1_2026_09.md`, lever 3) traced a cuSOLVER Cholesky of
`F + λH` at `abstract.py` `log_det_curvature_reg_matrix_term` (0.89 ms) after the reconstruction has
already factorised the same system. The NumPy path already reuses the fnnls factor via the
block-determinant identity (`inversion_util.log_det_from_passive_cholesky_from`, ~5 vs ~40 ms,
<= 2e-12 nats); the JAX path does not. The library certified solver (PyAutoArray#567,
`autoarray/util/jax_active_set.py`) ends in `masked_solve`, one `(n, n)` Cholesky of `Q` with the
fixed rows/columns replaced by the identity — so `log det Q_FF` is free and `log det Q` needs only the
Schur complement over the fixed set Z (~15 of 1500 on HST Delaunay).

## Do

1. Harness (no library edit): in `fixed_light_trace.py` add a `--logdet-candidate` mode that, under the
   library certified solver, captures the final masked factor + fixed mask at trace time and rebinds
   `log_det_curvature_reg_matrix_term` to `2 Σ log diag L + log det S`, where the fixed set is gathered
   into a static `k_max` slot array (`jnp.nonzero(size=k_max)`), `Y = L⁻¹ Q[:, Z]` (triangular solve,
   k_max RHS), `S = Q_ZZ − YᵀY` padded with the identity; `|Z| > k_max` or a PDIP-fallback lane takes the
   dense Cholesky via `lax.cond` (scalar composition only — vmap policy stays library PDIP).
2. Pre-register before submitting: gate = <= 1e-9 relative vs the unmodified library log likelihood
   (fiducial + 8 seeded draws, same composition), plus reconciliation ±5 % and unjoined = 0; record the
   observed |Z| distribution and k_max overflow count. Lever threshold stated up front (the ceiling is
   0.89 ms, so the phase-3 1.5 ms bar is unreachable by construction).
3. RTX screen locally, then a small A100 array (control + candidate at k_max ∈ {32, 64}, Delaunay and
   rectangular). Verdict note in `results/notes/`; the A100 submit→harvest is a human resume point.

## Out of scope

`log det H` (0.89 ms, a different matrix, no shared factor); vmap composition; NumPy (already done);
mixed precision; any silent library edit.
