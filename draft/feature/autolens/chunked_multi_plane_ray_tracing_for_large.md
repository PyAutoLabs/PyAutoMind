# Chunked multi-plane ray tracing for large halo populations

Type: feature
Target: PyAutoLens
Repos:
- PyAutoLens
Difficulty: large
Autonomy: supervised
Priority: normal
Status: formalised
Consequence: glance
Witness: a PyAutoLens test traces one realisation of at least 5,000 halos on 99 planes through the chunked path and through `Tracer`, agreeing to 1e-9 arcsec, with results identical across two chunk sizes.
Review-minutes: 3
Unattended: ready
Lane: wsl-data

## Finding

`substructure_util.traced_grids_via_scan` (through `Profile.vmapped_deflections_from`) materialises a
(halos x pixels x 2) array per plane: 9.3 GB for a 10^6 M_sun lower mass limit on a 101 x 101 grid.
It cannot render a CDM population down to 10^6 M_sun with sub-pixel sampling.

Source of truth: the `dm_sightlines` science project, `~/Science/Science/development/dm_sightlines` (local git, no remote; commit 845c5b3 or later). Its presets were frozen by the human on 2026-11-26 (`wiki/project/phase5_note.md` section 8). Port the validated code; do not redesign the physics.

The project's render layer (`sightlines/render/multiplane.py`, `arrays.py`) sums halos in fixed-size
chunks inside a `lax.scan` over planes, so memory is a tunable constant independent of the halo
count. Empty slots are padded with finite zero-deflection values (zero padding gives NaN gradients).
It also has a ray-blocked trace (`make_blocked_trace`) and a batched trace over realisations.

## What to build

- Chunked halo summation in the multi-plane scan path, with the chunk size a parameter.
- Array packing from a realisation table to padded chunk arrays (`chunked_arrays_from`,
  `chunked_batch_from`), raising on overflow.
- The ray-blocked variant for sub-sampled grids.
- Decide in the plan step whether this replaces `traced_grids_via_scan` or sits beside it.

## Evidence it is validated

- Agrees with the PyAutoLens `Tracer`, the library scan path and lenstronomy to 1e-11 arcsec or
  better on the same realisation (`results/phase2a_render/`, `tests/test_render.py`: 20 tests,
  including chunk-size and padding invariance, gradients, `vmap` over realisations, 99 planes).
- One whole pyHalo realisation traced by lenstronomy and by the project agrees to 7.5e-15 arcsec.
- Speed: one A100 traces 206k rays through 12,700 halos in 1.6 s; laptop GPU 0.7 s per trace at
  10^6 M_sun, 99 planes, 101 x 101.
- float64 only; float32 sums over 10^4 halos are unchecked.

## Out of scope

The population samplers (separate prompts); image-plane diagnostics.

Witness: a PyAutoLens test traces one realisation of at least 5,000 halos on 99 planes through the chunked path and through `Tracer`, agreeing to 1e-9 arcsec, with results identical across two chunk sizes.

<!-- formalised by the Intake (Conception) Agent on 2026-11-26 from file:/home/jammy/Science/Science/scratch/dm_sightlines_phase6_prompts/2_render.md -->
