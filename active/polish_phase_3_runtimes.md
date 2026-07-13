# polish phase 3 — PreOptimizationTimes runtime campaign

Type: maintenance
Target: autolens_profiling
Difficulty: large
Autonomy: supervised
Priority: normal
Status: formalised

Phase 3 of 4 of `polish.md` (see parent for full intent). Depends on phase 2
(vram validated; vmap batch sizes computed).

Run the full `likelihood_runtime` campaign to establish the
**PreOptimizationTimes** baseline — the last profiling before the optimization
and speed-up work, so these are the run times everything after is compared to.

Matrix:
- **Instruments** — all instrument types per dataset kind: imaging (AO, JWST,
  HST), interferometer, datacube. No point_source.
- **Modes** — vmap only, using the batch sizes computed by the vram package in
  phase 2. For imaging also do the whole sparse vs mapping comparison, making
  sure it runs through packages like vram.
- **Platforms** — laptop CPU, HPC CPU, HPC A100; A100 mixed-precision profiling
  wherever the source code supports it. **Do not run laptop GPU** — the user
  runs those in a follow-up prompt when the laptop is free.

Save all results per the phase-1 conventions (`.json` + `.md`, displayed in the
per-package GitHub `.md` files), tagged PreOptimizationTimes.

No searches — this campaign profiles likelihood functions only.
