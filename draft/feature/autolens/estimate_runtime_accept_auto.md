# `al.estimate_runtime` accepts `setup="auto"` and `number_of_cores="auto"`, and says "no estimate" instead of returning None for unmatched setups

Type: feature
Target: PyAutoLens
Repos:
- PyAutoLens
Themes:
- hpc-gpu
- profiling
Difficulty: small
Autonomy: supervised
Priority: medium
Status: draft
Consequence: judge
Witness: `al.estimate_runtime(dataset, model, search, setup="auto", number_of_cores="auto")` resolves the setup via `aa.Setup.auto` (with the dataset and model rule key, as the analyses do) and the cores via PyAutoFit's resolution (detected cores; 1 for JAX), then returns an estimate. A setup with no profiling row (e.g. `numba_cpu_dense_fp64`) returns an estimate whose `line()` says "no estimate for <setup_id> (no profiling cell)" rather than None. The guide `autolens_workspace/scripts/guides/advanced/auto_setup.py` and HowToLens `tutorial_need_for_speed.py` can then show the simpler call. Tests.
Review-minutes: 15
Unattended: no
Lane: any
Filed: 2026-11-25
Epic: likelihood-lifecycle
Parent: draft/research/autolens_profiling/likelihood_lifecycle_epic.md

## Context

Found by the 5F PR3 worker. Today `estimate_runtime` raises "'auto' is a device intent, not a setup_id" for `setup="auto"` and needs an integer `number_of_cores`, so tutorials pass a concrete setup_id and 1. Also note for prose: the wall model charges FLOOR_S = 0.014 s per evaluation (Nautilus sampler overhead, ported from autolens_inference wall/model.py), which dominates for very fast GPU likelihoods. A 0.2 ms/eval GPU cell therefore still estimates ~32 min for 1.3e5 evals. That is by design; it is not a bug.
