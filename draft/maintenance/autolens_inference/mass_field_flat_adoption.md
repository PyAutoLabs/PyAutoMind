# Move inference SLaM stages to flat fields

Type: maintenance
Target: autolens_inference
Repos:
- autolens_inference
Epic: mass-field
Status: draft
Autonomy: supervised
Filed: 2026-09-19
Issued: 2026-09-19
Blocked-by: PyAutoGalaxy#625 and PyAutoLens#745 merged/released for the new `mass_and_fields_from` helper

## Original user request

> We have been doing work which updates workspaces and lots more to a fields API, can we review where the updating te API for everything got too (E.g. I dont think we have done HowToLens) and continue all of that until its done?
>
> yes do all that, note that autolens_jax_joss is deleted more recently. But lets go

## Scope

Migrate all five staged model builders in `scripts/misc/slam/_runner.py` so `fields=field` survives source LP, both source PIX stages, light LP, and mass total. Use `al.util.chaining.mass_and_fields_from` for mass-chaining stages, with explicit prior versus fixed-instance choices at every stage. Validate each stage and the repository lint/smoke checks; do not alter committed science result rows without a new run. The two independent simulators are tracked in a separate task so they can land before the helper is released.

This is the inference slice of `draft/maintenance/autolens_profiling/mass_field_flat_adoption_science_repos.md`.
