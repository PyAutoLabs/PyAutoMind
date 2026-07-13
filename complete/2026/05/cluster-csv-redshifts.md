## cluster-csv-redshifts
- completed: 2026-05-06 (retroactive log — INCORRECT, see correction below)
- repos: autolens_workspace
- corrected: 2026-05-18 — verification was wrong; work never shipped. Re-issued via `issued/2_modeling_cluster.md` rewrite.
- notes: |
    Retroactively logged via 2026-05-06 hygiene scan. Original prompt
    `cluster/2_modeling.md` asked for `autolens_workspace/scripts/cluster/modeling.py`
    to load redshifts from `point_datasets.csv` via `al.list_from_csv` and link
    them to `Galaxy.redshift` (replacing the hardcoded `redshift=1.0`), plus
    move toward CSV-driven main/source galaxy loading.

    **Correction (2026-05-18):** the 2026-05-06 verifier saw `al.list_from_csv`
    on `modeling.py:143` but missed that the call is inside a `"""..."""`
    docstring example block — it's not the actual code path. The real code
    still loops `for i in range(5): al.from_json(point_dataset_{i}.json)`,
    hardcodes the source galaxy `redshift=1.0` (line 367), and uses the
    pre-rewrite `extra_galaxies` + scaling-relation structure (10 satellites,
    5 sources) which is fundamentally mismatched to the current 2-main + halo
    + 2-source-at-different-redshifts simulator. `cluster/modeling` and
    `cluster/start_here` remain parked in `autolens_workspace/config/build/no_run.yaml`.
    Work re-scoped and re-issued as a minimal first-pass rewrite of
    `modeling.py` only — see updated `issued/2_modeling_cluster.md`. Lesson:
    retroactive hygiene sweeps must check that "verified" code isn't inside
    docstring blocks.
