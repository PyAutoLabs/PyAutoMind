## likelihood-lifecycle-p5c3
- issue: https://github.com/PyAutoLabs/PyAutoLens/issues/885
- completed: 2026-11-24
- library-pr: https://github.com/PyAutoLabs/PyAutoGalaxy/pull/753
- library-pr: https://github.com/PyAutoLabs/PyAutoLens/pull/886
- epic: likelihood-lifecycle (phase 5C-3; next 5D PyAutoFit)

Phase 5C-3 shipped as two PRs under one issue. Together with 5B-3 (PyAutoArray#712), fits outside modeling can now get the optimal sparse operator when the lazy policy is on (default off until the R6 flip).

- **5C-3a, PyAutoGalaxy** (#753, merged 2026-11-24 as e357d1e1):
  - `AbstractFitInversion.sparse_operator` is a functools.cached_property that resolves `dataset.sparse_operator_for(xp, total_mappers > 0, settings)`. It is static under JAX because `register_instance_pytree` adds every cached_property to `no_flatten`.
  - The Galaxy `DatasetInterface` sites and the four interferometer helpers (an optional `sparse_operator=` argument) use it, so the inversion and the dirty-image correction share one operator.
  - `agg_util.dataset_with_setup_from` reapplies setup.json in `_imaging_from` / `_interferometer_from` (best-effort).
  - New `AnalysisSetupMixin`; `setup_util.setup_environment()` is public.
- **5C-3b, PyAutoLens** (#886, merged 2026-11-24 as d19108da):
  - Lens FitImaging / FitInterferometer pass `self.sparse_operator` at the `DatasetInterface` sites and to the helpers. `lens/to_inversion.py` is unchanged.
  - `AnalysisSetupNoOperator` is a thin subclass of the mixin.
  - The Lens aggregator inherits the reapply through Galaxy's loaders.
- **Gate:**
  - 5C-3a: 1659 Galaxy tests; Lens compatibility 1086 + 1 xfailed; Heart GREEN; smoke 5/5. autolens hit the parallel environment-build race and passed rerun alone, 42/42 + 2/2.
  - 5C-3b: 1101 + 1 xfailed, and the new tests fail without the change; Heart GREEN; smoke 4/4.
- **Traps:**
  - JAX pytree flattening of fits treats `cached_property` values as static via `cached_property_names`. Don't replace a cached property with a plain one for "pytree safety". The orchestrator wrongly did this once and reverted it.
  - When a parallel smoke autolens run fails with `ModuleNotFoundError` numpy/yaml, read the solo rerun's `test-results/*.json`. `smoke.log` keeps the failed run's content.
  - A canonical PyAutoFit checkout behind origin makes smoke test an older Fit, so fast-forward the clean canonical checkouts before smoke.
- **Open question raised by the human at merge (2026-11-24):** with lazy operators everywhere, what does the Analysis-level setup still own? See the epic ledger.

## Original prompt

# Likelihood lifecycle phase 5C-3: PyAutoGalaxy + PyAutoLens fit call sites for the lazy operator, aggregator reloads reapply `setup.json`, one shared setup-resolution path

Type: feature
Target: PyAutoLens
Repos:
- PyAutoGalaxy
- PyAutoLens
Themes:
- hpc-gpu
- profiling
Difficulty: large
Autonomy: supervised
Priority: medium
Status: active
Issued: 2026-11-24
Issue: https://github.com/PyAutoLabs/PyAutoLens/issues/885
Consequence: judge
Witness: The PyAutoGalaxy and PyAutoLens fits (`AbstractFit.sparse_operator`, `fit_imaging.py` / `fit_interferometer.py`, `lens/to_inversion.py`) pass `self.dataset.sparse_operator_for(xp, has_pixelization)` (5B-3) into `aa.DatasetInterface`, so a plain `al.FitImaging(dataset, tracer)` gets the lazy operator when the policy is on. Loading a fit from the aggregator (`al.agg.FitImagingAgg` / `FitInterferometerAgg` and their PyAutoGalaxy counterparts) for a search that wrote `files/setup.json` reapplies that setup to the reloaded dataset (`dataset.apply_setup`). So the reloaded fit takes the same operator route as the search, and its log likelihood matches the stored value to the search's tolerance. A search with no `setup.json` reloads exactly as before. The analysis's `modify_before_fit` resolution and the 5B-3 lazy factory path share one resolution helper rather than two copies. The full PyAutoGalaxy and PyAutoLens suites are green.
Review-minutes: 20
Unattended: no
Lane: any
Gate: 5B-3 MERGED (the lazy factory operator and policy switch in PyAutoArray). Phasing approved by the human 2026-11-24.
Epic: likelihood-lifecycle
Phase: 5
Parent: draft/research/autolens_profiling/likelihood_lifecycle_epic.md
Filed: 2026-11-24

## Context

- 5C writes `files/setup.json` (setup fields plus `chosen_by`) beside each search's output, but `autolens/aggregator/fit_imaging.py:91` / `fit_interferometer.py:92` rebuild fits from `dataset.fits` with no operator. A reload can therefore take a different route from the search (the routes differ by about 1e-4 relative) and run slowly with heavy memory on CPU.
- Setup resolution now lives in PyAutoGalaxy `autogalaxy/analysis/setup_util.py` / `AnalysisDataset.resolve_setup` (5C-1) and in the PyAutoLens point/weak setup mixin (5C-2). 5B-3 adds the factory-side resolution. 5C-3 makes them share one helper.

## Out of scope

- The lazy factory operator itself (5B-3).
- The JAX path.
- The default flip (R6).
- Workspace changes (5F).
