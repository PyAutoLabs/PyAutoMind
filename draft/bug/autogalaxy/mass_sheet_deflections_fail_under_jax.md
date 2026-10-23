# `@PyAutoGalaxy` MassSheet deflections fail under JAX (ArrayIrregular into `xp.multiply`)

Type: bug
Target: autogalaxy
Repos:
- @PyAutoGalaxy
Themes:
- jax
- mass-profiles
Difficulty: small
Autonomy: supervised
Priority: low
Status: formalised
Consequence: glance
Witness: `ag.mp.MassSheet(kappa=0.5).deflections_yx_2d_from(grid=aa.Grid2DIrregular([(0.1, 0.2)]), xp=jnp)` returns (0.05, 0.1), matches NumPy, and works under `jax.jit`; a unit test covers it.
Filed: 2026-10-23
Issue: https://github.com/PyAutoLabs/PyAutoGalaxy/issues/658

## Why

Found while reproducing PyAutoLens#799: a `MassSheet` host reproduced the singular-core candidate in NumPy but could not run under JAX. Verified 2026-10-23:

```
TypeError: multiply requires ndarray or scalar arguments, got <class 'autoarray.structures.arrays.irregular.ArrayIrregular'> at position 0.
```

`MassSheet.deflections_yx_2d_from` (`autogalaxy/profiles/mass/sheets/mass_sheet.py`) passes `radius=self.kappa * grid_radii`, where `grid_radii` comes from the decorated `radial_grid_from` as an `ArrayIrregular`. `GeometryProfile._cartesian_grid_via_radial_from` then calls `xp.multiply(radius[:, None], ...)`, which jnp rejects. NumPy accepts the wrapper.

## Deliverables

1. Pass the raw array (e.g. `grid_radii.array`). Audit other `_cartesian_grid_via_radial_from` callers for the same pattern.
2. Unit test of eager-NumPy vs `xp=jnp` vs `jax.jit` parity for `MassSheet` deflections.
