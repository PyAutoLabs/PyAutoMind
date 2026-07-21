## multistart_gradient_auto_convergence_phase_1

issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1406
completed: 2026-07-21
library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1407
workspace-pr: https://github.com/PyAutoLabs/autofit_workspace_test/pull/60

Phase 1 of 2 of auto-convergence (early-stopping) for the multi-start gradient searches (`af.MultiStartProdigy` / `MultiStartAdam` / `MultiStartADABelief` / `MultiStartLion`). Successor to the multi-start gradient v2 work (Fit#1398/#1400). Both PRs merged.

### What shipped
- **`MultiStartGradientConvergence` settings object** (`autofit/non_linear/search/mle/multi_start_gradient/convergence.py`) mirroring the `AutoCorrelationsSettings` precedent: `check_for_convergence=True`, plateau on the GLOBAL best figure-of-merit over a trailing window (`window=50`, `rtol=1e-4`, `atol=1e-3`, `min_steps=100`), `is_test_mode()` shrink hook, and a `check_if_converged(fom_history)` method. Exported as `af.MultiStartGradientConvergence`.
- **`convergence=` param** on `AbstractMultiStartGradient.__init__` (default → auto-convergence ON). The searches now stop early by default; `n_steps` is a HARD CEILING / max budget. `stop_reason` (`"converged"`|`"max_steps"`) persisted in `search_internal` for resume + the phase-2 results contract.
- **JAX validation** (`autofit_workspace_test/scripts/jax_assertions/multi_start_gradient_auto_convergence.py`): early-stop lands at the truth basin (converged step 158/300; 50.16/25.20/9.86) + a deterministic no-recompile guard (byte-identical value_and_grad HLO across independent builds → persistent compile cache hits on recall).

### Key traps / findings
- **The convergence check MUST run per-step, not only at the `iterations_per_full_update` boundary.** That param defaults to `None` → `iterations = n_steps` → the whole run is one chunk, so a boundary-only check would only fire at the very end and never stop early. The check runs every step (cheap NumPy plateau over the best-fom history) while checkpointing/`perform_update` stays at the boundary.
- **best_fom is monotonically non-increasing** (updated only on a new minimum), so the plateau test is `(fom[-window] - fom[-1]) <= atol + rtol*|fom[-window]|`. Non-finite window (no finite basin yet) → not converged.
- **Scope is PARAMETRIC ONLY (MGE/Sersic).** The check is skipped when `resurrect=True` (pixelized regime, whose best-fom climbs in breakthrough jumps a plateau check would false-stop) — pixelized behaviour is unchanged; it leans on the ceiling.
- **`check_if_converged` must return a Python `bool`, not `np.bool_`** — the unit tests use `is True`/`is False` identity (`np.True_ is True` is False).
- **JAX compile-cache-on-recall was already solved.** User asked to ensure recalled LH functions don't recompile; the persistent compilation cache is already default-ON via `autonerves/jax_wrapper.py` (`JAX_COMPILATION_CACHE_DIR`, compile-time arc PyAutoConf#128). Scope was **verify+guard**, not new machinery — and the search builds its `value_and_grad` identically on fresh vs resume paths (`search.py:198-208`, untouched), so the cache hit on resume holds **by construction**; the workspace guard is a regression net.

### Gate (--auto library ship)
tests 1521p/1s · smoke `searches/mle.py` early-stop fires · review self-CLEAN · Heart RED (2 pre-existing/unrelated reasons — `"PyAutoFit: 2 commit(s) behind origin"`, `"PyAutoLens: 1 uncommitted source change(s)"`) human-waived via AskUserQuestion. Both PRs human-merged.

### Follow-ups
- **Phase 2** (draft `draft/feature/autofit/multistart_gradient_auto_convergence_phase_2.md`): results contract — `converged`/`stop_reason` in `samples_info`, the fom_history convergence-trace artifact, and aggregator/samples_summary hardening for variable-length runs (guard the zero-weight/NaN diagnostic-row `IndexError`, Fit#275). Issue when picked up.

## Original prompt

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
