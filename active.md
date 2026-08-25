# Active Tasks

## transformed-message-factor-gradient-unpack
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1501 (issued 2026-08-19)
- issued: 2026-08-19
- prompt: active/16_transformed_message_factor_gradient_unpack.md
- status: HOLD — do not start dev. Fix-or-delete hangs off the PyAutoFit#1498 logpdf-contract
  decision (parked #1500 design bundle); dead code (zero production callers), crashes on first
  call if ever exercised.
- external: community PR https://github.com/PyAutoLabs/PyAutoFit/pull/1502 (@trexfr-ops) targets
  this exact unpack — review via /community before any local work; the #1498 adjudication decides
  whether the method should exist at all.
- registered: 2026-08-19 by the wake_up session — the issuing session (claude/autofit-priors-messages-audit-ylvenv)
  filed the prompt + issue but not this entry, tripping Lifecycle Drift on main.
- repos-none-claimed: this entry claims NO repos — one line deliberately, not 2-space bullets.

## gradient-eager-jit-divergence-py313
- issue: https://github.com/PyAutoLabs/autolens_workspace_test/issues/279 (issued 2026-08-25)
- issued: 2026-08-25
- prompt: active/gradient_eager_jit_divergence_py313.md
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/gradient-eager-jit-divergence-py313
- repos:
- summary: |
    Variant B of scripts/interferometer/jax_grad/gradient.py (RectangularRTUAdaptDensity +
    reg.Adapt, sparse-operator path) trips assert_eager_jit_consistent on the 3.13 leg only,
    deterministically 5/5. The prompt's investigation refutes both pure_callback
    constant-folding and a jax/jaxlib version delta; the mechanism is a discrete branch flip
    in the positive-only NNLS PDIP solve, whose data-dependent lax.while_loop trips one
    iteration apart under eager vs fused-XLA evaluation. Plan: instrument pdip_iter/converged
    eager-vs-jit, falsify the "3.13" attribution against runner hardware, then pin solver
    policy via al.Settings(nnls_solver_tol=, nnls_max_iter=) scoped to Variant B, leaving
    assert_eager_jit_consistent at rtol=1e-10 untouched at all 11 call sites, and remove the
    NEEDS_FIX park at config/build/no_run.yaml:42.
- next: /start_workspace — but implementation needs an environment that can RUN the stack.
  This session (claude/gradient-eager-jit-divergence-py313-5dylgx, web-github) has no PyAuto
  install and no JAX, and the failure only manifests on a CI 3.13 leg; every verification
  step in the plan is a measurement. Plan + issue are complete and were derived by reading
  live sources, not by running them.
- prior-art: complete/2026/08/positive-solver-divergence-diagnosis.md (autolens_profiling#113)
  — same PDIP solver, same one-ULP-boundary class; its method was a bounded sweep of the
  public nnls_solver_tol / nnls_max_iter controls, which is the route step 3 takes.
