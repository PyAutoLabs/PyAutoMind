## mass-field-inference-sim
- issue: https://github.com/PyAutoLabs/autolens_inference/issues/7 (closed completed 2026-09-19)
- completed: 2026-09-19
- workspace-pr: https://github.com/PyAutoLabs/autolens_inference/pull/8 (merge fc408426)
- epic: mass-field (consumer sweep)
- summary: Migrated the imaging and interferometer simulators to `MassField` and `Tracer(fields=[field])`. Compile, Ruff, README generator, wall submit checks, 55 repository tests, and both simulator smoke entries passed. The lint workflow passed and the PR merged on 2026-09-19. The staged inference SLaM migration remains separately tracked until the chaining helper is released.

## Original prompt

# Move inference simulators to flat fields

Type: maintenance
Target: autolens_inference
Repos:
- autolens_inference
Epic: mass-field
Status: draft
Autonomy: supervised
Filed: 2026-09-19
Issued: 2026-09-19

## Original user request

> We have been doing work which updates workspaces and lots more to a fields API, can we review where the updating te API for everything got too (E.g. I dont think we have done HowToLens) and continue all of that until its done?
>
> yes do all that, note that autolens_jax_joss is deleted more recently. But lets go

## Scope

Migrate `scripts/misc/simulators/{imaging,interferometer}.py` from galaxy-attached shear to `MassField` passed through `Tracer(fields=[field])`. These two scripts do not depend on the pending chaining helper. Validate their construction and repository lint and smoke checks. The staged SLaM runner remains in the separate `mass_field_flat_adoption.md` prompt until the helper is merged and released.
