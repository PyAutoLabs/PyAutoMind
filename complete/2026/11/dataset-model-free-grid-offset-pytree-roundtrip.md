## Outcome

Shipped in PyAutoFit#1779 (merged `17b87edb`, 2026-11-18).

- `Model.tree_flatten` (`autofit/mapper/prior_model/prior_model.py`) copes with zero direct
  priors and carries direct `TuplePrior` attributes as pytree children.
- `TuplePrior` (`autofit/mapper/prior/tuple_prior.py`) has its own `tree_flatten` /
  `tree_unflatten` (free priors as children; names and fixed values in aux) and is registered
  in `enable_pytrees` (`autofit/jax/pytrees.py`).
- New `test_autofit/mapper/test_model_pytree_tuple_prior.py`: cases (a) nothing free,
  (b) grid_offset free, (c) grid_offset + scalar keep `prior_count` 0/2/3 and `grid_offset`
  a `TuplePrior`; plus a direct `TuplePrior` round-trip. 3 of 4 fail without the fix.
- Tests: full `test_autofit` 4295 passed; autofit + autogalaxy smoke 26/26.
- Known gap (out of scope on the issue): fixed non-prior attributes (e.g. a fixed sky level)
  are not carried through the round-trip, so `instance_from_*` on the rebuilt model in case (b)
  looks up prior config for them. Follow-up filed as its own task.

- pending-release: PyAutoFit@https://github.com/PyAutoLabs/PyAutoFit/pull/1779

## Original prompt

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
Consequence: glance
Witness: A round-trip test through `jax.tree_util.tree_flatten` / `tree_unflatten` after `autofit.jax.register_model`, over a `Model` with zero direct priors and a `TuplePrior` child (the `DatasetModel` shape) with (a) nothing free, (b) the tuple free, (c) the tuple plus one scalar free, passes with `prior_count` equal before and after (0, 2, 3).
Review-minutes: 3
Issued: 2026-11-16
Verified: 2026-11-16 ac881b5c (PyAutoFit)
Lane: any
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

## Answers from the human
- Q3 (2026-11-16, shift 2026-11-16-pm question on PyAutoFit#1777): Use 1: (a) override — separate worktree off main for this fix alongside #1773, since no files overlap. https://github.com/PyAutoLabs/PyAutoFit/issues/1777#issuecomment-6925624924
