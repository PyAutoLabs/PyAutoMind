## Outcome

Shipped in PyAutoFit#1781 (merged `3ba1e6c3`, 2026-11-18). Follow-up to PyAutoFit#1777/#1779.

- `Model.tree_flatten` (`autofit/mapper/prior_model/prior_model.py`) carries the model's fixed
  direct attributes (not priors, tuple priors or child models; `cls`, `id` and private names
  skipped) in the aux data via `_direct_fixed_tuples`; `tree_unflatten` passes them back as
  keyword arguments, so the rebuilt model never falls back to a prior-config lookup.
- `test_autofit/mapper/test_model_pytree_tuple_prior.py`: instance round-trip
  (`instance_from_prior_medians`, `instance_from_vector`) for cases a-c with a fixed sky level;
  fails in a and b without the fix.
- Tests: CI GREEN; pytree/register_model files 190 passed; autofit + autogalaxy smoke passed.
- Identifiers: model and search identifiers for five models (incl. shared prior and a
  `DatasetModel` with fixed sky) identical before (`ac881b5cd`) and after (`aeac68800`).
- Known limit: a fixed attribute that is unhashable (numpy array, list) now sits in pytree aux
  data and could break JAX treedef comparison. Nothing flattens a `Model` under jit today
  (`Fitness` closes over the model), so left as is.


## Original prompt

# Model pytree round-trip drops fixed non-prior attributes (e.g. a fixed sky level)

Type: bug
Target: PyAutoFit
Repos:
- PyAutoFit
Difficulty: small
Autonomy: safe
Priority: medium
Status: formalised
Issued: 2026-11-18
Consequence: glance
Witness: after `autofit.jax.register_model`, a `Model` of a `DatasetModel`-shaped class with `grid_offset` free and a FIXED scalar attribute (e.g. a fixed sky level) round-trips through `jax.tree_util.tree_flatten` / `tree_unflatten` with the fixed value preserved, and `instance_from_prior_medians()` (or `instance_from_vector`) on the rebuilt model succeeds without looking up prior config for the fixed attribute and returns the same instance as the original model
Review-minutes: 5
Unattended: ready
Lane: any

Follow-up to PyAutoFit#1777 / PR #1779 (merged 2026-11-18; record
`complete/2026/11/dataset-model-free-grid-offset-pytree-roundtrip.md`). Human request,
verbatim: "Do the small follow up after prm".

#1779 made `Model.tree_flatten` carry direct priors and `TuplePrior` attributes as pytree
children, but fixed non-prior attributes on the `Model` (a float or other constant set on
the model, e.g. a fixed sky level) are not carried in the aux data. `tree_unflatten`
therefore rebuilds the model without them, and making an instance from the rebuilt model
in case (b) of `test_autofit/mapper/test_model_pytree_tuple_prior.py` falls back to a
prior-config lookup for the missing attribute (which a config-less class does not have).

Fix: carry the `Model`'s fixed (non-prior, non-`TuplePrior`) direct attributes in
`tree_flatten`'s aux data and restore them in `tree_unflatten`
(`autofit/mapper/prior_model/prior_model.py`); extend the #1779 test file with an
instance round-trip for cases (a)-(c) asserting the fixed value survives. Out of scope:
nested child models beyond what the existing flatten already recurses into.
