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

A `DatasetModel` whose `grid_offset` is a free parameter cannot be round-tripped
through `autofit.jax.register_model`: unflattening raises

    TypeError  (Prior.tree_unflatten)

Found while building the free-`grid_offset` control for `gaussian-precompute-p2`
(record `complete/2026/09/gaussian-precompute-p2.md`). The control was run a
different way and the phase shipped, so this blocks nothing today — but any JAX
model that wants a free grid offset hits it.

## Fix

Make `Prior.tree_unflatten` accept the children `register_model` hands it for a
free `grid_offset`, and add a round-trip test over a `DatasetModel` with one.
