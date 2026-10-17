# Imaging production over-sampling presets — phase 1 (workspace-only)

Type: feature
Target: autolens_profiling
Repos:
- autolens_profiling
Difficulty: medium
Autonomy: supervised
Priority: normal
Consequence: judge
Campaign: PyAutoPulse `imaging` / task `tasks/imaging_production_over_sampling.md`
Issue: https://github.com/PyAutoLabs/autolens_profiling/issues/430

## Request (verbatim, relayed by the architect session; human authorised 2026-10-17 "Yes launch 1 and 2 now")

Phase 1 as recorded: "workspace-only: --instrument euclid|hst presets for the JAX
Delaunay runtime/breakdown cells, keeping flat-1 selectable; CPU smoke only. A100
re-measure is a separate compute-authorized phase." Evidence/context:
PyAutoArray#606.

Goal: ONE bounded phase. Add `--instrument euclid|hst` presets (production
over-sampling settings as the task and PyAutoArray#606 define them) to the JAX
Delaunay runtime and breakdown cells, keep the current flat sub-size 1 selectable
and the default behaviour unchanged, and verify by CPU smoke (functional run, not
timing) that each preset executes and produces the catalogue-conformant JSON. No
measurements are recorded as campaign evidence in this phase; no A100 jobs.
