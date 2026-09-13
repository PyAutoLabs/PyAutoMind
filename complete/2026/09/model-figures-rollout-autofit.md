## model-figures-rollout-autofit
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1620 (closed completed 2026-09-13)
- completed: 2026-09-13
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1621 (merged `c089d0fb3`, head `1ff4572c1`, 1 commit)
- workspace-pr: https://github.com/PyAutoLabs/autofit_workspace/pull/154 (merged `8ef02275f`, head `ff8160f`, 2 commits)
- workspace-pr: https://github.com/PyAutoLabs/HowToFit/pull/52 (merged `70bfcfa18`, head `9e1b165`, 1 commit)
- pending-release: PyAutoFit@https://github.com/PyAutoLabs/PyAutoFit/pull/1621
- epic: model-figures phase 6a (sub-task (a) of `draft/feature/workspaces/model_figures_6_rollout.md`; (b)-(e) remain on the map)
- summary: |
    Sub-task (a) of the model-figures rollout: every script and tutorial in
    autofit_workspace and HowToFit that prints a model's `info` now draws
    `af.ModelPlotter(model).figure()` beside it, so the map (structure) is read
    before the legend (priors and values). autofit_workspace: 31 ModelPlotter
    figures across 9 scripts (cookbooks/model.py 12, multi_level_model.py 2,
    result.py 1 after the aggregator loop, features/model_comparison.py 3,
    search_chaining.py 5, search_grid_search.py 1, searches/start_point.py 2,
    overview_1_the_basics.py 4) plus the EP rollout in
    features/expectation_propagation.py (global-model figure at composition,
    `visualise_interval=1`, `__Seeing The Sweep__` block with
    `af.EPPlotter(result.factor_graph, ep_history=result.ep_history).figure(kind="state")`,
    graph_model.png / graph_state.png output-folder bullets). HowToFit: 13
    ModelPlotter figures across 7 tutorials (1.1 x4 with the map/legend teaching,
    1.3, 1.4 x4 with the `5 components` plate, 1.7, 1.optional_bayesian, 3.3,
    3.5) plus the EP state figure in tutorial 5 and `model_figure: false` added to
    config/output.yaml. Library: `EPResult.factor_graph` (additive, default None)
    populated by `optimise()`, because the high-level `optimise` built the swept
    graph internally and `af.EPPlotter(kind="state")` needs that graph, never
    `FactorGraphModel.graph` (rebuilds and renames prior factors per access).
    Notebooks regenerated in both repos (9 + 7 twins; catalogues byte-identical).
- decisions: |
    - Coverage rule: a figure at EVERY bare model print (the prompt's grep
      acceptance), including re-prints of an unchanged structure, where the
      prose makes the "map unchanged, legend moved" point (rendered fact:
      tutorial 4's tuned-priors variant renders byte-identically to the free
      one). Explicit exceptions: the aggregator loop in cookbooks/result.py gets
      one figure after the loop; `result*.info` / `samples.info` are not model
      prints. The map/legend definition is stated once per script (the older
      phase-2/4 blocks in model.py and multi_level_model.py were trimmed).
    - All three PRs opened under Heart RED `release validation FAILED (stage
      integrate)` (unrelated autolens integrate scripts) with explicit human
      authorisation 2026-09-13; merged via /prm in library-first order.
- verification: |
    PyAutoFit: full test_autofit 2847 passed / 2 skipped (+4 new in
    test_autofit/graphical/test_ep_result_factor_graph.py); sphinx 30 == baseline;
    black/pyflakes clean on touched files. Every touched workspace script and
    tutorial ran headless under the smoke env profile against the worktree
    PyAutoFit, exit 0, no traceback; autofit_workspace run_smoke 8 scripts + 2
    notebooks PASS, HowToFit run_smoke 18/18 PASS (tutorial 5 is in
    config/build/no_run.yaml NEEDS_FIX PyAutoFit#1454, so its manual headless run
    is the only coverage). EP prose was checked against real renders (HowToFit)
    and the renderer's encodings in autofit/model_figure/ep/render.py. CI at
    merge: every run and every matrix leg green on each head sha, 0 runs
    not-completed anywhere. PyAutoFit#1621 (`1ff4572c1`) — Docs (docs-build) +
    Tests (unittest-nojax, 3.12, 3.13). autofit_workspace#154 (`ff8160f`) —
    Navigator Check (3 jobs) + Smoke Tests (changes, 3.12, 3.13). HowToFit#52
    (`9e1b165`) — Navigator Check (3 jobs) + Tutorials Complete + Smoke Tests
    (3 legs). All three PRs read CLEAN / MERGEABLE at merge; merges proven in
    the canonical checkouts by `merge-base --is-ancestor` against `origin/main`.
- traps: |
    - `factor_graph.optimise(...)` returned no handle on the swept graph; fixed
      in the library, not with private `_make_ep_optimiser` calls in scripts.
    - `Factor.__eq__`/`__hash__` ignore the name, so history keys still compare
      equal to `FactorGraphModel.graph`'s renamed PriorFactors on a tiny model;
      the plotter only visibly breaks on larger graphs, the docs caveat stands.
    - `HowToFit/scripts/chapter_1_introduction/tutorial_1_models.py` is CRLF; a
      python read/write silently converted it to LF (1144-line phantom diff)
      and had to be restored before committing.
    - `pyauto-brain intake dashboard --check` does not exist in this Brain;
      the dry-run `intake dashboard` + `git status` is the currency check.
    - `run_smoke.py` writes an untracked `test-results/` in autofit_workspace
      (gitignored in HowToFit only) — remove it before staging.
- follow-ups: |
    1. `draft/bug/howtofit/tutorial_5_ep_shared_centre_never_assigned.md` — tutorial 5
       creates `centre_shared_prior` but never assigns it, so no centre is shared
       and dataset_0 never updates (filed 2026-09-13).
    2. Rollout map next cut: **(b) PyAutoLens surfaces**
       (`draft/feature/workspaces/model_figures_6_rollout.md`).
    3. Optional EP overlays: `draft/feature/autofit/model_figures_ep_overlays.md`.

## Original prompt

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
