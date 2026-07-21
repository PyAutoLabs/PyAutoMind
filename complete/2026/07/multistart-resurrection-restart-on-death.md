## multistart-resurrection
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1399
- completed: 2026-07-20
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1400
- workspace-pr: https://github.com/PyAutoLabs/autofit_workspace_test/pull/59

Phase 2 of the multi-start gradient v2 promotion (autolens_workspace_developer#101). Both PRs merged 2026-07-20. Completes the two-phase promotion begun in [[project_lr_free_optimizer_experiment]] (Phase 1 = #1398).

**Shipped:**
- `resurrect: bool = False` knob on `af.AbstractMultiStartGradient` (inherited by all `MultiStart*`). When on, dead (non-finite-objective) starts are redrawn each step (params from the start band + per-start optimizer state reinitialised) and merged into the alive population via a `jnp.where` mask over the vmapped state pytree — `_reinit_dead_starts`.
- `n_resurrections` diagnostic through `search_internal` (resume-safe) + `samples_info`.
- `autofit_workspace_test/scripts/searches/MultiStartResurrect.py` — on/off equivalence JAX validation (not in smoke_tests.txt; full-sweep precedent).

**Validation:** PyAutoFit numpy unit suite 9-pass · JAX: `_reinit_dead_starts` redraws only dead rows (params + state), alive rows byte-identical · `resurrect` on/off recover the identical best basin on the 1D Gaussian even when resurrection fires incidentally (n_resurrections=1 from a `sigma≈0` broad start).

**Traps / notes:**
- Default OFF is load-bearing: resurrection is only needed on inversion-heavy (pixelized) landscapes with broad non-finite walls; on the parametric MGE cell `apply_if_finite` alone suffices and behaviour must stay unchanged.
- Redraw into an `np.array` copy — `np.asarray` of a jax array is READ-ONLY. Mask size = `params.shape[0]` (broad-start collection may yield < `n_starts`).
- Ordering in the loop: capture best_* from the pre-redraw alive population, THEN resurrect, THEN step_update with the OLD grads — a dead start's old non-finite grad is zeroed for one step by apply_if_finite on its fresh state, so a redrawn start waits one step (matches the searches_minimal reference).
- Full pixelized validation is A100-only (ref job 330598: adam −51201 → +1718 over 3000 steps); the library port mirrors `reinit_starts` exactly. Even so Nautilus still wins the pix cell decisively — this makes gradient MAP VIABLE there, not competitive.
- Shipped past the same pre-existing/unrelated Heart RED as Phase 1 (PyAutoLens dirty, known 632p/10f ws-validation baseline, hygiene/release-stale) with human authorization; merge human.

See [[project_multi_start_gradient_search_promotion]], [[project_lr_free_optimizer_experiment]].

## Original prompt

# Multi-start gradient search v2 — restart-on-death (resurrection) layer

Type: feature
Target: autofit
Repos:
- @PyAutoFit
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: draft

**Phase 2 of the multi-start gradient v2 promotion (#101).** Depends on Phase 1
(`multistart_contrib_and_vmapped_state.md` — per-start `jax.vmap`ed optimizer
state + `optax.contrib` + `MultiStartProdigy` + `apply_if_finite` guard) being
merged first: resurrection reinitialises a dead start's *per-start* optimizer
state, which only exists after Phase 1's stacked→vmapped refactor.

Promote **restart-on-death (resurrection)** into
`af.AbstractMultiStartGradient` (`autofit/non_linear/search/mle/
multi_start_gradient/search.py`):

On likelihoods with hard non-finite regions (pixelized sources), every gradient
trajectory walks into a non-finite wall within ~25–50 steps. `apply_if_finite`
alone latches the start *at* the cliff edge (dead), and the current unguarded
loop silently NaN-poisons — this is #100's -39888 "0/16" result. Each step,
redraw any start whose objective went non-finite (params drawn fresh from the
start band + its vmapped optimizer state reinitialised), leaving alive starts
untouched. Proven to keep the population alive indefinitely and convert the
pixelized landscape from unsearchable to searchable (adam -51201 → +1718 over
3000 steps, job 330598).

Reference implementation: `autolens_workspace_developer/searches_minimal/
pix_lr_free.py` (`PIX_RESURRECT`, `reinit_starts`, the per-start death
diagnostics). Design points to carry:
- Gate behind a search knob (default off) so the existing MGE-cell behaviour and
  results are unchanged — resurrection is only load-bearing on inversion-heavy
  landscapes.
- `reinit_starts` merges fresh params/state into the alive population via a
  boolean mask (`jnp.where` over the vmapped state pytree); `np.asarray` of a
  JAX array is read-only, so redraw into an `np.array` copy.
- Optionally surface per-start death diagnostics (last finite step / params) in
  `search_internal` for downstream inspection.

Evidence + verdict: `searches_minimal/lr_free_findings.md` (#101, Phase 2).
Note the honest caveat for the docstring/PR: even with resurrection, Nautilus
still wins the pixelized cell decisively (+17419 in ~22 min warm vs +1718 after
2.7 h resurrected Adam); this layer makes gradient MAP *viable* on such
landscapes, not competitive there. Unit tests numpy-only per
[[feedback_no_jax_in_unit_tests]]; JAX/A100 validation in
autofit_workspace_test per the established split.
