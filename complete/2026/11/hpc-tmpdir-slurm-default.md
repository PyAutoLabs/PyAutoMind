# hpc-tmpdir-slurm-default: treat Slurm's default TMPDIR=/tmp as unset

- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1769 (closed 2026-11-12)
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1771
- workspace-pr: https://github.com/PyAutoLabs/autofit_assistant/pull/64
- workspace-pr: https://github.com/PyAutoLabs/autofit_inference/pull/20
- workspace-pr: https://github.com/PyAutoLabs/autogalaxy_assistant/pull/47
- workspace-pr: https://github.com/PyAutoLabs/autolens_inference/pull/66
- workspace-pr: https://github.com/PyAutoLabs/autocti_assistant/pull/41
- shipped and merged under a Heart RED development override (live human: "Override, ship + merge", then an explicit "Yes, merge when green" in a later turn after the first grant lapsed); recorded on the issue, PR bodies and autonomy_log first table (`red-override`). No glance shadow row: not a tiered auto-merge.

## Why
Follow-up to `complete/2026/11/hpc-keep-off-home.md`. Live probe jobs 415133/415134 on euclid-ral-compute-1: a default-export job got every variable right, but a `--export=NONE` job that sourced `activate.sh` got `TMPDIR=/tmp`, because Slurm sets `TMPDIR` to its TmpFS when the submit environment has none, so `${TMPDIR:-...}` never fired.

## What shipped
- PyAutoFit `_cache_exports`: `if [ -z "${TMPDIR:-}" ] || [ "$TMPDIR" = /tmp ]; then export TMPDIR="<cache_root>/tmp"; fi`; test covers unset, `/tmp` and `/scratch`. Full suite 4288 passed.
- `activate.sh` in autofit_assistant, autofit_inference, autogalaxy_assistant, autolens_inference, autocti_assistant: same rule. Verified under `env -i` + `set -u` for the three cases.

## Not done
- The four claimed repos (autofit_profiling, autolens_assistant, autolens_profiling, euclid_strong_lens_modeling_pipeline): phase B draft `draft/maintenance/workspaces/hpc_keep_temp_off_home_phase_b.md`; copy the now-merged `if` block from autofit_assistant/activate.sh.
- Not re-probed on RAL after merge (the RAL checkouts pick these up on their next sync).

## Original prompt

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
Issued: 2026-11-12
Issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1769

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
