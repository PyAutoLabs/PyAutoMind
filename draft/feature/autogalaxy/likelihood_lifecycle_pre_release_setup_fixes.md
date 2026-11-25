# Likelihood lifecycle pre-release fixes: four rough edges in the automatic compute setup, before the release that ships it

Type: feature
Target: PyAutoGalaxy
Repos:
- PyAutoFit
- PyAutoGalaxy
- PyAutoLens
Themes:
- hpc-gpu
Difficulty: medium
Autonomy: supervised
Priority: high
Status: draft
Consequence: judge
Witness: All four fixes are merged on library main before the next release.
1. With `analysis = al.AnalysisImaging(dataset, setup="auto")`, calling `analysis.print_vram_use(model=model, batch_size=...)` (or any pre-fit likelihood use) before `search.fit` resolves the setup on demand from that model: the banner prints once and the call proceeds. Where it can't (no model available), it raises a clear error saying the setup resolves when the fit starts, instead of the PyAutoLens `SetupException` that blames factor graphs. HowToLens `chapter_2_lens_modeling/tutorial_2_practicalities.py` runs in test mode with `setup="auto"` added (local check only, no HowToLens PR needed).
2. `al.estimate_runtime(dataset, model, search, setup="auto", number_of_cores="auto")` works. The setup resolves via `aa.Setup.auto` with the same dataset/model rule key the analyses use; the cores resolve via PyAutoFit's resolution (detected cores; 1 for JAX). A setup with no profiling row (e.g. `numba_cpu_dense_fp64`) returns an estimate whose `line()` says "no estimate for <setup_id> (no profiling cell)" instead of `None`.
3. With `PYAUTO_DISABLE_JAX=1` (or JAX not installed) and a setup resolving to a JAX designation, the `Setup:` line reports what actually runs, e.g. `Setup:    numpy · CPU · dense · fp64   (rule imaging/mge · designated JAX; JAX disabled)`, and the `Parallel:` line agrees.
4. `ModelAnalysis` (PyAutoFit `autofit/non_linear/analysis/model_analysis.py`, created by `analysis.with_model(...)`) forwards `modify_before_fit` (and returns the wrapper with its inner analysis rebound if the inner call returns a new object), so `setup="auto"` resolves for analyses wrapped this way, including inside factor graphs.

Tests cover each fix. The PyAutoFit, PyAutoGalaxy and PyAutoLens suites are green, and `pyauto-heart smoke --affected-by PyAutoFit` passes.
Review-minutes: 25
Unattended: no
Lane: any
Gate: likelihood-lifecycle 5A–5E and the setup banner MERGED (PyAutoNerves#223/#224, PyAutoArray#709/#710/#712/#713, PyAutoFit#1795/#1796/#1797, PyAutoGalaxy#752/#753/#755, PyAutoLens#882/#886/#888/#889). Must land before the release that carries them. The workspace PRs autolens_workspace#689/#690, HowToLens#139, autolens_assistant#192 and euclid_strong_lens_modeling_pipeline#142 wait for that release.
Epic: likelihood-lifecycle
Phase: 5
Parent: draft/research/autolens_profiling/likelihood_lifecycle_epic.md
Filed: 2026-11-25
Supersedes:
- draft/bug/autogalaxy/setup_auto_unresolved_before_fit_print_vram_use.md
- draft/feature/autolens/estimate_runtime_accept_auto.md
- draft/bug/autogalaxy/setup_banner_shows_jax_under_disable_jax.md

## Context

This is one task with up to three PRs (PyAutoFit, PyAutoGalaxy, PyAutoLens). Give them the **same branch name**, because library CI clones dependency repos at a matching branch name, otherwise main. Merge order: Fit → Galaxy → Lens.

- **Fix 1** (PyAutoGalaxy + PyAutoLens):
  - The setup resolves in `modify_before_fit` via `AnalysisSetupMixin.resolve_setup(model)` (PyAutoGalaxy `autogalaxy/analysis/analysis/setup.py`).
  - PyAutoLens `raise_if_setup_unresolved` (`autolens/analysis/analysis/setup.py`) guards each `log_likelihood_function` with a factor-graph message.
  - `print_vram_use` evaluates the likelihood before the fit.
  - Options: make `resolve_setup(model)` safe to call early and idempotent (no double banner when `modify_before_fit` later runs), call it from `print_vram_use(model=...)` when unresolved, and reword the guard to cover "used before the fit started" as well as factor graphs.
- **Fix 2** (PyAutoLens): `autolens/analysis/runtime_estimate.py` `estimate_runtime(...)` currently raises "'auto' is a device intent, not a setup_id" and needs an int `number_of_cores`.
  - Reuse the setup key logic (`setup_util.setup_key_and_note_from` in PyAutoGalaxy) and PyAutoFit `autofit/non_linear/parallel/pool.py` `resolve_number_of_cores`.
  - Note for prose (not a bug): the wall model's FLOOR_S = 0.014 s/eval dominates very fast GPU likelihoods.
- **Fix 3** (PyAutoGalaxy): `autogalaxy/analysis/setup_util.py` `setup_banner_from` prints the designated backend, although `use_jax_from` falls back to numpy. Found under the workspace smoke profile (`PYAUTO_DISABLE_JAX=1`).
- **Fix 4** (PyAutoFit):
  - `ModelAnalysis` has no `modify_before_fit` today (only `__init__`, `gradient_mode`, `__getattr__`). `__getattr__` may forward it implicitly, but the return value would then be the inner analysis, not the wrapper. Verify and fix.
  - See how 5D's `AnalysisFactor.modify_before_fit` / `rebind_analysis` handles the same wrapper problem (`autofit/graphical/declarative/factor/analysis.py`).
- **Running scripts:** prefix every script run with `MPLBACKEND=Agg` (the default qtagg backend pops windows on the human's desktop). Generate notebooks only from inside a workspace repo directory, never from a task-root folder.
- **Shipping:** ship_library with the `pending-release` label. When it merges, retire the three superseded drafts listed in the header (one record).

## Out of scope

- The R6 default flip and `use_jax` sweep.
- Workspace and assistant docs (already written in the open 5F/5G PRs; a later docs pass can switch them to the simpler calls).
- The double-source-plane visualizer and sensitivity-script bugs.
