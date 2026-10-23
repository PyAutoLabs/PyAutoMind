# `@autolens_profiling` stale auto-simulated `dataset/cluster/simple` is never regenerated

Type: bug
Target: autolens_profiling
Repos:
- @autolens_profiling
Themes:
- cluster
- profiling
- datasets
Difficulty: small
Autonomy: supervised
Priority: low
Status: formalised
Consequence: glance
Witness: with a local `dataset/cluster/simple` written by an older simulator, the cluster cell regenerates it (or fails loudly naming the stale file), and the regenerated dataset contains `scaling_galaxies.csv` and a `tracer.json` that loads with current PyAutoLens.
Filed: 2026-10-23
Issue: https://github.com/PyAutoLabs/autolens_profiling/issues/445
Related: `draft/bug/pyautolens/point_source_json_datasets_record_no_regime.md` (the same `should_simulate` existence-only gate)

## Why

Found during PyAutoLens#799. The local gitignored `dataset/cluster/simple` (written 2026-05-16) has no `scaling_galaxies.csv`. Its `tracer.json` uses the old `dPIEMassSph(rs=, b0=, ra=)` signature, so it no longer deserialises.

The current simulator (`scripts/misc/simulators/cluster.py`) writes `dPIEMassB0Sph` and `scaling_galaxies.csv`. But `_profile_cli.auto_simulate_if_missing` gates only on `al.util.dataset.should_simulate`, which checks existence, so a stale dataset is never refreshed. The #799 worker had to rebuild the CSV in a scratch copy and bypass `simple_truth_gate`.

## Deliverables

1. Detect a stale auto-simulated dataset. Options:
   - record the simulator sha256 (already computed in `scripts/cluster/image_plane/_datasets.py`) in a marker file beside the dataset, and re-simulate on mismatch;
   - or check for the required files.
2. Either regenerate or fail loudly; never silently use a stale truth.
3. Keep the shared helper general (it serves every `dataset_type`), and coordinate with the point-source regime draft named in `Related:`.
