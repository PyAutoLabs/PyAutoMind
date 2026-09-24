## hst-gpu-residue-p4
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/303
- completed: 2026-09-24
- workspace-pr: https://github.com/PyAutoLabs/autolens_profiling/pull/306 (merged `1fae64e`, head `83e27e1`)
- epic: hst-gpu-non-solver-residue (phase 4; campaign map `draft/research/autolens_profiling/hst_gpu_non_solver_residue_programme.md`)
- summary: |
    Phase 4 tested reusing the library certified solve's masked Cholesky
    factor for log det(F + λH): block-determinant identity with a
    k_max-slot Schur complement over the fixed (+ edge) set and a dense
    `lax.cond` overflow, as a harness-only scoped rebind
    (`scripts/misc/likelihood_breakdown/logdet_reuse_injection.py`) in
    `fixed_light_trace.py`, library certified solver via `al.Settings`
    under scalar jit (phase B policy). New A100 submit
    `hpc/batch_gpu/submit_breakdown_imaging_fixed_light_logdet_reuse_a100_hst_fp64`,
    16 result rows (A100 + RTX 2060 screen), verdict note
    `results/notes/hst_gpu_residue_phase4_logdet_2026_09.md` (+ job350651
    provenance JSON), campaign status note updated.
- verdict: NO LEVER. No candidate reached the pre-registered >= 0.5 ms
  saving on both jit_profile and interleaved bases.
- evidence: RAL A100 fp64 array 350651, 8/8 `COMPLETED 0:0`; gate 8/8 PASS
  at 1e-9 (72/72 pins) vs the unmodified library route. In-task
  interleaved savings: Delaunay N=1500 −0.27 / −0.31 / −0.45 ms
  (k32/k64/k256); rectangular +0.09 / +0.09 (dense overflow) / −0.38 ms.
  The triangular solve against the 1500x1500 factor costs 0.97-1.05 ms at
  every k >= 32, more than the 0.90 ms dense Cholesky; fixed-set sizes
  (draws |Z| 51-943) also defeat small k. Library mains: PyAutoArray
  `7fa8d271`, profiling source `a621160`.
- merge: PR #306 merged by the human; pushed under the human's
  development-only Heart-RED override ("yes i authorize", 2026-09-24);
  Heart remained RED for release.
- not-shipped: none — the PyAutoArray prompt was conditional on a lever
  and is correctly not filed.
- follow-ups: the campaign map's fp64 levers are exhausted. Remaining,
  outside this map: the human fp32-cube precision decision (phase 3), the
  cond-free batched fallback
  (`draft/feature/autofit/certified_solver_cond_free_batched_fallback.md`),
  and the qhull callback / batching work filed elsewhere.

## Original prompt

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
