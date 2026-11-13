# autocti_workspace: database scripts delete the wrong .sqlite under test mode, so a second run fails

Type: bug
Target: autocti_workspace
Repos:
- autocti_workspace
Themes:
- cti
- smoke
Difficulty: easy
Autonomy: supervised
Priority: low
Status: formalised
Consequence: glance
Witness: running `dataset_1d/advanced/temporal/plot.py` twice in a row under `config/build/profile_smoke.yaml` succeeds both times, and the same holds for every script that builds a database with `af.Aggregator.from_database(filename=...)` + `add_directory`.
Review-minutes: 3
Unattended: ready
Lane: any
Epic: cti-upkeep
Phase: 3
Filed: 2026-11-06

Found during cti-five-failing-scripts (autocti_workspace#45), 2026-11-06. Six scripts start with

```python
try:
    os.remove(path.join("output", f"{database_name}.sqlite"))
except FileNotFoundError:
    pass
agg = af.Aggregator.from_database(filename=f"{database_name}.sqlite", completed_only=False)
agg.add_directory(...)
```

Under `PYAUTO_TEST_MODE` the database is written to `output/test_mode/<name>.sqlite`, but the
script removes `output/<name>.sqlite`. So the old database survives, and the second run re-inserts
the same fits: `sqlite3.IntegrityError: UNIQUE constraint failed: fit.id` (this is the
"SQLAlchemy error" the 2026-11-05 triage saw on `temporal/plot.py`). CI always runs from a fresh
clone, so smoke stays green; it bites local re-runs only.

Scripts: `dataset_1d/advanced/temporal/{database,plot}.py`, `plot/ccd/{dataset_1d,imaging_ci}/database.py`,
`plot/fpa/{dataset_1d,imaging_ci}/database.py`.

Fix options: remove the file at the path the aggregator actually uses (check whether PyAutoFit
exposes the resolved output root, e.g. via `autoconf`/test-mode path helpers), or have the
library's `from_database` accept an overwrite flag. Check autolens_workspace for the existing
pattern first and mirror it.
