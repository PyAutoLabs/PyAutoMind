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
