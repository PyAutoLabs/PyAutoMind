# Model figures phase 6a — PyAutoFit surfaces (autofit_workspace + HowToFit, incl. the EP state figure)

Type: feature
Target: workspaces
Repos:
- PyAutoFit
- autofit_workspace
- HowToFit
Themes:
- visualization
- notebooks
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: formalised
Consequence: judge
Review-minutes: 30
Unattended: ready
Epic: model-figures
Phase: 6a
Filed: 2026-09-13
Issued: 2026-09-13

This is sub-task **(a)** cut from the rollout map
`draft/feature/workspaces/model_figures_6_rollout.md`, which orders one sub-task at a
time and never bundles two repos' rollouts into one PR. The map's bullet, verbatim:
"**(a) PyAutoFit surfaces** — `autofit_workspace` cookbooks and `features/`, the
`howtofit` scripts and the HowToFit chapters. The graphical-models chapter waits for
phase 4." Phase 4 has shipped, so that chapter is in scope here.

## Context

The `model-figures` epic (phases 1-5 shipped, phase 5 merged as PyAutoFit#1619) gives
every model a figure: `af.ModelPlotter(model).figure()` for the structure, and for
expectation propagation `af.EPPlotter(...)` plus per-run `graph_model.png` /
`graph_state.png`. Census (read-only, 2026-09-13): `autofit_workspace/scripts/` has
**28 bare** `print(<model>.info)` sites across 9 scripts; `HowToFit/scripts/` has **14
bare** sites across 8 tutorials. Neither EP script draws a figure.

**API gap found:** `FactorGraphModel.optimise(...)`
(`PyAutoFit/autofit/graphical/declarative/abstract.py:172-214`) builds the swept graph
inside `_make_ep_optimiser` and returns an `EPResult` (`declarative/result.py:57`)
carrying only `ep_history`, `declarative_factor`, `updated_ep_mean_field`.
`EPPlotter(kind="state")` must receive **the optimiser's own factor graph** (history is
keyed by its factor objects; `FactorGraphModel.graph` rebuilds and renames on every
access — `docs/features/graphical.md:288-292` says so). So a workspace script cannot
draw the state figure after the high-level `optimise` without a private API. The fix
belongs in the library, once: `EPResult.factor_graph` (additive, default `None`), passed
through from `abstract.py:210-214`, with a test and a `docs/features/graphical.md`
"Seeing the EP run" high-level form.

## Coverage rule

Acceptance is a grep: a figure call beside every `model.info` occurrence. Add one at
**every** bare site, with these exceptions recorded in the completion record:

- `autofit_workspace/scripts/cookbooks/result.py:406` — indented `print(model.info)`
  inside the aggregator loop: one figure **after** the loop for the last loaded model,
  prose says the three are identical in structure.
- `result*.info` / `samples.info` lines are not model prints (not counted).
- Where a print re-shows an **unchanged structure** after a prior/value-only edit (e.g.
  `cookbooks/model.py:109`), the figure still goes in, prose one line: "the map is
  unchanged; only the legend moved" — that contrast is the teaching point.

Pattern (verbatim from phases 2/4): `print(x.info)` → blank line → `"""` prose `"""` →
`af.ModelPlotter(x).figure()`. The prose opens with the fixed map/legend sentence the
first time it appears in a script, then one short paragraph on what the figure shows
that the info cannot. Default `figure()` settings. No `try/except` in scripts; a guard
belongs in the library.

## EP rollout (the phase-5 flag)

- `autofit_workspace/scripts/features/expectation_propagation.py`: at the `factor_graph`
  composition add `print(factor_graph.global_prior_model.info)` +
  `af.ModelPlotter(factor_graph.global_prior_model).figure()`. Add `visualise_interval=1`
  to the `factor_graph.optimise(...)` call (`:303-309`; default 100, so with
  `max_steps=5` the state PNG otherwise refreshes once). After the call add prose +
  `af.EPPlotter(factor_graph_result.factor_graph,
  ep_history=factor_graph_result.ep_history).figure(kind="state")`, reading the figure
  (factor status, update age, confirmed reverted updates); extend the `__Output Folder__`
  prose with `graph_model.png` / `graph_state.png`.
- `HowToFit/scripts/chapter_3_graphical_models/tutorial_5_expectation_propagation.py`:
  figure beside `:221`, `visualise_interval=1` on `:263-264`, EPPlotter state figure +
  tutorial-register prose after the fit, output-folder bullets for the two PNGs. Leave
  `tutorial_optional_hierarchical_ep.py` alone (its optimise is commented out by design).
- `HowToFit/config/output.yaml`: add `model_figure: false` with the same two-line comment
  as `autofit_workspace/config/output.yaml:106-108` — today the key is absent there, so
  the prose pointer would be false.
- Under CI the `LaplaceOptimiser` EP loop runs real sweeps even in `PYAUTO_TEST_MODE`, and
  `EPState.from_history` renders an empty history as `absent` rather than raising — so the
  inline state figure is safe in smoke.

## Notebooks + catalogue

Per repo convention (both AGENTS.md): from the repo root,
`PYTHONPATH=../PyAutoHands/autohands python3 ../PyAutoHands/autohands/generate.py autofit`
/ `... howtofit`. Commit **only** the touched scripts' `.ipynb` twins plus
`llms-full.txt` / `workspace_index.json` if the flow rewrites them; never sweep in other
scripts' pre-existing drift. HowToFit: confirm `tutorial_8_scientific_workflow.ipynb`
still has zero code cells.

## Verification

- PyAutoFit: new test + full `pytest test_autofit/`; `black --check` on touched files;
  sphinx build warning count == 30.
- Every touched script runs headless from its repo root under the smoke env profile
  (`PYAUTO_TEST_MODE=1 PYAUTO_SKIP_FIT_OUTPUT=1 PYAUTO_SKIP_VISUALIZATION=1
  PYAUTO_SKIP_CHECKS=1`, `MPLBACKEND=Agg`, `MPLCONFIGDIR=/tmp/matplotlib`,
  `NUMBA_CACHE_DIR=/tmp/numba_cache`, `PYTHONPATH` pointing at the worktree PyAutoFit so
  the new `EPResult.factor_graph` resolves; `PYAUTO_SKIP_API_GATE=1` for the branch-only
  symbol) — exit 0, no traceback. HowToFit smoke runs *every* tutorial;
  autofit_workspace's allowlist is narrower, so run the EP and `features/` scripts
  locally anyway. `pyauto-heart smoke` grades against the canonical checkout, so run the
  EP scripts against the worktree PyAutoFit explicitly (phase-2 trap).
- Notebooks regenerated; navigator catalogue current; `git status` shows only intended
  twins.
- Ship order: `ship_library` (PyAutoFit PR) → `ship_workspace` (autofit_workspace PR,
  HowToFit PR; both bodies link the library PR; library-first gate) → `/prm` over the
  three, then Mind record + follow-up: the map's next cut is **(b) PyAutoLens surfaces**.
