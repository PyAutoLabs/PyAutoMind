# PyAutoEyes phase 2 — organ board + Eyes conductor registry awareness

Type: feature
Target: PyAutoEyes
Repos:
- PyAutoEyes
- PyAutoBrain
Themes:
- visualization
- infrastructure
Difficulty: large
Autonomy: supervised
Priority: high
Lane: local-dev
Status: draft
Consequence: judge
Witness: the PyAutoEyes Pages board publishes; the Brain board footer shows the Eyes chip; `tests/test_board_theme.py` green; `pyauto-brain eyes survey organs/PyAutoEyes` surveys every registered instance
Review-minutes: 15
Epic: pyautoeyes-birth
Phase: 2
Filed: 2026-09-25

Blocked on: phase 1 shipped.

## Task

- `eyes/board.py` renders `dashboard.md/.html` from every instance's
  `viz_manifest.yaml` + conductor survey (per instance: figure count, stale,
  gaps, orphans, last render version, open critiques from the Mind draft
  list); `pages_dashboard.yml` + `dashboard_refresh.yml` (Cortex pattern);
  `badge.json`.
- Brain: `config/policy.yaml` `board.boards` gets `eyes: PyAutoEyes`;
  `board/_theme.py` `ORGANS["eyes"]` palette + `MARKS["eyes"]` glyph
  (`tests/test_board_theme.py` enforces); optional `collect_eyes()` strip in
  `board/_board.py` reading `dashboard.md` counts.
- Eyes conductor: `--instance <name>` resolving through `registry.yaml`
  (`survey`/`review` default to all instances when given the organ root); fix
  or formally document the non-recursive producer scan (draft bug
  `draft/bug/pyautobrain/eyes_survey_recursive_producers.md`).
