## mass-field-profiling-live
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/287 (closed completed 2026-09-19)
- completed: 2026-09-19
- workspace-pr: https://github.com/PyAutoLabs/autolens_profiling/pull/288 (merge 5584028a)
- epic: mass-field (live profiling consumer sweep)
- summary: Migrated all 47 live, non-chaining profiling builders from galaxy-attached shear to top-level `MassField` models passed through flat `fields=` collections and manually assembled tracers. Five inline historical witnesses and five staged `scripts/misc/pipeline_resume/slam_resume.py` calls remain intentionally unchanged. Validation included the AST audit, Ruff, README and wall checks, 665 passing tests with 5 skips, the profiling smoke set, and imaging/interferometer runtime witnesses. CI passed after its timing-only real-likelihood threshold received the approved minimal relaxation from 3.0% to 3.1%. The staged pipeline remains tracked in `draft/maintenance/autolens_profiling/mass_field_pipeline_resume.md` until the chaining helper is publicly released.

## Original prompt

# Move live profiling builders to flat fields

Type: maintenance
Target: autolens_profiling
Repos:
- autolens_profiling
Epic: mass-field
Status: draft — human approved separate worktree waiver 2026-09-19
Autonomy: supervised
Filed: 2026-09-19
Issued: 2026-09-19
Difficulty: large

## Original user request

> We have been doing work which updates workspaces and lots more to a fields API, can we review where the updating te API for everything got too (E.g. I dont think we have done HowToLens) and continue all of that until its done?
>
> yes do all that, note that autolens_jax_joss is deleted more recently. But lets go

## Scope and plan

AST audit on 2026-09-19 found 57 galaxy-attached shear calls in `scripts/`: 5 inline historical witnesses, 5 staged calls in `scripts/misc/pipeline_resume/slam_resume.py`, and 47 other live builders. This prompt covers the 47 live non-chaining builders; `mass_field_pipeline_resume.md` covers the staged chain after the helper release. Move shear to a top-level `MassField` at lens redshift in each model, include `fields=field` in every outer `af.Collection`, and pass fields into every manually built tracer. Preserve the following measurements exactly: `fixed_light_numba_s4_witness.py`, `*_levers_l{2,3}_witness.py`, `fixed_light_draws.py`, `fixed_light_trace.py`, and `results/hazards/component/profile_registry_coverage.json`.

Run AST audit, Ruff, README generator check, PR smoke, and one representative imaging/interferometer/point-source script where available. Do not rewrite committed result rows from past versions. The repo is currently claimed by `hst-gpu-residue-p2`; its dirty files are the excluded `fixed_light_trace.py`, an HPC submit script and result artifacts. **Human waiver, 2026-09-19:** proceed in a separate flat-fields profiling worktree, preserving that task's files and results. Record the waiver in `active.md` and restrict this task to disjoint paths.
