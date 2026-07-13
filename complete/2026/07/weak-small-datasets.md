## weak-small-datasets
- issue: https://github.com/PyAutoLabs/PyAutoLens/issues/583
- completed: 2026-07-09
- autoarray-pr: https://github.com/PyAutoLabs/PyAutoArray/pull/366 (merged)
- autolens-pr: https://github.com/PyAutoLabs/PyAutoLens/pull/584 (merged)
- notes: Step 9 of the weak series (--auto supervised, same-session). SMALL_DATASETS_N_CATALOGUE=25 + cap_catalogue_size_for_small_datasets in autoarray dataset_util (centralised beside pixel caps, reusable for point catalogues); SimulatorShearYX.via_tracer_random_positions_from consumes it (explicit-grid via_tracer_from never mutated — tested invariant). modeling.py smoke run: 25 galaxies, ~30s vs ~7min. CI GOTCHA: PyAutoLens PR CI failed both legs on first run — the dependency-branch checkout did NOT pick up the same-named PyAutoArray branch (AttributeError on the new helper); resolution = merge autoarray first, then re-run the autolens PR workflows via gh api runs/<id>/rerun — green. Remember for any cross-repo (autoarray->autolens) additive API: expect first-run red, merge upstream, rerun.
