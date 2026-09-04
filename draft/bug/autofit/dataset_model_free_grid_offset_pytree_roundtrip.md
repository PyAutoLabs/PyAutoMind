# DatasetModel with a free grid_offset cannot round-trip autofit.jax.register_model

Type: bug
Target: autofit
Repos:
- PyAutoFit
Themes:
- jax
Difficulty: small
Autonomy: safe
Priority: normal
Status: draft
Filed: 2026-09-03

## Symptom

A bare `af.Model(al.DatasetModel)` cannot be round-tripped through
`jax.tree_util.tree_flatten` / `tree_unflatten` after
`autofit.jax.register_model`: flattening raises

    ValueError: not enough values to unpack (expected 2, got 0)
    (autofit/mapper/prior_model/prior_model.py:331, Model.tree_flatten)

Corrected 2026-09-04 while triaging autolens_workspace#524. Three facts replace
the original description:

1. The failure is a `ValueError` in `Model.tree_flatten`, not a `TypeError` in
   `Prior.tree_unflatten` (that line is never reached).
2. It is not caused by a free `grid_offset`: the same model with *no* free
   parameters fails identically. The trigger is a `Model` with zero *direct*
   priors — the `grid_offset` priors live under a `TuplePrior`, which
   `direct_prior_tuples` excludes.
3. Related silent defect: with `grid_offset_0/1` **and** `background_sky_level`
   free (prior_count 3), the round-trip succeeds but the rebuilt model has
   prior_count 1 — `Model.tree_flatten` drops `TuplePrior` children.

None of this reaches a search: `Fitness` (`autofit/non_linear/fitness.py:245`)
captures the model as a closure constant and only traces the parameter vector.
A free `grid_offset` inside a `FactorGraphModel(use_jax=True)` compiles and runs
under the vmapped Nautilus fitness (verified on the corrected
`multi_dataset/start_here.py`). It blocks nothing today.

Originally found while building the free-`grid_offset` control for
`gaussian-precompute-p2` (record `complete/2026/09/gaussian-precompute-p2.md`).

## Fix

Make `Model.tree_flatten` handle zero direct priors and include `TuplePrior`
children (so `tree_unflatten` rebuilds them), and add a round-trip test over a
`DatasetModel` with (a) nothing free, (b) a free `grid_offset`, (c) a free
`grid_offset` plus `background_sky_level`, asserting `prior_count` survives.
