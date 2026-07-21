# Auto-convergence (early stopping) for the multi-start gradient searches — Phase 1: convergence loop + settings

Type: feature
Target: PyAutoFit
Repos:
- PyAutoFit
- autofit_workspace_test
Difficulty: large
Autonomy: supervised
Priority: normal
Status: formalised

Phase 1 of 2 (see `multistart_gradient_auto_convergence_phase_2.md` for the
results-contract + aggregator-hardening follow-up; issue phase 2 only as this one
nears shipping — no bulk-issuing). Successor to the multi-start gradient v2 work
(contrib rules + resurrection, Fit#1398/#1400).

## Goal

Give `af.MultiStartProdigy / MultiStartAdam / MultiStartADABelief / MultiStartLion`
a first-class **auto-convergence (early-stopping)** mode (default on) so users no
longer hand-tune `n_steps`. Today `AbstractMultiStartGradient` runs a FIXED
`n_steps` budget with NO convergence criterion. `n_steps` stays a HARD
CEILING / max budget (never runs forever).

## Scope

- **In scope:** PARAMETRIC SOURCES ONLY (MGE / Sersic — the smooth, well-behaved
  regime where a global-best plateau genuinely means converged).
- **Out of scope:** pixelized. Its best-fom climbs in long plateaus punctuated by
  breakthrough jumps (resurrection churn), so plateau detection false-stops there.
  So when `resurrect=True` the auto behavior stays conservative / **off** and leans
  on the ceiling. (The real pixelized goal is smoothing the LIKELIHOOD, not
  band-aiding the optimizer — tracked separately.)

## Design (mirror the `AutoCorrelationsSettings` precedent)

Emcee/Zeus terminate early via `AutoCorrelationsSettings`
(`autofit/non_linear/search/mcmc/auto_correlations.py`:
`check_for_convergence=True`, a companion `check_if_converged`, and an
`is_test_mode()` shrink hook). Mirror that shape:

1. **New file** `autofit/non_linear/search/mle/multi_start_gradient/convergence.py`
   — `MultiStartGradientConvergence(check_for_convergence=True, window, rtol, atol,
   min_steps)` + a `check_if_converged(fom_history)` method. Plateau on the GLOBAL
   best figure-of-merit over the trailing window:
   `|best_fom[-1] - best_fom[-window]| <= atol + rtol * |best_fom[-window]|`,
   only once `len(fom_history) >= max(min_steps, window)`. `is_test_mode()`
   shrinks `window`/`min_steps` so tests terminate fast.
2. **`search.py` `__init__`** (`AbstractMultiStartGradient`, ~line 28): add a
   `convergence: Optional[MultiStartGradientConvergence] = None` param; default
   constructs the settings (auto ON). Store on self. Export
   `MultiStartGradientConvergence` via `autofit/__init__.py`.
3. **`search.py` loop** (~line 302–321, at the `iterations_per_full_update`
   boundary, right after `fom_history` extends + `save_search_internal`, before
   `perform_update`): if convergence enabled AND NOT `resurrect`, break when
   `check_if_converged` passes. `n_steps` remains the hard ceiling. Carry a
   `stop_reason` local (`'converged'` | `'max_steps'`) so `during_analysis` and
   the final state reflect the early stop. (`stop_reason` / `converged` surfacing
   into `samples_info` + result artifacts is phase 2 — this phase only needs the
   local so the loop terminates correctly.)
4. **Config:** add convergence defaults to the packaged `autofit/config/` so
   downstream workspaces inherit them.

## JAX compile-cache guarantee (recall must NOT recompile)

Requirement: when a likelihood function is recalled (resume / restart), the
JIT/grad-compiled value_and_grad must be reused, not recompiled.

The stack ALREADY ships the durable lever: `autonerves/jax_wrapper.py` sets
`JAX_COMPILATION_CACHE_DIR` (→ `~/.cache/pyauto_jax`) +
`JAX_PERSISTENT_CACHE_MIN_COMPILE_TIME_SECS=1` for every user (compile-time arc,
PyAutoConf#128). XLA serializes each compiled executable (jit AND grad) to disk
keyed on its HLO hash, so a fresh process loads the binary instead of recompiling.
Do NOT build redundant caching machinery (prefer the lean existing lever).

Phase-1 work is to **verify + guard**, not to build:

- In `_fit` (`search.py:198–208`) `batched_value_and_grad` is built once per fit
  and reused across all loop iterations — confirm no per-iteration re-tracing.
- On resume (`search.py:216–253`) the closure is rebuilt from a fresh
  `fitness.call`; the on-disk cache only HITS if the HLO is byte-identical across
  processes. Auto-convergence introduces variable-length/resume paths — prove the
  resumed value_and_grad HLO is stable so the persistent cache hits (no recompile
  on recall). If early-stop perturbs traced shapes and busts the cache, keep the
  traced computation shape-stable (the actual work, if any).
- Add a JAX-validation script in **autofit_workspace_test** that runs an MGE
  multi-start fit to early-stop, resumes in a fresh process, and asserts the
  resume does NOT recompile (cache HIT / near-zero compile time).

## Testing

- **Unit tests (numpy-only, PyAutoFit):** plateau boundaries — converges on a flat
  history, does NOT on a climbing history, respects `min_steps`, disabled when
  `resurrect=True`, `n_steps` ceiling still honoured. NEVER use JAX in library
  unit tests.
- **JAX validation (autofit_workspace_test):** end-to-end MGE early-stop +
  resume-no-recompile check (above). Cluster-scale scripts stay out of the curated
  smoke subset.

## Deliverable

Library PR (PyAutoFit) shipped first so the workspace can consume the API-change
summary, then the JAX-validation follow-up in autofit_workspace_test.

<!-- phase 1 split from multistart_gradient_auto_convergence.md by start_dev on 2026-07-21 -->
