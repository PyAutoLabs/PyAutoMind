# Move inference SLaM stages to flat fields

Type: maintenance
Target: autolens_inference
Repos:
- autolens_inference
Epic: mass-field
Status: draft
Autonomy: supervised
Filed: 2026-09-19
Unblocked: 2026-09-19 — PyAutoGalaxy#625 and PyAutoLens#745 are merged, the human approved consuming the helper from current source `main`, and the autolens_inference#8 simulator task is complete.

## Original user request

> We have been doing work which updates workspaces and lots more to a fields API, can we review where the updating te API for everything got too (E.g. I dont think we have done HowToLens) and continue all of that until its done?
>
> yes do all that, note that autolens_jax_joss is deleted more recently. But lets go

## Scope

Migrate all five staged model builders in `scripts/misc/slam/_runner.py` so `fields=field` survives source LP, both source PIX stages, light LP, and mass total. Use `al.util.chaining.mass_and_fields_from` for mass-chaining stages, with explicit prior versus fixed-instance choices at every stage. Validate each stage and the repository lint/smoke checks; do not alter committed science result rows without a new run. The two independent simulators are tracked in a separate task so they can land before the helper is released.

This is the inference slice of `draft/maintenance/autolens_profiling/mass_field_flat_adoption_science_repos.md`.

## Stage mapping from the 2026-09-19 code review

| Stage | Existing shear route | Intended flat field route |
|---|---|---|
| source LP | free `ExternalShear` on lens Galaxy | free `MassField(redshift=redshift_lens, shear=...)` in root `fields=` |
| source PIX 1 | lens shear model from source LP | `mass_and_fields_from(..., fields_result=source_lp_result.model.fields)`; root `fields=` |
| source PIX 2 | fixed shear instance from PIX 1 | fixed `source_pix_result_1.instance.fields` |
| light LP | fixed shear instance from lens-source result | fixed `source_result_for_lens.instance.fields` |
| mass total | free shear model from lens-source result | `mass_and_fields_from(..., fields_result=source_result_for_lens.model.fields)` |

Test each builder's returned model collection for a field and its expected prior/fixed type, then run Ruff, README/wall checks, `pytest scripts/misc/test -q`, and the repository's SLaM smoke entry. The whole staged fit is expensive and its result rows must not be silently rewritten.
