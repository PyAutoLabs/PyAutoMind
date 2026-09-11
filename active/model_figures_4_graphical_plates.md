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
