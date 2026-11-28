# Workspace examples: simulate CDM subhalos and line-of-sight halos

Type: feature
Target: autolens_workspace
Repos:
- autolens_workspace
Difficulty: large
Autonomy: supervised
Priority: normal
Status: formalised
Consequence: glance
Witness: the rewritten `los_halos` scripts run end to end from released code in the workspace smoke test.
Review-minutes: 3
Unattended: ready
Lane: wsl-data

## Finding

`scripts/imaging/features/advanced/los_halos/` (`start_here.py`, `simulator.py`, `simulator_jax.py`)
shows the old `LOSSampler` with 4 + 4 planes and has no lens subhalos. Once the arrays-first
line-of-sight sampler, the subhalo sampler and the chunked ray tracing are in the library, the
examples should show them.

Source of truth: the `dm_sightlines` science project, `~/Science/Science/development/dm_sightlines` (local git, no remote; commit 845c5b3 or later). Its presets were frozen by the human on 2026-11-26 (`wiki/project/phase5_note.md` section 8). Port the validated code; do not redesign the physics.

## What to build

- Rewrite the `los_halos` examples on the new API: sample a line-of-sight realisation at a
  redshift spacing of 0.01, render it with the chunked multi-plane path, simulate an image.
- A subhalo example with the `cdm_fiducial` preset and one with `ORiordan2025`, and a combined
  subhalo plus line-of-sight simulation.
- State the limits in the text: float64, the dependence of the subhalo signal on the stripping
  model, and that most of the raw image difference is a bulk source-plane shift a refit absorbs.

## Out of scope

The project's chi-squared diagnostics ladder and anything with a pixelised source.

Depends on the four library prompts from the same project being released (truncated NFW
constructors, chunked ray tracing, line-of-sight sampler, subhalo sampler). Workspace scripts
only: no library change belongs here.
This is the exit criterion of the project's phase 6: workspace examples run from released code.

Witness: the rewritten `los_halos` scripts run end to end from released code in the workspace smoke test.

<!-- formalised by the Intake (Conception) Agent on 2026-11-26 from file:/home/jammy/Science/Science/scratch/dm_sightlines_phase6_prompts/5_workspace.md -->
