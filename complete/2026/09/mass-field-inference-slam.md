## mass-field-inference-slam
- issue: https://github.com/PyAutoLabs/autolens_inference/issues/9 (closed completed 2026-09-19)
- completed: 2026-09-19
- workspace-pr: https://github.com/PyAutoLabs/autolens_inference/pull/10 (merge f9266f57)
- epic: mass-field (staged inference consumer)
- summary: Migrated all five inference SLaM stages to a top-level `MassField`. Source LP creates the free field, source PIX 1 and mass total carry model fields through `mass_and_fields_from`, and source PIX 2 plus light LP use fixed instance fields. The helper is consumed from current PyAutoGalaxy/PyAutoLens source `main`; no packaged release is required. Validation: the five-stage runtime field witness and 56 tests passed, with Ruff, formatting, README, wall, smoke, and required CI checks green.

## Original prompt

# Move inference SLaM stages to flat fields

Type: maintenance
Target: autolens_inference
Repos:
- autolens_inference
Epic: mass-field
Status: draft
Autonomy: supervised
Difficulty: medium
Consequence: judge
Witness: each of the five SLaM builder stages returns a root collection with the expected free or fixed field, and repository lint, tests, and the SLaM smoke entry pass without changing committed science results
Filed: 2026-09-19
Issued: 2026-09-19
Unblocked: 2026-09-19 — PyAutoGalaxy#625 and PyAutoLens#745 are merged, the human approved consuming the helper from current source `main`, and the autolens_inference#8 simulator task is complete.

## Original user request

> We have been doing work which updates workspaces and lots more to a fields API, can we review where the updating te API for everything got too (E.g. I dont think we have done HowToLens) and continue all of that until its done?
>
> yes do all that, note that autolens_jax_joss is deleted more recently. But lets go

## Scope

Migrate all five staged model builders in `scripts/misc/slam/_runner.py` so `fields=field` survives source LP, both source PIX stages, light LP, and mass total. Use `al.util.chaining.mass_and_fields_from` for mass-chaining stages, with explicit prior versus fixed-instance choices at every stage. Validate each stage and the repository lint/smoke checks; do not alter committed science result rows without a new run. The two independent simulators are tracked in a separate task so they can land before the helper is released.

This is the inference slice of `draft/maintenance/autolens_profiling/mass_field_flat_adoption_science_repos.md`.

This is a one-file consumer migration using an existing merged API. It adds no public API and needs no design, library, or documentation phase.

## Stage mapping from the 2026-09-19 code review

| Stage | Existing shear route | Intended flat field route |
|---|---|---|
| source LP | free `ExternalShear` on lens Galaxy | free `MassField(redshift=redshift_lens, shear=...)` in root `fields=` |
| source PIX 1 | lens shear model from source LP | `mass_and_fields_from(..., fields_result=source_lp_result.model.fields)`; root `fields=` |
| source PIX 2 | fixed shear instance from PIX 1 | fixed `source_pix_result_1.instance.fields` |
| light LP | fixed shear instance from lens-source result | fixed `source_result_for_lens.instance.fields` |
| mass total | free shear model from lens-source result | `mass_and_fields_from(..., fields_result=source_result_for_lens.model.fields)` |

Test each builder's returned model collection for a field and its expected prior/fixed type, then run Ruff, README/wall checks, `pytest scripts/misc/test -q`, and the repository's SLaM smoke entry. The whole staged fit is expensive and its result rows must not be silently rewritten.
