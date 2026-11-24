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
