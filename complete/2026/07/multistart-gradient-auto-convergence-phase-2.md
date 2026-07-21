## multistart_gradient_auto_convergence_phase_2

issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1409
completed: 2026-07-21
library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1410
workspace-pr: https://github.com/PyAutoLabs/autofit_workspace_test/pull/61

Phase 2 of 2 — the results contract for multi-start gradient auto-convergence. **Completes the 2-phase arc** (phase 1: `complete/2026/07/multistart-gradient-auto-convergence-phase-1.md`). Both PRs merged.

### What shipped
- **samples_info** now carries `converged` / `stop_reason` / `convergence` (settings) / `fom_history` (trace, plain floats for JSON round-trip) — the auto-convergence outcome is inspectable downstream and through the results DB.
- **`figure_of_merit_vs_iteration`** MLE plotter (`mle_plotters.py`) draws the global-best FoM trace so the plateau is visible; wired into `abstract_mle.py` `plot_results` behind a default-on, `KeyError`-tolerant gate; no-op for LBFGS/Drawer (no `fom_history`).
- **Bug fix:** `Samples.max_log_likelihood_index` / `max_log_posterior_index` `np.argmax`→`np.nanargmax`.
- **Aggregator regression tests** (variable-length + zero-weight/NaN rows) + JAX **results-DB round-trip** validation (`autofit_workspace_test`).

### Key findings / traps
- **`np.argmax` selects NaN.** `np.argmax([2.5, nan, nan]) == 1` — so `max_log_likelihood_index`/`max_log_posterior_index` were returning the multi-start's zero-weight **NaN diagnostic rows** (inconsistent with `max_log_likelihood_sample`, which uses a `>` loop and was correct — that's why `max_log_likelihood()` itself was fine). Fix = `nanargmax` with an all-NaN→index-0 guard. Reproduced before fixing (house rule); the Samples-level `max_log_likelihood`/`summary` path had NO IndexError (Fit#275 guard at `search_output.py:320` covers empty loads).
- **Workspace-config trap.** A new `should_plot("figure_of_merit_vs_iteration")` bracket-lookup would `KeyError` on every MLE fit in any workspace whose `plots_search.yaml` shadows the `mle` section without the new key. Gate is `try/except KeyError → default True` so it never crashes older workspaces; packaged `plots_search.yaml` has the key.
- **fom_history** stored as plain `float` list (not `np.float64`) so `samples_info.json` serialises cleanly.

### Gate (--auto library ship)
tests 1525p/1s · smoke `searches/mle.py` · review self-CLEAN (the shared-`samples.py` nanargmax fix flagged as in-scope for the NaN edge) · Heart RED (2 pre-existing/unrelated — `"PyAutoFit: 2 commit(s) behind origin"`, `"PyAutoLens: 1 uncommitted source change(s)"`) human-waived via AskUserQuestion. Both PRs human-merged.

### Arc complete
The 2-phase multi-start gradient auto-convergence work is done: default-on early-stopping (phase 1) + inspectable results contract (phase 2). No further phases planned.

## Original prompt

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
