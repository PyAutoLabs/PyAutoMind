## env-var-rename
- issue: https://github.com/PyAutoLabs/autolens_workspace_test/issues/65
- completed: 2026-04-30
- workspace-pr:
  - https://github.com/PyAutoLabs/autolens_workspace_test/pull/66
  - https://github.com/PyAutoLabs/autogalaxy_workspace_test/pull/21
  - https://github.com/PyAutoLabs/autofit_workspace_test/pull/18
  - https://github.com/PyAutoLabs/PyAutoBuild/pull/63
- notes: Finished the `PYAUTOFIT_TEST_MODE` → `PYAUTO_TEST_MODE` rename in the two `_test` repos skipped by the prior pass (autolens, autogalaxy), and fixed a second silent no-op surfaced by a general scan: `PYAUTO_WORKSPACE_SMALL_DATASETS` (set in every `_test` build config and `PyAutoBuild/release.yml`) was never read by any library — consumers all check `PYAUTO_SMALL_DATASETS`. Both renames switched silent no-ops into canonical names that actually fire. Activating `PYAUTO_SMALL_DATASETS=1` for the first time exposed override gaps: autolens needed `model_composition/`, autogalaxy needed `aggregator/`, `imaging/model_fit`, and `imaging/visualization` (the entire imaging-overrides set autolens already had). All `unset: [PYAUTO_SMALL_DATASETS]` overrides match the established autolens pattern. `lp.py`/`mge.py` parallel write-race noted but not fixed — pre-existing, unrelated to the rename. Out of scope and untouched: `autolens_assistant/CLAUDE.md` (uncommitted local edits) and `z_projects/{cowls_diana,euclid_group,concr}/CLAUDE.md` (not git-tracked from this checkout) — doc references in those still mention the old names.
