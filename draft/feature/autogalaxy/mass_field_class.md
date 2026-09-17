# MassField: a MassProfile-only sibling of Galaxy for external shear, mass sheets and external potentials

Type: feature
Target: PyAutoGalaxy
Repos:
- PyAutoGalaxy
Themes:
- cluster
Difficulty: small
Autonomy: supervised
Priority: normal
Consequence: glance
Witness: `ag.MassField(redshift=0.5, shear=ag.mp.ExternalShear(0.05, 0.05)).deflections_yx_2d_from(grid)` is `np.array_equal` to the same profile on an `ag.Galaxy`; `ag.MassField(redshift=0.5, bulge=ag.lp.Sersic())` raises; `git diff --stat` shows `autogalaxy/galaxy/galaxy.py` and `autogalaxy/config/priors/` untouched; `pytest test_autogalaxy -q -n auto` green.
Review-minutes: 5
Unattended: ready
Epic: mass-field
Phase: 1
Filed: 2026-09-17

Add `MassField` to PyAutoGalaxy: the redshift-bearing container for the mass
components that describe the tidal field of everything *outside* the modelled
system — `ExternalShear`, `MassSheet`, `ExternalPotential` — so a model can say
"this is a property of the system" instead of pinning the field to one galaxy.
The design, prior art and the backwards-compatibility invariant are in the epic
ledger `draft/feature/autogalaxy/mass_field_epic.md`; read it first.

## What to build

1. **`@PyAutoGalaxy/autogalaxy/galaxy/mass_field.py`** — `class MassField(Galaxy)`.
   - `__init__(self, redshift, **kwargs)`: call `Galaxy.__init__`, then validate
     that every component is a `MassProfile` (`autogalaxy.profiles.mass.abstract.abstract.MassProfile`).
     A `LightProfile`, `Pixelization`, `Regularization` or anything else raises
     `exc.GalaxyException` naming the offending key and saying what a
     `MassField` is for. The list-rejection message `Galaxy` already has still
     applies (inherited).
   - Do **not** restrict to the three sheet classes: any `MassProfile` is
     accepted (a user may want an NFW "environment" halo as a field). The
     docstring names the three intended ones.
   - `__repr__`: `MassField(redshift=..., <component names>)` so it never prints
     as a `Galaxy`.
   - Inherits every aggregate method unchanged: `deflections_yx_2d_from`,
     `convergence_2d_from`, `potential_2d_from` sum the profiles;
     `image_2d_from` returns zeros because `has(cls=LightProfile)` is False by
     construction. No override needed — verify with tests rather than re-implement.
   - `dict()`/`to_dict` round trip via `autonerves.dictable` must rebuild a
     `MassField`, not a `Galaxy` (the type path is what dictable stores; test it).
2. **Export** `ag.MassField` from `@PyAutoGalaxy/autogalaxy/__init__.py` beside
   `Galaxy` / `Galaxies`.
3. **JAX pytree registration** — `@PyAutoGalaxy/autogalaxy/jax/registration.py`
   registers `Galaxy` with `no_flatten=("redshift",)`; register `MassField` the
   same way in the same walker (a subclass is a distinct pytree type). Measure
   with the three-way probe from `complete/2026/07/public-register-galaxies-classes.md`
   using a `MassField` in the `Galaxies` list.
4. **Tests** — `@PyAutoGalaxy/test_autogalaxy/galaxy/test_mass_field.py`:
   construction with each of the three sheets and with all three; rejection of
   light profiles / pixelizations with the named key in the message; field
   equality of deflections / convergence / potential against the same profiles
   on a `Galaxy`; `image_2d_from` zeros; `Galaxies([galaxy, mass_field])`
   aggregate sums; `to_dict`/`from_dict` round trip type; `__repr__`.
5. **Docs** — `@PyAutoGalaxy/docs/api/galaxy.rst` gains `MassField`; a short
   "External fields" paragraph in the galaxy overview page explaining when to
   use it and that the galaxy-attached form remains supported.

## Hard constraints

- **`autogalaxy/galaxy/galaxy.py` is not edited.** Not a docstring, not a
  type hint. The `Galaxy`-attached form is the backwards-compatible API and its
  PyAutoFit result identifiers must not move; the cheapest proof is that the
  file is absent from the diff.
- No deprecation warning anywhere for sheets on a `Galaxy`.
- No prior config changes (`autogalaxy/config/priors/`): `MassField` holds
  profiles whose priors already resolve by profile class.

## Out of scope (later phases)

PyAutoLens registration, COOLEST mapping, the LOS sampler and the
`model_util` helper are phase 2; workspaces are phases 3–5.
