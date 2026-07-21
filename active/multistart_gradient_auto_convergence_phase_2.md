# Auto-convergence for the multi-start gradient searches — Phase 2: results-contract + aggregator hardening

Type: feature
Target: PyAutoFit
Repos:
- PyAutoFit
- autofit_workspace_test
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: formalised

Phase 2 of 2 — the results contract the prompt author flagged as "part 2, must
ship together" with the convergence loop
(`multistart_gradient_auto_convergence_phase_1.md`). **Do not issue this until
phase 1 nears shipping** (no bulk-issuing a prompt series). Depends on the
phase-1 `stop_reason` / `converged` locals and the `MultiStartGradientConvergence`
settings object landing first.

## Goal

Make the auto-convergence outcome inspectable and keep the aggregator robust to
the variable-length runs early stopping now produces.

## Scope

1. **samples_info:** add `converged: bool` + `stop_reason` (`'converged'` |
   `'max_steps'`) + the convergence settings to `samples_info`
   (`search.py:507`, `samples_via_internal_from`).
2. **Result artifacts:** surface the `fom_history` convergence trace in the
   standard result artifacts so users can visually verify the plateau (the loop
   already tracks `fom_history`).
3. **Aggregator / samples_summary coverage:** extend test coverage for
   variable-length runs (different `total_steps` across datasets). Guard the known
   zero-weight / NaN diagnostic-row aggregator `IndexError` edge — see
   PyAutoFit#275 (`_quick_fit` consolidation, samples-weight-threshold) — since
   the multi-start searches write zero-weight diagnostic rows for the non-best
   starts.

## Testing

- **Unit tests (numpy-only):** samples_info carries the new keys; aggregator
  handles variable-length runs + the zero-weight diagnostic-row edge without
  `IndexError`.
- **JAX validation (autofit_workspace_test):** aggregate a small set of MGE
  early-stopped runs and confirm the convergence trace + `converged`/`stop_reason`
  round-trip through the results database.

## Deliverable

Library PR (PyAutoFit) + aggregator test coverage. Workspace-facing artifact
example follows once the API lands.

<!-- phase 2 split from multistart_gradient_auto_convergence.md by start_dev on 2026-07-21 -->
