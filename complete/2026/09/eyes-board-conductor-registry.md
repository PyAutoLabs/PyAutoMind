## eyes-board-conductor-registry
- issue: https://github.com/PyAutoLabs/PyAutoMind/issues/451
- completed: 2026-09-28
- epic: pyautoeyes-birth (phase 2)
- library-pr: https://github.com/PyAutoLabs/PyAutoEyes/pull/3
- library-pr: https://github.com/PyAutoLabs/PyAutoBrain/pull/429

### What shipped
- **PyAutoEyes#3** (merge a2e1ee7):
  - New `eyes/context.py` gives each instance its context: the Brain conductor survey (PNGs, gaps, orphans and stale renders per domain) and the open Mind critiques (drafts that mention the instance).
  - Every figure gets a "Suggest an improvement" link. It opens a pre-filled `eyes-critique` issue on the project repo titled `figure: <domain>/<file>`. That label now exists on autolens_visualization.
  - A counts table (Instances / Figures / Behind / Critiques) heads `dashboard.md`, and `badge.json` is generated beside it.
  - The `<!-- eyes:context -->` carry-forward markers stop a CI render with no checkout from erasing the survey.
  - `pyauto-eyes board` gains `--no-survey` and `--mind`.
- **PyAutoBrain#429** (merge 79a8652):
  - The `eyes` board surface and a policy.yaml chip in the canonical organ order.
  - `ORGANS["eyes"]` gold and `MARKS["eyes"]`, which put the chip in every family footer.
  - A `collect_eyes()` strip that reads the Eyes counts table.
  - `pyauto-brain eyes survey|review --instance NAME` resolves through the PyAutoEyes `registry.yaml` and fans out from the organ root. It exits 2 on an unknown instance.
  - Conductor AGENTS.md and the eyes skill prose are updated.

### Witness evidence (from the PR test plans)
- Eyes: 65 tests passed. Ruff is clean. Live `pyauto-eyes check` is OK (40 figures resolve on raw URLs). Live `board` shows lens with 40 png, 0 gaps, 0 orphans, 0 stale and 5 critiques.
- Brain: 1085 tests passed. Heart and Hands footer tests pass against the branch. Live `eyes survey --instance lens` shows 22 imaging png and 18 interferometer png, with the tracked manifest present.

### Not verified / follow-ups
- The PyAutoEyes **Pages Dashboard** workflow failed on the merge commit a2e1ee7 (and on #2). `configure-pages` reports "Create Pages site failed: Resource not accessible by integration" because GitHub Pages is not enabled on the repo. A human needs to enable it (Source: GitHub Actions) and re-run it. `badge.json` and the dashboard are therefore not yet published.
- The post-merge `dashboard_refresh.yml` dispatch (no diff apart from live critiques) was not run.
- The sibling boards gain the Eyes chip on their next self-heal refresh, which was not observed at close-out.
- The recursive-producer scan bug was deliberately left to `draft/bug/pyautobrain/eyes_survey_recursive_producers.md`.

## Original prompt

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
Issued: 2026-09-28

Blocked on: none — phase 1b COMPLETE 2026-09-28 (PyAutoMind#448; record `complete/2026/09/eyes-organ-skeleton.md`).

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
