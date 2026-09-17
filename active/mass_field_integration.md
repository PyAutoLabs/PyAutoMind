# MassField in PyAutoLens: Tracer(fields=), the analysis `fields` slot, COOLEST 1:1, LOS sheets, model_util helper

Type: feature
Target: PyAutoLens
Repos:
- PyAutoLens
Themes:
- cluster
Difficulty: large
Autonomy: supervised
Priority: normal
Consequence: judge
Witness: `al.Tracer(galaxies=[lens, source], fields=[al.MassField(redshift=0.5, shear=...)]).traced_grid_2d_list_from(grid)` is `np.allclose` to the same shear on `lens`; `tracer.galaxies` is `[lens, source]` (no field in it); a model with `fields=af.Collection(field=af.Model(al.MassField, ...))` fits through `AnalysisImaging` under `PYAUTO_TEST_MODE=2`; COOLEST round trip of that tracer returns an `al.MassField` with the same parameters to 1e-12 and a legacy `al.Galaxy(..., shear=...)` still exports byte-identically; `al.model_util.mass_field_from(lens=lens_model, potential=True).potential.centre is lens_model.mass.centre`; identifier pin (galaxy-attached model, equal on `main` and branch); `pytest test_autolens -q -n auto` green.
Review-minutes: 10
Unattended: ready
Epic: mass-field
Phase: 2
Filed: 2026-09-17
Issued: 2026-09-17

Gate cleared 2026-09-17: phase 1 (`complete/2026/09/mass-field-class.md`,
PyAutoGalaxy#621) is merged on PyAutoGalaxy `main`; CI runs the same-named
library branch, so `main` is enough and a release is not required for this
phase.

Teach PyAutoLens about `ag.MassField` (phase 1 of the epic
`draft/feature/autogalaxy/mass_field_epic.md`; read it first). A field is its
own thing: it gets its own tracer argument and its own model slot, and only the
tracer's planes merge it with the galaxies. `tracer.galaxies` never holds a
field, so every script that indexes galaxies positionally keeps working.

## What to build

1. **`Tracer(galaxies, fields=None, cosmology=...)`** — `@PyAutoLens/autolens/lens/tracer.py`:
   - store `self.fields` (a list; `[]` when None); validate members on
     `redshift` the way `_validate_galaxies` does, with a message naming
     `MassField`.
   - `galaxies_ascending_redshift`, `plane_redshifts` and `planes` are built
     over galaxies **and** fields; a plane (an `ag.Galaxies`) may therefore
     hold a `MassField`, which phase 1 made safe. Everything downstream
     (`traced_grid_2d_list_from`, `deflections_yx_2d_from`,
     `convergence_2d_from`, `potential_2d_from`, `has`, `cls_list_from`, the
     positions solver, magnification, critical curves) flows through planes
     and needs no change — verify each with a test rather than assume.
   - `tracer.galaxies` is unchanged; `tracer.fields` is the new accessor;
     `total_planes` counts field-only planes (a LOS sheet plane is a plane).
   - `sliced_tracer_from` places fields in the planes nearest their redshift
     like `line_of_sight_galaxies`; `to_dict`/`from_dict` carries `fields`;
     the JAX pytree flatten of `Tracer` includes `fields`
     (`@PyAutoLens/autolens/jax/registration.py` walks `tracer.galaxies` — walk
     `tracer.fields` too and register `MassField`; the walker is a copy of the
     autogalaxy one by a recorded human decision, so patch both, do not share).
   - `MultiPlaneRedshiftWarning`: fields are mass-bearing for the light/mass
     ordering check.
   - The per-galaxy surfaces (`FitImaging.galaxy_model_image_dict`,
     `subplot_galaxies_images`, the aggregator's galaxy tables) iterate
     `tracer.galaxies` and therefore never see a field — assert that in a test.
2. **Analysis `fields` slot** — `@PyAutoLens/autolens/analysis/analysis/lens.py`
   `tracer_via_instance_from`: beside the `extra_galaxies` / `scaling_galaxies`
   folds, `fields = list(instance.fields) if getattr(instance, "fields", None) is not None else None`
   and pass `Tracer(galaxies=galaxy_list, fields=fields, cosmology=cosmology)`.
   Same in the interferometer / point-source analyses if they build their own
   tracer. The subhalo `perturb` path is unchanged.
3. **COOLEST** — `@PyAutoLens/autolens/interop/coolest.py`:
   - `to_coolest`: each `tracer.fields` entry becomes one COOLEST `MassField`
     entity carrying all its profiles (`ExternalShear` → `ExternalShear`,
     `MassSheet` → `ConvergenceSheet`; `ExternalPotential` has no COOLEST
     profile — route it through the existing `on_unsupported` path with the
     profile named). **Keep the legacy peel**: a `Galaxy` carrying sheets still
     exports them as a separate `MassField` entity, byte-identical to today's
     output (the workspace_test round-trip script is the regression).
   - `from_coolest`: a COOLEST `MassField` entity becomes an `al.MassField`
     in the returned tracer's `fields`, not a `Galaxy`. Update the docstring.
4. **Line-of-sight sampler** — `@PyAutoLens/autolens/lens/los.py` builds
   `ag.Galaxy(redshift=z_cen, mass_sheet=...)` per plane; build `ag.MassField`
   and return the sheets separately (`galaxies_from` → halos as galaxies,
   `fields_from` → sheets, or one call returning both) so the caller writes
   `Tracer(galaxies=[lens, source] + halos, fields=sheets)`. Keep a shim for
   the old single-list return if any caller in the tests or the workspace
   `los_halos` scripts depends on it, and say which in the PR.
5. **`model_util` helper** — beside `mge_model_from` (the module the workspace
   reaches as `al.model_util`): `mass_field_from(lens, shear=True,
   mass_sheet=False, potential=False, redshift=None) -> af.Model`. Builds
   `af.Model(al.MassField, redshift=<lens.redshift unless given>, ...)` with
   `af.Model(al.mp.ExternalShear)` / `af.Model(al.mp.MassSheet)` /
   `af.Model(al.mp.ExternalPotential)` as requested, and **ties
   `potential.centre` (and `mass_sheet.centre`) to `lens.mass.centre` as a shared
   prior** — the human's convention for where an external potential is centred.
   `lens` is an `af.Model` of a `Galaxy` with a `mass`; if it has none, raise
   naming the galaxy. Document that for a multi-deflector system the caller
   picks the primary galaxy explicitly, and that the result goes in
   `fields=af.Collection(field=...)`.
6. **Tests + docs** — tracer tests for each bullet of step 1; an analysis
   test fitting a model with `fields` under test mode; round-trip and
   legacy-peel COOLEST tests; a `test_model_util` case for each helper flag and
   the shared-prior identity; `los` tests for the new return; the identifier
   pin; API docs for `MassField` (re-export in `@PyAutoLens/autolens/__init__.py`
   beside `Galaxy`), `Tracer.fields` and `model_util.mass_field_from`.

## Hard constraints

- Legacy galaxy-attached sheets and shear-only galaxies in `galaxies`: no
  warning, no behaviour change, COOLEST export unchanged (regression-test it).
- `tracer.galaxies` never contains a field.
- No prior config changes.
