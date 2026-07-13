# polish phase 4 — likelihood breakdown and README dashboard

Type: maintenance
Target: autolens_profiling
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: formalised

Phase 4 of 4 of `polish.md` (see parent for full intent). Depends on phase 3
(PreOptimizationTimes runtime results in).

Two deliverables:

1. **likelihood_breakdown** — per-step decomposition for one representative
   config per dataset kind: HST for imaging, Alma_high for interferometer, and
   datacube. Same platforms as phase 3 (laptop CPU, HPC CPU, HPC A100 + mixed
   precision where supported); results saved per the phase-1 conventions and
   tagged PreOptimizationTimes.

2. **README dashboard** — populate the high-level dashboard designed in phase 1
   on the GitHub README, showing all key PreOptimizationTimes results at a
   glance, with links down into the per-package `.md` result pages.

Out of scope: searches; point_source; laptop GPU (user follow-up); the future
PyAutoBrain profiling agent (separate `feature/pyautobrain/` prompt when its
time comes).
