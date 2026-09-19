# Carry flat fields through profiling pipeline resume

Type: maintenance
Target: autolens_profiling
Repos:
- autolens_profiling
Epic: mass-field
Status: draft
Autonomy: supervised
Difficulty: medium
Consequence: judge
Witness: each of the five resumed stage models contains the expected free or fixed top-level field, and the resume smoke completes without changing committed result artifacts
Filed: 2026-09-19
Unblocked: 2026-09-19 — PyAutoGalaxy#625 and PyAutoLens#745 are merged; the human approved consuming the helper from current source `main`. The profiling parallel-worktree waiver remains in force.

## Original user request

> We have been doing work which updates workspaces and lots more to a fields API, can we review where the updating te API for everything got too (E.g. I dont think we have done HowToLens) and continue all of that until its done?
>
> yes do all that, note that autolens_jax_joss is deleted more recently. But lets go

## Scope and plan

Migrate five galaxy-attached shear calls in `scripts/misc/pipeline_resume/slam_resume.py`. Carry one top-level field through source LP, source PIX 1/2, light LP, and mass total. Use `al.util.chaining.mass_and_fields_from` where mass priors and field priors move together; use an instance field only when the existing stage fixed shear. Verify each stage model's field prior or fixed value and run the script's resume smoke/witness. This is a separate PR after the 47 independent live builders, not a text replacement in a chained model.

This is a one-file consumer migration using an existing merged API. It adds no public API and needs no design, library, or documentation phase.
