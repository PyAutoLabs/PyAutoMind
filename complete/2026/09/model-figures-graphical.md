## model-figures-graphical
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1616 (closed completed 2026-09-12)
- completed: 2026-09-12
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1617 (merged `650cb88339f6b93c0ab4c52356b866f26669e82b`)
- workspace-pr: https://github.com/PyAutoLabs/autofit_workspace/pull/153 (merged `4f121f2a64a8a7b71f87bbe715fe0c9a7a80c526`)
- workspace-pr: https://github.com/PyAutoLabs/HowToFit/pull/51 (merged `3cadd7d6303fd507ddf91c0fa03d7aaf02e3d8a6`)
- pending-release: PyAutoFit@https://github.com/PyAutoLabs/PyAutoFit/pull/1617
- epic: model-figures — phase 4 of 6 shipped; phase 5 (`draft/feature/autofit/model_figures_5_ep_view.md`, the EP diagnostic view) is now unblocked, and phase 6 (`draft/feature/workspaces/model_figures_6_rollout.md`) has its last blocker cleared
- session: local-dev, Fable architect session; implementation, tests, docs, ship and close-out legs delegated to Opus subagents (worktree `~/Code/PyAutoLabs-wt/model-figures-graphical`, parallel-claim waiver vs `remove-parallel-ep-optimiser` #1612 — disjoint files)
- summary: |
    `af.ModelPlotter` now draws standard plate notation for graphical models.
    Passing a `FactorGraphModel`'s `global_prior_model` to the plotter triggers a
    graphical pass in `graph_spec` keyed off `GlobalPriorModel.factor`: repeated
    per-dataset structure collapses into a dashed **dataset plate** badged with
    the dataset count; **shared priors are hoisted** into a card above the plate
    and linked back to its rows; **hierarchical draws are not sharing** — a
    hierarchically drawn parameter renders as a `drawn` pill fed by a violet
    arrow from its `HierarchicalFactor` card (the review's highest-priority
    correction: `⇄ centre` and the draw arrow make opposite claims); **observed
    data gets its own green `observed` encoding**, never the grey fixed pill; and
    the footer splits the parameter count into hyper-parameters, per-dataset
    parameters and unique sampled scalars.

    New internals (none exported from `autofit`): `graph_spec.FactorInfo`,
    `graph_spec.DrawEdge` (a draw edge instead of a sharing link),
    `GraphSpec.graphical_counts(raw_root)`, plus `model_figure` dataset-plate
    detection, shared-prior hoisting, draw-route rendering and the
    `observed`/`drawn`/`shared` pill states. Two internal signatures gained
    optional arguments: `graph_spec._path_index(spec, model, hyper_paths=None)`
    and `model_figure.presentation._badge_colours(badge, state="free")`.

    **Behavioural, not API:** `autofit/__init__.py` is unchanged and no public
    symbol was added, removed, renamed or re-signatured.
    `af.ModelPlotter(factor_graph.global_prior_model).figure()` previously drew
    the global model as ordinary repeated cards and now renders plate notation.
    Non-graphical models render exactly as before; no migration.

    Downstream, this filled the three "visualization not implemented" holes —
    `docs/features/graphical.md`, `autofit_workspace/scripts/features/graphical_models.py`
    and HowToFit chapter 3 — and shipped the shared-vs-hierarchical teaching
    pair as HowToFit tutorials 2 and 4.
- verification: |
    `pytest test_autofit/` 2759 passed / 2 skipped / 0 failed, including new
    suites `test_autofit/graph_spec/test_graphical.py` and
    `test_autofit/model_figure/test_graphical_presentation.py`; `black --check`
    and `pyflakes` clean on touched files; Sphinx 30 warnings == `main`
    baseline (30); figures regenerated via
    `docs/images/model_figures/make_figures.py` and reviewed.

    CI at merge — every run and every matrix leg green on each head sha:
    PyAutoFit `447c00e92` Tests (3.12 / 3.13 / nojax) + Docs = 4/4;
    autofit_workspace `b85bbac` Smoke (3.12 / 3.13 / changes) + Navigator
    (catalogue staleness / paths + banner lint / unbatched multi-start) = 6/6;
    HowToFit `e62ac27` Smoke 3 legs + Navigator 3 legs + Tutorials Complete = 7/7.
    All three PRs read `CLEAN` / `MERGEABLE`; merged in library-first gate order.
- notes: |
    Opened under Heart RED (`red_reason` "release validation FAILED (stage
    integrate)" — unrelated autolens / autolens_test scripts) with explicit
    human authorisation recorded on PyAutoFit#1616. That readiness judgement was
    made at PR-open and was **not** re-run at merge; the Heart *freeze* flag,
    which is the only gate `/prm` reads, was clear (`not frozen`, exit 0).

    `pending-release: PyAutoFit@#1617` is carried into this record deliberately:
    a merged library PR is not a released library, and only `/review_release`
    clears the key once a release has actually published.

## Original prompt

# Model figures phase 4 — plate notation for graphical models

Type: feature
Target: PyAutoFit
Repos:
- PyAutoFit
- autofit_workspace
- HowToFit
Themes:
- visualization
- graphical-ep
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: formalised
Consequence: judge
Review-minutes: 25
Unattended: ready
Epic: model-figures
Phase: 4
Filed: 2026-09-10
Issued: 2026-09-11

**Phase 2 shipped 2026-09-11** — `complete/2026/09/model-figures-renderer.md` (PyAutoFit#1614 merged, autofit_workspace#152 merged); this phase is unblocked.
(Deliberately not in a `Blocked-by:` header: that key is graded against GitHub
refs and cannot name a Mind prompt path.)

Phase 4 of the `model-figures` epic. Ledger (brief, full design record, full
independent review): `draft/feature/autofit/model_figures_epic.md`. This phase
adds the **teaching-oriented model view** for graphical models — plate notation
over a `FactorGraphModel`. The *diagnostic* EP factor graph is phase 5; the
review explicitly approved keeping them separate because they answer different
questions.

## The figure

Standard plate notation, drawn with the phase-2 vocabulary:

- A **shared prior hoisted above the plate**, drawn once, with the plate members
  pointing at it.
- A dashed **plate** `dataset i = 1…N` containing one collapsed component box,
  whose rows carry either a shared pointer or a per-dataset free pill.
- **Observed data** with **its own encoding** — shaded `data_i`. Fixed model
  constants and observations are different concepts and must not share the grey
  pill.
- **Hierarchical draws are not sharing.** This is the review's first and highest
  priority correction. A hierarchically drawn parameter renders as **`centre_i`
  with a "drawn" annotation**, and the parent distribution's arrow **ends on
  that pill**, not on the dataset frame and not as a shared marker. `⇄ centre`
  says "the same parameter across datasets"; the hierarchical arrow says
  "distinct centres drawn from a common distribution". They are opposite claims.
- **Hyper-parameters are counted separately** from the per-dataset parameters
  (e.g. two free hyper-parameters *plus* three parameters per dataset), and the
  footer says so.

## Plate inference

Plates are **inferred**, because declarative variables carry `plates=()` — there
is no plate information in the model to read. Infer by:

1. grouping `graph.analysis_factors` by **prior-model isomorphism**, then
2. checking, per path, the **actual sharing and hierarchical membership**.

Matching model *shape* does not establish identical priors, identical analyses,
or conditional independence — the review is explicit that inference must inspect
actual sharing and hierarchical membership, not shape alone. The phase-1 plate
safety condition applies here too: a plate must preserve sharing, relations,
assertions and exceptions across members, and the figure states what the plate
repeats.

## Verified primitives and traps (DESIGN §4, §6 — executed)

- `fgm.graph` **rebuilds on every access** and renames `PriorFactor`s. Cache it
  once and work from the cached object, or names will drift between reads.
- `factor.name` is **not unique** across `_HierarchicalFactor`s. Use
  `factor.name_for_variable(v)`; **never** `variable.label`.
- Declarative variables have `plates=()` — do not expect to read plates off the
  graph.
- `with_free_parameters` does **not** exist on the installed `af.Model`; the live
  multi-dataset idiom is `model.copy()` + `af.AnalysisFactor` +
  `af.FactorGraphModel`. In the fully-shared case all children of
  `GlobalPriorModel` are the **same object** (`id == 1` for all three).
- `CompoundPrior` / `ComparisonAssertion` are `AbstractPriorModel`s with
  `cls = float` and masquerade as components; `repr()` of a `CompoundPrior`
  subclass without `__str__` recurses forever (`compound.py:88`) — never `repr`
  in a label path.

## Fill the two "not implemented yet" holes

Both exist today and both say, in the text, that the picture is missing:

1. `autofit_workspace/scripts/features/graphical_models.py` — "This is what our
   factor graph looks like:" followed by **nothing**.
2. HowToFit `chapter_graphical_models`, tutorial 2 — "visualization of graphs
   not implemented yet".

## Teaching examples — shared vs hierarchical

The review made this phase's *pedagogical* deliverable explicit: ship a pair of
worked examples that put the two side by side, because conflating them is the
single most common misreading of a plate diagram.

- **Shared**: one parameter, one prior object, N datasets — the arrow means
  "this is literally the same number".
- **Hierarchical**: N distinct `centre_i`, each *drawn* from a parent
  distribution whose own parameters are free — the arrow means "these came from
  a common population".

Each example carries its figure, its `graph.info`, and one paragraph saying what
the reader should be able to see in the figure that the text does not show.

## Acceptance

- Both placeholders render a figure.
- A hierarchical model's figure shows `centre_i` "drawn", with the parent arrow
  landing on the pill — and no shared marker anywhere on it.
- A shared model's figure hoists the shared prior above the plate.
- Observed data is visually distinct from fixed constants.
- Parameter accounting in the footer separates hyper-parameters from per-dataset
  parameters.
