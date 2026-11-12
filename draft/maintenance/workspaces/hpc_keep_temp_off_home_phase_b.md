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
Witness: each repo's activate.sh HPC branch replaces an unset OR Slurm-default (`/tmp`) TMPDIR with `$(dirname "$PYAUTO_HPC_CACHE")/tmp` (mkdir'd), with text identical to phase A; a preset TMPDIR wins (checked by sourcing under env -i with a fake PYAUTO_HPC_BASE).
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

## Added 2026-11-12: Slurm's own TMPDIR=/tmp defeats fill-if-unset (found by a live probe)

Probe jobs 415133/415134 on euclid-ral-compute-1: with the default `--export=ALL` every
variable is right (the RAL login drop-in propagates). With `--export=NONE,...` plus
`source activate.sh`, caches were right but **TMPDIR=/tmp**: Slurm sets `TMPDIR` to its
`TmpFS` (`/tmp`) when the submit environment has none, so phase A's
`${TMPDIR:-...}` never fires. Fix everywhere phase A put TMPDIR (the five phase-A
activate.sh files plus PyAutoFit `autofit/campaign/scheduler/slurm.py` `_cache_exports`)
and in the four phase-B repos: treat `TMPDIR` that is unset, empty or exactly `/tmp` as
unset, e.g.
`if [ -z "${TMPDIR:-}" ] || [ "$TMPDIR" = /tmp ]; then export TMPDIR=".../tmp"; fi`.
Add a PyAutoFit test for the `/tmp` case. Note: `/tmp` on compute-1 is a 5.3 TB disk
(5.0 TB free), so this is lower urgency than the `$HOME` caches, which are fixed.

## Update 2026-11-12: phase-A repos and PyAutoFit DONE

`complete/2026/11/hpc-tmpdir-slurm-default.md` (PyAutoFit#1769) shipped the `/tmp`-as-unset
rule to PyAutoFit and the five phase-A activate.sh files. What remains here is only the four
claimed repos: copy the `if [ -z "${TMPDIR:-}" ] || [ "$TMPDIR" = /tmp ]` block from
autofit_assistant/activate.sh. Drop PyAutoFit and the five phase-A repos from `Repos:`.
