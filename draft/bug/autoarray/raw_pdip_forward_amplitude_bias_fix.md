# Linear-solver programme phase 2: fix the raw-forward PDIP amplitude bias in PyAutoArray

Type: bug
Target: PyAutoArray
Repos:
- PyAutoArray
- euclid_strong_lens_modeling_pipeline
- autolens_profiling
Difficulty: medium
Autonomy: supervised
Priority: high
Status: formalised
Filed: 2026-09-30
Blocked-by: none (the PyAutoArray claim of `sparse-data-none-guard` cleared 2026-09-30 — `complete/2026/09/sparse-data-none-guard.md`, PyAutoArray#591 merged)
Witness: a PyAutoArray regression test loads the phase-1 corpus npz (copied from autolens_profiling `results/lens/solver/corpus/` as a fixture beside `test_autoarray/inversion/inversion/files/mge_slam_nnls_systems.npz`) and asserts, per system, converged AND amplitude agreement with fnnls (amp_rel_max ≤ 1e-3, source flux_rel ≤ 1e-4) — an amplitude assertion, not logL — red on unfixed main; plus euclid `tests/test_compute_latent_variable.py::test_latent_euclid_variables_traces_under_jax_jit` passes on library main with no config override.
Review-minutes: 3
Consequence: glance
Unattended: needs-slicing

Epic `linear-solver-programme`, phase 2. Contract: `complete/2026/09/linear-solver-accuracy-study.md` (phase-1 record with the original programme prompt folded in; the phase-1 verdict blocker is satisfied — autolens_profiling#355 merged 2026-09-30).

## Symptom

Raw PDIP (PyAutoArray#572, `nnls_preconditioning_no_mapper: raw`, the released mapper-less
default) stops on the objective (gap 4.7e-6 vs fnnls) with amplitudes 4.3 % off fnnls, so
euclid `total_source_flux` traces to 3.511 under `jax.jit` vs 3.320 eager. The euclid latent
test has been red since 2026-09-25. logL cannot see it (Δχ² ~1e-5); amplitude latents shift ~6 %.

## Fix

Candidate: phase 1 verdict (autolens_profiling#355, `complete/2026/09/linear-solver-accuracy-study.md`): **no candidate passes the pre-registered rule** — raw PDIP reports converged on 81/81 (KKT ~3e-14) yet leaves 11.5 % of the reference amplitude on euclid columns inactive in the reference (total_source_flux +5.76 %); jacobi diverges on 29/81. Post-hoc, each of these turns the euclid latent test green: forward polish (+7.5e-5), tol 1e-5 (+5.1e-4), jaxnnls tol with cap > 50 (-3e-8); caps ≤ 16 are unsafe. The binding constraint is the stopping test, not the iteration budget. Choose among these on the post-hoc evidence and gate on inactive-column flux, not logL/KKT.

Implement exactly the candidate the phase-1 pre-registered rule admits (converged 100 %, 48/48
SLaM incl.; worst amp_rel_max ≤ 1e-3; worst source flux_rel ≤ 1e-4; KKT ≤ 10× pdip_jacobi's;
lowest median iterations). The three plausible shapes:

1. A tighter data-scaled tolerance constant in `data_scaled_solver_tol`
   (`autoarray/util/jax_nnls.py`).
2. Return the PyAutoArray#573 polished iterate (≤ 10 warm-started Jacobi iterations) as the
   forward value in `_raw_forward_backward_point` / `_solve_nnls_raw_forward_with`. The
   custom_vjp forward must return the same value the primal (`solve_nnls_primal_raw_forward`)
   returns, or jit/grad and eager diverge — polish both or neither.
3. A KKT / solution-based stop instead of the objective-gap stop.

Also touch the `inversion_util.py` raw branch if the candidate needs it, and update the
`nnls_preconditioning_no_mapper` comment in `general.yaml` to describe the new behaviour.

## Constraint

The 48/48 SLaM source_lp[1] points must stay converged (#571); the existing
`mge_slam_nnls_systems.npz` test must stay green.

## Rejected

- Loosening `JIT_VS_EAGER_REL` in the euclid test.
- A pipeline config stopgap to `jacobi` (reintroduces #571).

## Downstream

- workspace_test mapper-less likelihood pins: re-pin if the forward value moves.
- autolens_profiling: re-run `scripts/lens/solver/accuracy.py` post-fix and append the row to
  `results/notes/linear_solver_accuracy_2026_09.md` (+ campaign page
  `wiki/campaigns/linear_solver_accuracy.md`).

## Ownership and order

PyAutoArray owns the solver; euclid_strong_lens_modeling_pipeline owns the witness test (no edit
expected there); autolens_profiling is the corpus fixture source. Library-first: ship PyAutoArray,
then re-verify the euclid test on library main.
