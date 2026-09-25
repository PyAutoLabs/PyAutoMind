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
