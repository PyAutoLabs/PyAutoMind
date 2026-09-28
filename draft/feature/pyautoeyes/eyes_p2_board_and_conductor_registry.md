# PyAutoEyes phase 2 — cross-project dashboard, critique route, Brain chip, conductor registry

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
Witness: the PyAutoEyes Pages dashboard publishes with a thumbnail per lens figure linked to its raw PNG in `autolens_visualization`, a freshness line, and a working "suggest an improvement" affordance per figure; a `render.yml` run in `autolens_visualization` triggers `dashboard_refresh.yml`; the Brain board footer shows the Eyes chip; `tests/test_board_theme.py` green; `pyauto-brain eyes survey --instance lens` resolves through `registry.yaml`
Review-minutes: 15
Epic: pyautoeyes-birth
Phase: 2
Filed: 2026-09-25

Blocked on: phase 1b shipped.

## Task

- **Dashboard content** (`eyes/board.py` → `dashboard.md/.html`, the epic
  ledger): per registered instance, a thumbnail grid of every figure in its
  tracked manifest, each thumbnail *linked* to the raw PNG in the project
  repo (the organ never copies figures), click-through to full size, grouped
  by domain/producer; per-instance freshness (rendered stack version vs the
  latest library release on PyPI); survey gaps and orphans (from
  `pyauto-eyes survey`); open critiques (Mind drafts carrying the instance's
  target); `badge.json`.
- **Critique route.** Each figure carries a "suggest an improvement"
  affordance that pre-fills a critique routed through intake: a copyable
  `/eyes review <instance> <figure>` command and/or a pre-filled GitHub issue
  link on the project repo (title + figure path + manifest version). The
  dashboard never files anything itself.
- **Brain board chip**: `config/policy.yaml` `boards.eyes: PyAutoEyes`;
  `board/_theme.py` `ORGANS["eyes"]` palette + `MARKS["eyes"]` glyph
  (`tests/test_board_theme.py` enforces); optional `collect_eyes()` strip in
  `board/_board.py` reading the dashboard's counts.
- **Eyes conductor**: `--instance <name>` resolving through the organ's
  `registry.yaml` (`survey`/`review` default to every registered instance
  when given the organ root); the conductor stays repo-name-free — the
  registry is data, not code. The non-recursive producer scan stays its own
  bug draft (`draft/bug/pyautobrain/eyes_survey_recursive_producers.md`).
