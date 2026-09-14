Phase 6b of the `model-figures` epic — the PyAutoLens surfaces — shipped in two waves,
and wave 2 finished under a **changed prose standard** rather than the one the prompt
specified.

## The standard change

Mid-task (2026-09-14) the human ruled that the per-figure reading commentary this
rollout had been writing is information overload and the figure should be
self-explanatory. Every opener block now reads exactly:

> The same model can also be visualized as a figure, making its structure easier to
> understand at a glance.
>
> The figure shows how the model is organized: which parameters belong to each
> component, and whether they are free, fixed, shared, linked by an expression, solved
> during the fit, or not configured. `model.info` provides the corresponding numerical
> details, including the prior assigned to each free parameter and the value of each
> fixed parameter.

This **supersedes the prompt's "Pattern" section** for the opener block and retires its
"lens vocabulary must be verified by rendering" requirement, which no longer had
anything to govern. A later approved pass stripped the same vocabulary (pills, plates,
badges, greyed, footer counts) from the shorter notes at second and third figure sites.

## Shipped (both waves, all four branches verified merged)

| Wave | Repo | PR | Branch |
|---|---|---|---|
| 1 | HowToLens | #81 | `feature/model-figures-rollout-lens` |
| 1 | autolens_workspace | #543 | `feature/model-figures-rollout-lens` |
| 2 | autolens_workspace | #546 | `feature/model-figures-rollout-lens-b` |
| 2 | HowToLens | #83 | `feature/model-figure-prose-lens` |

autolens_workspace #546: 102 scripts + 102 notebooks + `workspace_index.json`, four
commits (collapse 58 files; 51 new wave-2 figure sites across 44 scripts; regenerate
twins; strip later-site vocabulary, 32 notes / 21 scripts). Shipped as ONE PR, a
departure from the prompt's "two PRs by folder", so the sweep did not wait on a merge
to open a third. HowToLens #83: 12 tutorials + 12 twins, 10 teaching sentences preserved.

## Traps worth keeping

- **Wave 2 was stalled, not in flight.** 13 modified interferometer scripts sat
  uncommitted in the worktree for ~22 hours with zero commits ahead of `origin/main`.
  A dead or ended session leaves work that looks active on the dashboard. Check file
  mtimes and `git log origin/main..HEAD`, not just the presence of a worktree.
- **A dead subagent's detached run keeps going.** When the wave-2 agent died on a
  network error mid-verification, its `nohup` script was still executing. Starting a
  second sweep double-ran ~33 scripts concurrently on a 15 GB machine and produced one
  false OOM (`multi_galaxy/features/pixelization/delaunay.py`, which passes solo in
  75s). Genuine limits reproduce **byte-identical** allocation sizes when re-run alone;
  contention does not.
- **`pgrep -f "python3 scripts/"` is useless here** — it matches the harness's own
  `/bin/bash -c '...'` wrappers whose command line contains that string, including the
  one that just wrote the script. It inflated a workload count and deadlocked a
  wait-loop on an idle machine. Match the interpreter: `ps -C python3` / `pgrep -x`.
- **`multi_galaxy/start_here.py` needs `PYAUTO_TEST_MODE=2`** — 54s there against a
  900s timeout at `TEST_MODE=1`.
- **Half the HowToLens blocks carried no `**map**` token**, and in two the token wraps
  across a line break. Use a whitespace-flattened per-file search.
- The prompt's exclusion of `cluster/mass_parameterizations.py` holds, though not for
  the stated reason: it does have one real `print(model_1.info)`, but `model_2`-`model_4`
  have no prints at all, so a figure on `model_1` alone would make the file less
  consistent. Adding the three missing prints is a separate docs task.

## Verification

End-to-end gate clean over `scripts/*.py` and `notebooks/*.ipynb` in both repos — zero
non-exempt figure vocabulary, with science uses of "map" (convergence maps, `θ → θⱼ`
mappings, dict mappings) untouched. Notebooks regenerated via
`PyAutoHands/autohands/generate.py`, `check_navigator.py` passing. Headless 96/102
exit 0; the 6 failures are pre-existing (JAX 26-81 GB allocations on a 15 GB machine,
plus `cluster/lenstool` missing `dataset/cluster/smacs0723`) and **none of the 6 files
carries a non-prose code change**, two carrying no code change at all. All 12 HowToLens
tutorials pass, 3-205s.

Heart YELLOW at ship time, nine pre-existing reasons, human-acknowledged.

Next cuts: **(b2) SLaM stages**, **(c) PyAutoGalaxy surfaces**. The sibling sweep of the
six unclaimed repos shipped as `model-figure-prose-simplify` (autofit_workspace#156).

## Original prompt

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
