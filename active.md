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
- status-note: 2026-08-26 — BLOCKED on a PyAutoArray fix; root-caused, do not start
  workspace dev yet. A runnable stack was built in-session (both Python legs,
  source-installed libraries at the retime run's exact versions) and the failure
  reproduced bit-for-bit. Findings posted to autolens_workspace_test#279.
- refuted: the prompt's own UPDATE 2026-08-24 diagnosis, on three counts. (1) NOT
  3.13-only — 3.12 fails identically on the same host, so the CI split was runner
  hardware, not CPython. (2) NOT a PDIP branch flip — pdip_iter is identical eager
  vs jit, and the gap is bit-identical across 5 solver policies. (3) So pinning
  nnls_solver_tol/nnls_max_iter cannot work; that fix direction is dead.
- root-cause: a discrete bilinear cell-assignment flip in PyAutoArray's rectangular
  mapper (interpolator/rectangular.py:452). transform() ends in clip(F_q, 0, 1),
  so saturated points land on exactly-integer indices where ix_up = ceil(g)
  collapses onto ix_down; 1 ULP in the traced grid then jumps a point's weight a
  whole mesh row. Underneath it the row weights are mirrored (ix_up carries
  1 - t_row instead of t_row) — proven by a linear-reproduction test the current
  code fails by ~a full cell in the row axis while the column axis is exact.
- spawned: draft/bug/autoarray/rectangular_mapper_bilinear_row_weights.md — the real
  fix, human-required. Validated locally (gap exactly 0.0, this script green on both
  legs at 83s/86s vs the 300s cap, pytest test_autoarray/ 1220 passed) but it changes
  reconstructions library-wide (+1222.6 logL on imaging/jax_likelihood/rectangular.py,
  a better fit) and 16 workspace scripts' hardcoded EXPECTED_LOG_* constants need
  regenerating, autogalaxy_workspace_test too.
- next: hold. The NEEDS_FIX park in config/build/no_run.yaml STAYS until the library
  fix lands; this repo's eventual change is only constant regeneration + un-parking,
  behind the library-first gate.
- prior-art: complete/2026/08/positive-solver-divergence-diagnosis.md (autolens_profiling#113)
  — same PDIP solver, same one-ULP-boundary class; its method was a bounded sweep of the
  public nnls_solver_tol / nnls_max_iter controls, which is the route step 3 takes.
