# MassField in PyAutoLens: pytree registration, COOLEST 1:1 mapping, LOS sheets, model_util helper

Type: feature
Target: PyAutoLens
Repos:
- PyAutoLens
Themes:
- cluster
Difficulty: medium
Autonomy: supervised
Priority: normal
Consequence: glance
Witness: COOLEST round trip of a tracer holding `al.MassField(redshift=0.5, shear=..., mass_sheet=...)` returns an `al.MassField` (not a `Galaxy`) with the same parameters to 1e-12; a legacy `al.Galaxy(..., shear=...)` still exports a `MassField` entity exactly as before; `al.model_util.mass_field_from(lens=lens_model, potential=True).potential.centre is lens_model.mass.centre` (shared prior); `pytest test_autolens -q -n auto` green; `autolens/analysis/` untouched.
Review-minutes: 8
Unattended: ready
Epic: mass-field
Phase: 2
Blocked-by: phase 1 (`draft/feature/autogalaxy/mass_field_class.md`) merged on PyAutoGalaxy main — CI runs the same-named library branch, so main is enough; a release is not required for this phase
Filed: 2026-09-17

Teach PyAutoLens about `ag.MassField` (phase 1 of the epic
`draft/feature/autogalaxy/mass_field_epic.md`; read it first). The tracer needs
nothing: it duck-types on `redshift` and promises `Galaxy` subclasses work. The
work is at the four seams that name the class.

## What to build

1. **JAX registration** — `@PyAutoLens/autolens/jax/registration.py` registers
   `Galaxy` by class; add `MassField` the same way (the walker is a copy of the
   autogalaxy one by a recorded human decision, so patch both, do not share).
2. **COOLEST** — `@PyAutoLens/autolens/interop/coolest.py`:
   - `to_coolest`: an `al.MassField` in the galaxy list becomes one COOLEST
     `MassField` entity carrying all its profiles (`ExternalShear` →
     `ExternalShear`, `MassSheet` → `ConvergenceSheet`; `ExternalPotential` has no
     COOLEST profile — route it through the existing `on_unsupported` path with
     the profile named). **Keep the legacy peel**: a `Galaxy` carrying sheets
     still exports them as a separate `MassField` entity, byte-identical to
     today's output (the workspace_test round-trip script is the regression).
   - `from_coolest`: a COOLEST `MassField` entity becomes an `al.MassField`,
     not a `Galaxy` holding external profiles. Update the docstring that says
     otherwise.
3. **Line-of-sight sampler** — `@PyAutoLens/autolens/lens/los.py` builds
   `ag.Galaxy(redshift=z_cen, mass_sheet=ag.mp.MassSheet(kappa=kappa_neg))` per
   plane; build `ag.MassField` instead. This is simulation-side (no model, no
   identifier), but grep the tests and the workspace `los_halos` scripts for
   `hasattr(g, "mass_sheet")` detection, which keeps working, and note in the
   PR that `isinstance(g, al.MassField)` is now the cleaner test (phase 3 uses it).
4. **`model_util` helper** — beside `mge_model_from` (find the module the
   workspace reaches as `al.model_util`): `mass_field_from(lens, shear=True,
   mass_sheet=False, potential=False, redshift=None) -> af.Model`. Builds
   `af.Model(al.MassField, redshift=<lens.redshift unless given>, ...)` with
   `af.Model(al.mp.ExternalShear)` / `af.Model(al.mp.MassSheet)` /
   `af.Model(al.mp.ExternalPotential)` as requested, and **ties
   `potential.centre` (and `mass_sheet.centre`) to `lens.mass.centre` as a shared
   prior** — the human's convention for where an external potential is centred.
   `lens` is an `af.Model` of a `Galaxy` with a `mass`; if it has none, raise
   with a message naming the galaxy. Document that for a multi-deflector
   system the caller picks the primary galaxy explicitly.
5. **Tests + docs** — round-trip and legacy-peel tests in the COOLEST test
   module; a `test_model_util` case for each helper flag and the shared-prior
   identity; `los` test updated for the new type; API docs entry for
   `MassField` (re-export in `@PyAutoLens/autolens/__init__.py` beside
   `Galaxy`) and for `model_util.mass_field_from`.

## Hard constraints

- `autolens/analysis/` is not edited: the field lives in the `galaxies`
  collection and reaches the tracer through the existing path.
- Legacy galaxy-attached sheets: no warning, no behaviour change, COOLEST
  export unchanged (regression-test it).
- No prior config changes.
