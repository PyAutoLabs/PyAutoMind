# Model figures phase 6b — PyAutoLens surfaces (autolens_workspace + HowToLens, SLaM deferred)

Type: feature
Target: workspaces
Repos:
- autolens_workspace
- HowToLens
Themes:
- visualization
- notebooks
Difficulty: large
Autonomy: supervised
Priority: normal
Status: formalised
Consequence: judge
Review-minutes: 45
Unattended: ready
Epic: model-figures
Phase: 6b
Filed: 2026-09-13
Issued: 2026-09-13

This is sub-task **(b)** cut from the rollout map
`draft/feature/workspaces/model_figures_6_rollout.md`, which orders one sub-task at a
time and never bundles two repos' rollouts into one PR. The map's bullet, verbatim:
"**(b) PyAutoLens surfaces** — `guides/modeling/cookbook.py` (phase 3 already did this;
verify only), `imaging/modeling/*` and `features/*` (MGE, pixelization, point source,
multi-dataset), `slam_start_here.py` and the SLaM pipelines, and the HowToLens chapters
that compose models." The SLaM half of that bullet is deferred here — see below.

## Context

Every script/tutorial that prints a model's `info` should draw
`af.ModelPlotter(model).figure()` beside it (map before legend). Census (read-only,
2026-09-13):

| Surface | Bare model prints | Files | CI |
|---|---|---|---|
| autolens_workspace, non-SLaM | 127 | 102 | smoke allowlist (37 scripts, incl. `guides/modeling/cookbook.py`, `imaging/modeling.py`, `multi_galaxy/*`, …); no SLaM script is smoke-tested |
| HowToLens | 20 | 12 (chapters 2 and 4 only) | opt-out smoke, `no_run.yaml` empty → every tutorial runs |
| SLaM-style scripts (41) | 0 prints; ~200 inline stage `def`s | 41 | none |

Human decisions (2026-09-13): **SLaM is deferred to its own cut (b2)**
(`draft/feature/workspaces/model_figures_6b2_slam_stages.md`) — nothing in this task
touches a SLaM stage; **autolens_workspace ships as two PRs by folder**, plus one
HowToLens PR. No library change is expected (lens models rendered in phase 3;
`EPResult.factor_graph` is on PyAutoFit main from 6a).

## Waves and PRs

- **Wave 1 (parallel legs):**
  - **HowToLens PR** — 20 sites / 12 tutorials + `config/output.yaml` `model_figure: false`
    key (absent today).
  - **autolens_workspace PR A** — folders `guides/`, `imaging/`, `point_source/`,
    `multi_dataset/` (~61 bare sites).
- **Wave 2 (after PR A merges):** **autolens_workspace PR B** — `interferometer/`,
  `group/`, `multi_galaxy/`, `cluster/`, `weak/` (~66 sites) on branch
  `feature/model-figures-rollout-lens-b` cut from the merged `main` in the same worktree.
  One task, shipped in waves; the record is written only after wave 2 (prm.md 5.1 "waves trap").

## Pattern (unchanged from 6a)

`print(x.info)` → blank line → column-0 `"""` prose `"""` → `af.ModelPlotter(x).figure()`. First figure
in a script: the map/legend opener (as `autolens_workspace/scripts/guides/modeling/cookbook.py:84-97`)
+ one paragraph on what THIS figure shows; later sites 1-3 lines; unchanged structure → "map unchanged,
legend moved". Lens vocabulary must be **verified by rendering** before it is written (as 6a did):
`galaxies` collection frames, `redshift = 0.5` subtitle, light/mass cards, MGE `30 components` plate +
`centre · shared across group`, `intensity · solved` (linear light), `reconstruction · solved`
(pixelization), `centre · solved` (point source), `areas_factor · missing`. No try/except. Prose
register = PyAutoLens workspace style (`__Section__` docstrings; assistant AGENTS.md); read the whole
file before editing, targeted edits only.

Placement exceptions (recorded in the record):

- `guides/results/database/start_here.py:351` — `print(model.info)` inside
  `for model in model_gen:` → one figure after the loop.
- `guides/results/start_here.py:245` — print inside `if (files_path / "model.json").exists():`
  → the `.figure()` goes inside the same `if`; the one-line prose goes in the preceding
  module-level docstring (indented strings never become cells).
- `guides/modeling/cookbook.py:505` — the reloaded-JSON model; prose already describes the
  figure's one difference, so add the call (phase 3 left it bare).
- `guides/modeling/advanced/expectation_propagation.py` — beside the `global_prior_model.info` figure,
  mirror 6a's EP rollout: `visualise_interval=1` on `optimise(...)` (line 276) and, after the fit,
  `af.EPPlotter(factor_graph_result.factor_graph, ep_history=factor_graph_result.ep_history).figure(kind="state")`
  with the same reading prose; this needs PyAutoFit main (merged 6a, unreleased) → `release-gate:
  PyAutoFit` on the row. `graphical.py` / `hierarchical.py`: figure on `global_prior_model` only.
- `result*.info`, `dataset*.info`, `mass_result.info` are not model prints; `multi_dataset/features/one_by_one/modeling.py:266` is commented out — leave.
- `cluster/mass_parameterizations*.py` prose promises prints that do not exist — out of
  scope; ledger line (fix belongs to a docs prompt).

## Verification

- Every touched script runs headless from its repo root under the smoke env profile
  (`PYAUTO_TEST_MODE=1 PYAUTO_SKIP_FIT_OUTPUT=1 PYAUTO_SKIP_VISUALIZATION=1
  PYAUTO_SKIP_CHECKS=1 PYAUTO_SKIP_API_GATE=1 MPLBACKEND=Agg`, worktree `activate.sh`
  sourced), exit 0, no traceback. A leg may need `dataset/` present (the repo ships them or
  a simulator writes them; follow `AGENTS.md`). Scripts in `config/build/no_run.yaml` (GUI,
  time_delays cosmology, CSE…) that cannot run headless: edit them anyway, skip the run, and
  list them as "edited, not runnable" in the PR body.
- `.github/scripts/run_smoke.py` for the allowlisted scripts touched (autolens_workspace)
  and the full HowToLens runner (39 tutorials).
- Coverage grep per touched folder: every model print has `.figure(` within ~20 lines;
  exceptions listed.
- Notebooks: `PYTHONPATH=../PyAutoHands/autohands python3 ../PyAutoHands/autohands/generate.py autolens`
  / `... howtolens` from each repo root; commit only touched twins (+ `llms-full.txt` /
  `workspace_index.json` if rewritten); `check_navigator.py` OK. `config/priors/*.yaml` are CRLF
  in both repos — do not touch them.
- Ship: `ship_workspace` per PR (pending-release label; PR body `## Scripts Changed` by
  folder, "edited, not runnable" list, no `## Upstream PR`; note the PyAutoFit-main
  dependency of the EP guide), `/prm` per wave, record after wave 2 with the three PRs;
  then the map's next cuts: **(b2) SLaM**, **(c) PyAutoGalaxy surfaces**.
