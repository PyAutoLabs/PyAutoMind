## multistart-contrib-vmapped-state
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1397
- completed: 2026-07-20
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1398
- workspace-pr: https://github.com/PyAutoLabs/autofit_workspace_test/pull/58

Phase 1 of the multi-start gradient v2 promotion (autolens_workspace_developer#101). Both PRs merged 2026-07-20.

**Shipped:**
- `optax` → `optax.contrib` rule resolution in `af.AbstractMultiStartGradient` (unlocks prodigy et al.).
- Optimizer state moved from a single stacked `(n_starts, ndim)` init to per-start `jax.vmap(optimizer.init)` + a vmapped update step — so learning-rate-free rules' global scalar estimates (Prodigy `d`, DoG `max_dist`, Mechanic scale, MoMo Polyak) stay independent per start. Elementwise Adam family numerically unchanged.
- `optax.apply_if_finite` in-step guard with a new `max_consecutive_nan=8` knob; `value=`-forwarding branch for MoMo-family rules.
- `af.MultiStartProdigy` (learning-rate-free) added + exported; `optax` pin → `>=0.2.5`.
- `autofit_workspace_test/scripts/searches/MultiStartProdigy.py` JAX validation (not added to smoke_tests.txt — follows the MultiStartAdam.py full-sweep precedent).

**Validation:** PyAutoFit numpy unit suite 7-pass · JAX end-to-end Adam/Prodigy/Prodigy(batch=4) recover the 1D Gaussian truth basin, Adam == Prodigy optimum with NO learning rate (the headline #101 result) · vmapped `ApplyIfFiniteState` opt_state dill round-trips exactly and resumes.

**Traps / notes:**
- `needs_value` (momo consumes the loss) must be detected on the **unwrapped** rule — `apply_if_finite` hides `value` behind `**extra_args`. prodigy/adam have `extra_args` but no `value`.
- The resume path stores the richer vmapped `ApplyIfFiniteState` pytree; dill (`save/load_search_internal`) preserves the NamedTuple structure so `optax.tree_utils.tree_get` round-trips — verified directly.
- Prodigy is learning-rate-free via `_default_learning_rate = None` → the rule is built with no lr (its own default), and `learning_rate` stays `None` through dict round-trip.
- Shipped past a pre-existing/unrelated Heart RED (PyAutoLens dirty checkout, the known 632p/10f ws-validation baseline predating the change, hygiene/release-staleness) with explicit human authorization; merge was human. See [[project_lr_free_optimizer_experiment]], [[project_multi_start_gradient_search_promotion]].

**Follow-up:** Phase 2 (restart-on-death resurrection) — filed draft, depends on this PR's per-start vmapped state; being issued next.

## Original prompt

# Multi-start gradient search v2 — optax.contrib rules + per-start vmapped state

Type: feature
Target: autofit
Repos:
- @PyAutoFit
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: draft

**Phase 1 of the multi-start gradient v2 promotion (#101).** The restart-on-death
(resurrection) recovery layer is Phase 2
(`multistart_resurrection_restart_on_death.md`), which builds on the per-start
vmapped state introduced here.

Promote the optax.contrib / learning-rate-free rule support from
autolens_workspace_developer#101 into `af.AbstractMultiStartGradient`
(`autofit/non_linear/search/mle/multi_start_gradient/search.py`):

1. **optax.contrib rule resolution.** The current
   `getattr(optax, self.optax_method)` misses `optax.contrib` (prodigy et al.).
   Resolve the rule from `optax` then fall back to `optax.contrib`.
2. **Per-start vmapped optimizer state.** The current stacked-`(n_starts, ndim)`
   state init COUPLES the lr-free rules' *global scalar* estimates (prodigy /
   dadapt `d`, DoG `max_dist`, mechanic scale, momo Polyak) across starts.
   Init/update the optimizer per start via `jax.vmap` (elementwise rules — the
   existing Adam/ADABelief/Lion — are numerically unaffected; the #101 benchmark
   showed no per-eval cost). This is the load-bearing refactor Phase 2 also
   depends on.
3. **`optax.apply_if_finite` in-step guard.** Wrap the rule so a single
   non-finite step zeroes the update instead of NaN-poisoning (optax >= 0.2.5
   forwards momo's `value=` kwarg). Bump the `optax` pin in `pyproject.toml` to
   `optax>=0.2.5`. (Resurrection in Phase 2 is the recovery layer *on top of*
   this guard, which alone only latches at the cliff edge.)
4. **`af.MultiStartProdigy`.** Add the concrete search — on the MGE cell prodigy
   is bit-identical to hand-tuned adam (+31787.84) with NO learning rate, the
   headline #101 result. Export it from `autofit/__init__.py` alongside the
   existing `MultiStart*` classes.

Wiring reference: `autolens_workspace_developer/searches_minimal/pix_lr_free.py`
(the per-start `jax.vmap(opt.init)` / vmapped `update`, the `needs_value` branch
for momo's `value=`). Evidence: `searches_minimal/lr_free_findings.md`
(#101, Phase 1 — MGE cell table).

Unit tests numpy-only per [[feedback_no_jax_in_unit_tests]] (config knobs, rule
resolution incl. contrib, dict round-trip, Prodigy defaults); JAX validation
(prodigy == adam on the MGE cell, vmapped-state independence) in
autofit_workspace_test per the established split. Existing Adam/ADABelief/Lion
results must be unchanged.
