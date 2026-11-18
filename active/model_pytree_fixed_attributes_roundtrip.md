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
