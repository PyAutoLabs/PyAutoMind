## stale-auto-simulated-cluster-dataset
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/445
- completed: 2026-11-24
- workspace-pr: https://github.com/PyAutoLabs/autolens_profiling/pull/532
- The simple-cluster cache gate (`dataset/cluster/simple`) now requires `scaling_galaxies.csv` and deserializes the saved tracer with the installed PyAutoLens before reuse; a stale directory raises an error naming the offending file (`scaling_galaxies.csv` or `tracer.json`) and how to regenerate it. Covers both cluster profiling cells and the robust-settings sweep.
- Validation: reproduced on main 9b4a6452 with the legacy dataset (old `rs` keyword); witness on branch rejected stale, accepted a fresh `scripts/misc/simulators/cluster.py` output; regression test + ruff; cluster import smokes; independent Opus review CLEAN; scoped Heart GREEN.
- Merge waited on autolens_profiling#534 (xla census anchors after the convolver move) fixing main lint; merged by human /prm after a branch update from main only.

## Original prompt

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
Lane: any
Verified: 2026-11-24 9b4a6452 (autolens_profiling)

## Why

Found during PyAutoLens#799. The local gitignored `dataset/cluster/simple` (written 2026-05-16) has no `scaling_galaxies.csv`. Its `tracer.json` uses the old `dPIEMassSph(rs=, b0=, ra=)` signature, so it no longer deserialises.

The current simulator (`scripts/misc/simulators/cluster.py`) writes `dPIEMassB0Sph` and `scaling_galaxies.csv`. But `_profile_cli.auto_simulate_if_missing` gates only on `al.util.dataset.should_simulate`, which checks existence, so a stale dataset is never refreshed. The #799 worker had to rebuild the CSV in a scratch copy and bypass `simple_truth_gate`.

## Deliverables

1. Detect a stale auto-simulated dataset. Options:
   - record the simulator sha256 (already computed in `scripts/cluster/image_plane/_datasets.py`) in a marker file beside the dataset, and re-simulate on mismatch;
   - or check for the required files.
2. Either regenerate or fail loudly; never silently use a stale truth.
3. Keep the shared helper general (it serves every `dataset_type`), and coordinate with the point-source regime draft named in `Related:`.
