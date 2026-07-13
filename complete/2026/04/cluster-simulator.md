## cluster-simulator
- issue: https://github.com/PyAutoLabs/PyAutoLens/issues/464
- completed: 2026-04-20
- library-pr: https://github.com/PyAutoLabs/PyAutoLens/pull/465
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace/pull/77
- notes: Added optional `redshift` to `PointDataset` with CSV round-trip and per-source validation (library). Rewrote `autolens_workspace/scripts/cluster/simulator.py` as a 5-member cluster with standalone `NFWMCRLudlowSph` halo (`mass_at_200=10^15.3`) and 2 sources at z=1.0 producing 3 images each, writing a combined `point_datasets.csv` as the canonical hand-editable cluster input. Removed `cluster/simulator` from `no_run.yaml`. Follow-up prompts written: `admin_jammy/prompt/cluster/1_visualization.md` (cluster-scale viz prototype) and `2_csv_model_redshift.md` (pipe `PointDataset.redshift` into `af.Model(al.Galaxy, redshift=...)`). `modeling.py` and `start_here.py` remain parked in `no_run.yaml` — rewrite deferred until those two follow-ups land.
