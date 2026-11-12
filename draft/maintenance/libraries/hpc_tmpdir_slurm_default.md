# Treat Slurm's default TMPDIR=/tmp as unset in activate.sh and campaign job scripts

Type: maintenance
Target: PyAutoFit
Repos:
- PyAutoFit
- autofit_assistant
- autofit_inference
- autogalaxy_assistant
- autolens_inference
- autocti_assistant
Difficulty: small
Autonomy: supervised
Priority: high
Status: formalised
Consequence: glance
Witness: a job with `--export=NONE` that sources a fixed activate.sh (or runs a PyAutoFit cache_root script) gets TMPDIR on the shared disk, not /tmp; a TMPDIR set to anything other than /tmp still wins; tests cover the /tmp case.
Review-minutes: 3
Filed: 2026-11-12

Follow-up to `complete/2026/11/hpc-keep-off-home.md` (PyAutoFit#1767). Live probe jobs
415133/415134 on euclid-ral-compute-1: with `--export=NONE,...` + `source activate.sh` the
caches were right but TMPDIR=/tmp, because Slurm sets TMPDIR to its TmpFS (`/tmp`) when
the submit environment has none, so phase A's `${TMPDIR:-...}` never fires.

Human (2026-11-12): "fix the TMPDIR=/tmp gap now too".

Fix: treat TMPDIR that is unset, empty or exactly `/tmp` as unset —
- the TMPDIR block in the five phase-A activate.sh files;
- PyAutoFit `autofit/campaign/scheduler/slurm.py` `_cache_exports`, with a test for the
  `/tmp` case.
The four claimed repos stay in `draft/maintenance/workspaces/hpc_keep_temp_off_home_phase_b.md`.
