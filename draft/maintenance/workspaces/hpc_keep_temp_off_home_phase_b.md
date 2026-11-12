# Phase B: send HPC temp files to the shared disk (TMPDIR) in the four remaining activate.sh

Type: maintenance
Target: workspaces
Repos:
- autofit_profiling
- autolens_assistant
- autolens_profiling
- euclid_strong_lens_modeling_pipeline
Difficulty: small
Autonomy: supervised
Priority: high
Status: formalised
Consequence: glance
Witness: each repo's activate.sh HPC branch fills an unset TMPDIR with `$(dirname "$PYAUTO_HPC_CACHE")/tmp` (mkdir'd), with text identical to phase A; a preset TMPDIR wins (checked by sourcing under env -i with a fake PYAUTO_HPC_BASE).
Review-minutes: 3
Filed: 2026-11-12

Phase A shipped 2026-11-12 (record `complete/2026/11/hpc-keep-off-home.md`, PyAutoFit#1767):
PyAutoFit campaign `cache_root:` plus TMPDIR in five workspace activate.sh files. These four repos
were claimed by other tasks at the time (nautilus-spawn-training-pool,
results-library-p5a-assistant, gradient-correctness-sweep, sky-orientation-p2).

Copy the five-line TMPDIR block from autofit_assistant/activate.sh (directly after the
`ASTROPY_CACHE_DIR` export) into each repo's PYAUTO_HPC_CACHE block. Why: on RAL compute
nodes `/tmp` sits on a tiny local OS disk that tools filled, crashing nodes (RAL admin,
2026-11-12).
