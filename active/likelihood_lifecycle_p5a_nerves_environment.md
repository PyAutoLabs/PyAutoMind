# Likelihood lifecycle phase 5A: PyAutoNerves environment probe, `PYAUTO_SETUP` honoured at import, and the x64 opt-out bug

Type: feature
Target: PyAutoNerves
Repos:
- PyAutoNerves
Themes:
- hpc-gpu
- profiling
Difficulty: medium
Autonomy: supervised
Priority: high
Status: active
Issued: 2026-11-23
Issue: https://github.com/PyAutoLabs/PyAutoNerves/issues/222
Consequence: judge
Witness: PyAutoNerves main carries `autonerves.environment.Environment.detect()` returning gpu, gpu_name, gpu_memory_gb, cores (SLURM_CPUS_PER_TASK, then sched_getaffinity, then cpu_count), ram_gb, numba, nufftax and a site hint, each branch covered by a unit test with the environment monkeypatched; `jax_wrapper` honours `PYAUTO_SETUP=auto|cpu|gpu|<setup_id>` at import (explicit cpu/numba intents set JAX_PLATFORMS=cpu and the *_NUM_THREADS variables before JAX initialises; `auto` and unset set nothing), checked by subprocess import tests; under `JAX_ENABLE_X64=False` (and `0`) importing autonerves leaves `jax.config.read("jax_enable_x64")` False while unset still forces x64 on, checked by a subprocess test; full test suite green
Review-minutes: 20
Unattended: ready
Lane: any
Gate: MET 2026-11-16 — human ruled phase 4 closed (gaps listed), approved report §3.4 and R6 = opt-in first (ledger line 2026-11-16). Ran after the wall-estimate bug, per the human — that bug is fixed (`complete/2026/11/validation-wall-estimates-miss-eval-count-and-sampler-floor.md`, autolens_inference#70, merged 2026-11-16).
Epic: likelihood-lifecycle
Phase: 5
Parent: draft/research/autolens_profiling/likelihood_lifecycle_epic.md
Filed: 2026-11-16

## Context

- Phase 5 (epic ledger): optimal setup baked into the source, library first: 5A PyAutoNerves → 5B PyAutoArray → 5C PyAutoGalaxy + PyAutoLens → 5D PyAutoFit → 5E estimator → 5F workspace/HowToLens → 5G assistant → 5H science projects. This prompt is **5A only**. One issue in PyAutoNerves.
- Design: report §3.5 (`draft/research/autolens_profiling/likelihood_lifecycle_epic_report.md`), the PyAutoNerves row:
  - `autonerves.environment.Environment.detect()` → gpu (bool), gpu_name, gpu_memory_gb, cores (SLURM_CPUS_PER_TASK → sched_getaffinity → cpu_count), ram_gb, numba, nufftax, site hint (SLURM_CLUSTER_NAME, hostname class).
  - `jax_wrapper` honours `PYAUTO_SETUP=auto|cpu|gpu|<setup_id>` at import: only explicit cpu/numba intents set `JAX_PLATFORMS=cpu` and the `*_NUM_THREADS` variables before JAX initialises; `auto` sets nothing at import (JAX picks the GPU when present).
- Boundary (report §3.4): auto decides backend, device, operator, precision, route, threads and default cores; it never touches the model, the sampler or the HPC request, and an explicit override (`PYAUTO_SETUP=<setup_id>`) always wins. 5A only detects and honours the override; it chooses nothing (choice is 5B `Setup.auto`).
- The x64 bug is adopted into 5A (ledger "Adopted": `draft/bug/autonerves/jax_enable_x64_env_ignored_and_fp32_leg_runs_fp64.md` → 5A). Root cause in `@PyAutoNerves/autonerves/jax_wrapper.py` (the `JAX_ENABLE_X64` block: an explicit `False` is overwritten with `True`). 5A fixes the Nerves root cause only; that draft's PyAutoFit `preflight.py` `X64_WARNING` text and the autofit_inference fp32 row check stay in that draft (narrow it when 5A merges). Ruling R4 (mixed precision `experimental` until the x64 bug is fixed) depends on this fix.
- Existing neighbours, read before designing: `@PyAutoNerves/autonerves/site_config.py` and `autonerves/site/ral.yaml` (site layer); the thread-pinning lessons in Brain memory (numba under Nautilus is one process per core; never prange inside multiprocessing workers; OMP does not cap numba).

## Plan

1. `autonerves/environment.py`: frozen dataclass `Environment` + `detect()`; no JAX import inside `detect()` beyond what is already initialised (GPU facts read lazily or via `jax.devices()` only when JAX is already imported; document which). Unit tests with monkeypatched env vars, affinity and missing optional packages.
2. `jax_wrapper.py`: read `PYAUTO_SETUP` before JAX initialises; implement the cpu/numba intents (`JAX_PLATFORMS=cpu`, thread variables set only when absent, never overwriting a user value); `auto`/unset is a no-op. Invalid values raise a clear error naming the allowed forms.
3. x64: respect an explicit `JAX_ENABLE_X64=False|0`; keep forcing x64 on when unset; update the log message to match.
4. Docs: docstrings only (workspace prose is 5F). Changelog/pending-release note per ship_library.
5. Ship via ship_library to an open PR (pending-release). Stop at PR-open; merge is the human's `/prm`.

## Out of scope

`aa.Setup`, `Setup.auto`, the rule table and `apply_setup` (5B); `setup="auto"`, banner and `setup.json` (5C); `number_of_cores="auto"` (5D); the estimator (5E). No compute; no RAL.
