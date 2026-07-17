# Multi-start gradient search v2 — restart-on-death + optax.contrib rules

Type: feature
Target: autofit
Repos:
- @PyAutoFit
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: draft

Promote the two experiment-proven upgrades from autolens_workspace_developer#101
into `af.AbstractMultiStartGradient` (autofit/non_linear/search/mle/
multi_start_gradient/search.py):

1. **Restart-on-death (resurrection).** On likelihoods with non-finite regions
   (pixelized sources), every trajectory dies within ~50 steps and the current
   implementation silently latches/NaN-poisons (#100's -39888 "0/16" result).
   Redraw a dead start (params + its optimizer state) from the start band each
   step — proven to keep the population alive indefinitely and to convert the
   pixelized landscape from unsearchable to searchable (adam -51201 -> +1718
   over 3000 steps, job 330598). Reference implementation:
   `searches_minimal/pix_lr_free.py` (`PIX_RESURRECT`, `reinit_starts`).
2. **optax.contrib rule support with per-start vmapped state.** The current
   `getattr(optax, self.optax_method)` misses `optax.contrib` (prodigy et al.),
   and the stacked-(n_starts, ndim) state init COUPLES the lr-free rules'
   global scalar estimates (prodigy/dadapt d, DoG max_dist, mechanic scale,
   momo Polyak) across starts. Promotion must `jax.vmap` optimizer init/update
   per start (elementwise rules unaffected; benchmark showed no per-eval cost).
   Add `af.MultiStartProdigy` — on the MGE cell prodigy is bit-identical to
   hand-tuned adam (+31787.84) with NO learning rate, the headline #101 result.
   `optax.apply_if_finite` (optax>=0.2.5 forwards momo's value= kwarg) as the
   in-step guard, with resurrection as the recovery layer.

Evidence + wiring details: `searches_minimal/lr_free_findings.md` (#101).
Unit tests numpy-only per [[feedback_no_jax_in_unit_tests]]; JAX validation in
autofit_workspace_test per the established split.
