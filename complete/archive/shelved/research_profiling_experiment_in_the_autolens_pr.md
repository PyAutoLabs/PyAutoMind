# Research profiling experiment in the autolens_profiling repo (group4 MGE search benchmark) — SUPERSEDED 2026-08-18

> **SUPERSEDED / SHELVED 2026-08-18.** Removed from the registry (was
> `parked.md :: group4-mge-search-benchmark`, issue
> [autolens_profiling#82](https://github.com/PyAutoLabs/autolens_profiling/issues/82))
> — superseded by the 2026-08-17 human-approved inference-methods programme
> (`active/inference_programme_ledger.md`, autolens_profiling#134), which now
> owns sampler-benchmark direction. The first half already SHIPPED (code + first
> GPU results merged as autolens_profiling#83); the remaining gradient-family
> sweep is not carried forward as scoped here.
>
> **Preserved parked context (from the deleted `parked.md` entry):** parked
> 2026-07-24 — code + first GPU results MERGED (PR #83), worktree/claim RELEASED.
> *Remaining at park time:* gradient-family sweep
> (prodigy / lion / adabelief / prodigy_autoconv) + Nautilus anchor on the laptop
> GPU (`~/venv/PyAutoGPU`, `JAX_PLATFORM_NAME=cuda JAX_PLATFORMS=cuda,cpu
> XLA_PYTHON_CLIENT_MEM_FRACTION=0.5`, `--config-name local_gpu_fp64`), then
> recovery/walltime aggregation. Warm output preserved in the main checkout under
> `output/searches/`. *Paths (post scripts/<dataset>/<task>/ restructure,
> autolens_profiling#84):* group4 cells live at
> `scripts/cluster/searches/<sampler>/mge.py` (samplers: `multi_start_prodigy`,
> `multi_start_lion`, `multi_start_adabelief`, `multi_start_prodigy_autoconv`,
> `nautilus`); run via the sweep driver `scripts/misc/searches/sweep.py`
> (e.g. `--only <sampler>/group/mge` — the sweep still keys the group cell class
> internally, mapping it to `scripts/cluster/` on disk). If compile is too heavy:
> dial `_GROUP4_MGE_TOTAL_GAUSSIANS` 10->6 and/or `_MULTI_START_N_STARTS` 64->32.


Type: research
Target: workspaces
Repos:
- autolens_profiling
Difficulty: hard
Autonomy: safe
Priority: normal
Status: formalised

Research profiling experiment in the autolens_profiling repo. We currently have autolens_profiling examples that run JAX gradient max-likelihood optimizers on a single lens galaxy with a single MGE source. Extend this to a much higher-dimensional, harder model: 4 lens galaxies + 4 source galaxies. Write a simulator.py that generates the dataset from known input truth, then run the existing JAX gradient optimizers (max-likelihood samplers) alongside Nautilus and record whether any of them scale to this dimensionality and recover the input truth. If none of the optimizers succeed, investigate more careful initialization strategies. This is an exploratory benchmark, not a library change.

<!-- formalised by the Intake (Conception) Agent on 2026-07-21 from user-intake -->
