# hpc-keep-off-home (phase A): keep HPC temp files and caches off $HOME and worker /tmp

- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1767 (closed 2026-11-12)
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1768
- workspace-pr: https://github.com/PyAutoLabs/autofit_assistant/pull/63
- workspace-pr: https://github.com/PyAutoLabs/autofit_inference/pull/19
- workspace-pr: https://github.com/PyAutoLabs/autogalaxy_assistant/pull/46
- workspace-pr: https://github.com/PyAutoLabs/autolens_inference/pull/65
- workspace-pr: https://github.com/PyAutoLabs/autocti_assistant/pull/40
- tier: glance, auto-merged on green 2026-11-12 (human-approved plan); Heart YELLOW acknowledged by the human at ship (PyAutoArray open PR 8d old)

## Why
The RAL admin warned on 2026-11-12 (repeating 2026-09-25) that worker nodes were crashing: tools wrote caches and temp files to `~` and `/tmp`, which on compute nodes sit on a tiny local OS disk (compute nodes don't mount the login node's `/home`; Slurm `TmpFS=/tmp`). The human installed `~/.bashrc.d/keep_off_home.sh` on the RAL login node the same day, covering every job submitted with sbatch's default `--export=ALL`. This task covers the repos, for jobs submitted with a restricted `--export`.

## What shipped
- **PyAutoFit#1768:** optional top-level `cache_root:` in `campaign.yaml` (absolute path, validated). `Campaign.cache_root` → `SubmitRequest.cache_root` → `sbatch_script` emits fill-if-unset exports of `TMPDIR` (`tmp/`), `XDG_CACHE_HOME` (`.cache/`), pip/matplotlib/numba/CUDA/Triton/astropy caches, plus `JAX_COMPILATION_CACHE_DIR` via `${VAR-...}` so an empty value still disables it. They sit after `set -euo pipefail` and before the stage env, so stage env wins. Paths are escaped for a double-quoted context. Without `cache_root:` the script is byte-identical. 4 new tests; full suite 4288 passed.
- **activate.sh** in autofit_assistant, autofit_inference, autogalaxy_assistant and autolens_inference: fill-if-unset `TMPDIR="$(dirname "$PYAUTO_HPC_CACHE")/tmp"` + mkdir after the existing cache block. autocti_assistant's HPC branch had no redirection at all and now has the full block plus TMPDIR. Verified by sourcing each under `env -i` with a fake `PYAUTO_HPC_BASE`.

## Not done
- **Phase B (blocked):** the same TMPDIR line in autofit_profiling, autolens_assistant, autolens_profiling and euclid_strong_lens_modeling_pipeline (claimed by nautilus-spawn-training-pool, results-library-p5a-assistant, gradient-correctness-sweep, sky-orientation-p2). Re-filed as `draft/maintenance/workspaces/hpc_keep_temp_off_home_phase_b.md` and listed in `planned.md`.
- **Out of scope:** `collaborator/development/autolens_profiling` submits (local repo, no remote) and euclid_dr1 `submit_docs_tar` hard-code worker `/tmp`.
- **To opt in:** campaigns add `cache_root: /mnt/ral/jnightin` once PyAutoFit is released.

## Original prompt

# Keep HPC temp files and caches off $HOME and the worker's /tmp

Type: maintenance
Target: PyAutoFit
Repos:
- PyAutoFit
- autofit_assistant
- autofit_inference
- autofit_profiling
- autogalaxy_assistant
- autolens_assistant
- autolens_inference
- autolens_profiling
- euclid_strong_lens_modeling_pipeline
- autocti_assistant
Difficulty: small
Autonomy: supervised
Priority: high
Status: formalised
Consequence: glance
Witness: every RAL-capable activate.sh fills an unset TMPDIR (and autocti_assistant's HPC branch the full cache block) with a directory beside PYAUTO_HPC_CACHE on the shared disk; a job script from PyAutoFit's Slurm scheduler exports fill-if-unset TMPDIR/XDG_CACHE_HOME when a cache root is configured, with tests; nothing writes to ~ or /tmp on a worker by default.
Review-minutes: 5
Filed: 2026-11-12
Issued: 2026-11-12
Issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1767

## Request (verbatim, RAL admin 2026-11-12)

> I'd like to remind all users that if they use VSCode, Claude, and various Python local
> tools that they need do define their ENV vars to preclude use of /home/USERNAME when
> running these through Slurm. Point all temp/cache env vars to the shared disk instead.
> The worker nodes have tiny OS disks, and I'm finding multiple nodes crashing due to
> "out of space" errors caused by the aforementioned utilities dumping data into
> ~/.cache, ~/.vscode, ~/copilot, ~/.claude, etc.

Human: "make sure true for all places we interact with RAL".

## What is already done

- RAL login node: `~/.bashrc.d/keep_off_home.sh` (installed 2026-11-12) fills unset
  TMPDIR, XDG_*, pip/matplotlib/numba/CUDA/Triton/astropy/HF/JAX caches,
  CLAUDE_CONFIG_DIR, VSCODE_AGENT_FOLDER and COPILOT_HOME under /mnt/ral/jnightin. Jobs
  inherit it through sbatch's default `--export=ALL`. Jobs submitted with a restricted
  `--export=VAR=...` do NOT, so the repos must still cover it themselves.
- Facts: compute nodes do not mount the login node's /home; Slurm `TmpFS=/tmp` is on the
  tiny OS disk.
- 8 activate.sh files already redirect caches to `$PYAUTO_HPC_CACHE` (added after the
  2026-09-25 warning) but none set TMPDIR.

## Scope

1. In the HPC branch of each RAL-capable activate.sh (autofit_assistant, autofit_inference,
   autofit_profiling, autogalaxy_assistant, autolens_assistant, autolens_inference,
   autolens_profiling, euclid_strong_lens_modeling_pipeline), add a fill-if-unset
   `TMPDIR` next to the PYAUTO_HPC_CACHE block (a `tmp/` beside `.cache/`, `mkdir -p ||
   true`). Keep the blocks identical across repos.
2. cti/autocti_assistant/activate.sh: its PYAUTO_HPC_BASE branch has no redirection;
   add the same full cache + TMPDIR block.
3. PyAutoFit `autofit/campaign/scheduler/slurm.py`: generated job scripts source no
   activate.sh and set no cache env. Emit fill-if-unset exports (TMPDIR, XDG_CACHE_HOME,
   and the cache vars) when the site/request names a cache root, and cover it in
   `test_autofit/campaign/test_slurm.py`.

## Out of scope (not PR-able)

- `collaborator/development/autolens_profiling` (local git repo, no remote): ~10 submits in
  hpc/batch_{cpu,gpu}/ hard-code worker /tmp. Fix by local edit if they are ever re-run.
- Science euclid_dr1 `hpc/run_manifests/eclipse_r2_add_unmodelled_20261030/submit_docs_tar`
  writes a tar to worker /tmp; a completed one-off run.
