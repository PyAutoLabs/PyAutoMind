# `setup="auto"` analyses raise a misleading SetupException when used before `search.fit` (e.g. `analysis.print_vram_use`)

Type: bug
Target: PyAutoGalaxy
Repos:
- PyAutoGalaxy
- PyAutoLens
Themes:
- hpc-gpu
Difficulty: small
Autonomy: supervised
Priority: medium
Status: draft
Consequence: judge
Witness: With `analysis = al.AnalysisImaging(dataset, setup="auto")`, calling `analysis.print_vram_use(model=model, batch_size=...)` (or any pre-fit use that evaluates the likelihood) before `search.fit` either resolves the setup on demand (preferred: resolve with the given model, log the banner once, then proceed) or raises a clear error saying the setup resolves when the fit starts and how to resolve it early. The message no longer blames factor graphs. HowToLens `chapter_2_lens_modeling/tutorial_2_practicalities.py` runs with `setup="auto"` in test mode. There are tests for the pre-fit path.
Review-minutes: 15
Unattended: no
Lane: any
Filed: 2026-11-25
Epic: likelihood-lifecycle
Parent: draft/research/autolens_profiling/likelihood_lifecycle_epic.md

## Context

Found by the 5F PR3 worker (issue autolens_workspace#688). The setup is resolved in `modify_before_fit` (PyAutoGalaxy `autogalaxy/analysis/analysis/setup.py` `AnalysisSetupMixin.resolve_setup`). PyAutoLens `raise_if_setup_unresolved` (`autolens/analysis/analysis/setup.py`) guards every `log_likelihood_function` and says setups are not supported inside factor graphs. A pre-fit `print_vram_use` call evaluates the likelihood, trips the guard, and gets the factor-graph message. HowToLens tutorial 2 makes exactly this call, which is why it still runs without a setup. Option: give the mixin a public `resolve_setup(model)` users can call early, and have `print_vram_use(model=...)` call it when the setup is unresolved; reword the guard message to cover "used before the fit started".
