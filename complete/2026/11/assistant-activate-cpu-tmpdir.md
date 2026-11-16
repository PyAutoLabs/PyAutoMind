Shipped in autolens_assistant#186 (closes autolens_assistant#185) and autogalaxy_assistant#48, merged 2026-11-13 by the human's `/prm`.

`activate.sh` (the template every science project copies via `skills/start-new-project.md`), cluster branch:

- JAX pinned to the CPU on GPU-less jobs: `JAX_PLATFORMS=cpu` (one stderr line) only when it is unset and `SLURM_JOB_GPUS`, `SLURM_GPUS_ON_NODE` and `CUDA_VISIBLE_DEVICES` are all empty. The venv's CUDA plugin otherwise logs a cuInit ERROR + traceback in every CPU job (RAL probes 415320/415321). A `--gres=gpu` job always has all three set (RAL gpu probe 415323), so GPU runs are untouched.
- autolens template gains the TMPDIR-off-/tmp block the autogalaxy template already had (RAL admin, 2026-11-12); the two templates now agree apart from library names.

Outside the PRs, same day: the six live Science projects' `activate.sh` got the same CPU-pin + TMPDIR block (laptop and RAL, RAL originals kept as `activate.sh.bak-20261113`).

Tests: `bash -n`; stub-venv behaviour test (no-GPU, GPU, explicit JAX_PLATFORMS, laptop branch) on both templates and all six projects.

Shipped under the Heart RED development override (recorded on the issue, both PRs, active.md and autonomy_log.md 2026-11-13); Heart remains RED for release purposes.

## Original prompt

# Assistant activate.sh: pin JAX to CPU on GPU-less jobs; autolens keeps TMPDIR off /tmp

Targets: @autolens_assistant @autogalaxy_assistant
Type: bug
Filed: 2026-11-13
Issued: 2026-11-13
Issue: https://github.com/PyAutoLabs/autolens_assistant/issues/185
Consequence: judge

Verbatim user request (2026-11-13): "do all four" — item 4: add the JAX_PLATFORMS line to the projects and the template (plus the autolens template's missing TMPDIR block found on the way).

Tier: judge — merge mode: human /prm
