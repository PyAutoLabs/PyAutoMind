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
