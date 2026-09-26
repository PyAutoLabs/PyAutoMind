## mge-nnls-grad-nan
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/573 (left open until Release Integrate confirms)
- completed: 2026-09-25
- library-pr: https://github.com/PyAutoLabs/PyAutoArray/pull/574
- corrective-red: "release validation FAILED (stage integrate)" — authorization https://github.com/PyAutoLabs/PyAutoArray/issues/573#issuecomment-5837171428; merge by human /prm ("and I authorize on red heart but I guess keep going to get it out of red.")

- Cause: #572's raw-forward PDIP stops at data_scaled_solver_tol, leaving s·z ~1e-10..2.5e-9 ≫ nnls_target_kappa=1e-11; the backward solve_relaxed_nnls on Q_pc pushed toward the boundary at z/s~1e13-14 and NaN'd under jit (4/16 keys eager, script's own key under jit).
- Fix: backward-only polish, ≤ RAW_BACKWARD_POLISH_MAX_ITER=10 warm-started tight PDIP iterations on (Q_pc,q_pc), kept only if converged with finite y and s,z>0; `solve_nnls(init=)`; `raw_forward_backward_status()`. Primal/forward HLO byte-identical.
- Rejected: kappa_eff = max(target_kappa, max(s·z)) — 6/48 SLaM NaN, 11/16 jit, relaxed "converged" with s<0 (a converged flag alone is not a guard).
- Evidence: full suite 1702 PASS; red-first fixture files/mge_grad_nan_systems.npz; jax_grad/mge.py 16/16 keys finite eager+jit, FD max rel 1.59e-6; runtime vs autolens_profiling no slowdown (value+grad −2.7%); #571 capture 48/48; independent review CLEAN; smoke 159 PASS.
- Trap: the 09-25 Integrate log lists jax 0.11.2 but a later step downgrades to 0.10.2 — JAX version was not the cause.
- Trap: worktree_create wrote an activate.sh whose PYTHONPATH pointed at the autolens-visualization-birth worktree; print autoarray.__file__ before trusting any ad-hoc run.
- Follow-up (not this task): autolens_workspace_test scripts/interferometer/jax_likelihood/mge.py vmap logL −45560751.36 vs pin −3152.65 under the smoke profile, identical on main 3de624b5.

## Original prompt

# fix: NaN JAX gradient on MGE (mapper-less) positive-only solves after #572

Type: bug
Target: @PyAutoArray
Autonomy: human-required
Issued: 2026-09-25
Issue: https://github.com/PyAutoLabs/PyAutoArray/issues/573

## Original request (verbatim, 2026-09-25)

> do it properly so go ahead with these, noting that in terms of run times we need to monitor any slowly against autolens_profiling - Proper fix, either of:
>   - run a few tight solver iterations before the gradient solve; or
>   - raise the gradient solve's target to at least the gap the forward solve leaves, so it never has to push toward the boundary.

## Context

Heart Release Integrate 2026-09-25 (PyAutoHeart run 36108062907) failed on
`autolens_workspace_test/scripts/imaging/jax_grad/mge.py`: "Gradient contains non-finite values".
Diagnosed to PyAutoArray #572 (merge 3de624b5): `autoarray/util/jax_nnls.py`
`_solve_nnls_raw_forward_with` — raw forward stops at `data_scaled_solver_tol`
(~5.5e-8) leaving s·z ~1e-10..2.5e-9; backward `solve_relaxed_nnls(Q_pc, ..., target_kappa=1e-11)`
must push toward the boundary at z/s ~1e13-14; jit while_loop overshoots → NaN at the
50-iteration cap. 4/16 perturbation keys NaN on main, 0/12 pre-#572. Forward likelihood unaffected.
This is the last failure blocking the release (autolens_workspace#577 fixed the other two).

Keep the #571 forward-convergence fix. Choose (a) polish vs (b) effective kappa on evidence;
surface the relaxed solve's converged flag; regression test sweeping perturbation points;
monitor runtime vs autolens_profiling before shipping.
