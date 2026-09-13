## model-figures-ep-view
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1618 (closed completed 2026-09-13)
- completed: 2026-09-13
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1619 (merged `9ad5fdfa2`, head `ba756b82db472591cb9f3927ca07695b227e2290`, 6 commits on `54f464d97`)
- pending-release: PyAutoFit@https://github.com/PyAutoLabs/PyAutoFit/pull/1619
- epic: model-figures — phase 5 of 6 shipped; phase 6 (`draft/feature/workspaces/model_figures_6_rollout.md`, the workspace/HowToFit rollout) is the only phase left
- session: local-dev, Fable architect session; implementation, tests, docs, ship and close-out legs delegated to Opus subagents (worktree `~/Code/PyAutoLabs-wt/model-figures-ep-view`)
- summary: |
    Phase 5 of the `model-figures` epic: the **diagnostic** EP view, kept
    separate from phase 4's teaching view because they answer different
    questions.

    New package `autofit/model_figure/ep/` — `spec.py` (factor-graph structure),
    `state.py` (what the EP run did to each factor), `presentation.py`,
    `layout.py`, `render.py`, `plotter.py`. It draws an **explicit** factor
    graph (factor nodes and variable nodes both drawn), plate-grouped so it
    survives large dataset counts, with the EP run's state laid over it: factor
    status, update age, and confirmed reverted updates — and it never hides a
    failing plate member behind an aggregate.

    `autofit/model_figure/config.py` lifts the `_model_figure_enabled` gate so
    the phase-4 model view and the new EP views read one switch.

    Public door: `af.EPPlotter(factor_graph, ep_history, model_approx).figure(kind="model"|"state")`.

    `Visualise` writes `graph_model.png` once and `graph_state.png` on every
    `visualise_interval` tick, behind the existing `model_figure` key in
    `output.yaml`.

    `docs/features/graphical.md` gains a "Seeing the EP run" section carrying
    three figures.
- verification: |
    `pytest test_autofit/` 2843 passed / 2 skipped / 0 failed; Sphinx warning
    count 30 == the `main` baseline (30); `black --check` and `pyflakes` clean
    on touched files.

    CI at merge — every run and every matrix leg green on head sha
    `ba756b82`: Tests [pull_request] run 34719550730 (unittest-nojax, 3.12,
    3.13) and Docs [pull_request] run 34719550700 (docs-build), 0 runs
    not-completed. PR read `CLEAN` / `MERGEABLE`. Merge proven in the canonical
    checkout: `origin/feature/model-figures-ep-view` is an ancestor of
    `origin/main`, 0 commits ahead.
- decisions: |
    **Human decisions taken during the phase:**

    - **Layout is networkx + matplotlib only.** graphviz was rejected as a
      dependency: no `dot` binary locally, on the GitHub runner, or on Colab,
      and it is not pip-installable.
    - **Optional overlays deferred.** mean ± std, precision, and KL sparklines
      were cut from this phase and deferred to a follow-up prompt; the three
      highest-priority overlays from the review (status, age, reversion) are
      what shipped.
- traps: |
    Key design facts, verified against the installed EP machinery:

    - **The reversion signal is `status.changed[v] is False`** — never
      `changed is None`. `None` means "not yet visited"; only an explicit
      `False` is a confirmed reverted update. Conflating them paints unvisited
      factors as reverted.
    - **A factor reads as stale when `sweeps >= 1` and 0 of its updates
      landed** — that is the stale predicate, not a time-based one.
    - **Factor age comes from `FactorHistory`**, not from wall-clock or from
      the sweep counter alone.
- notes: |
    Opened 2026-09-12 22:17 under Heart RED ("release validation FAILED (stage
    integrate)" — unrelated autolens / autolens_test scripts) with explicit
    human authorisation, recorded on PyAutoFit#1618. That readiness judgement
    was made at PR-open and was **not** re-run at merge; the Heart *freeze*
    flag, which is the only gate `/prm` reads, was clear (`not frozen`,
    exit 0). The ship-gate BLOCKED comment on the issue was the last comment
    before close-out — no PR-open comment was ever posted, so the "Shipped"
    comment covers both.

    `pending-release: PyAutoFit@#1619` is carried into this record
    deliberately: a merged library PR is not a released library, and only
    `/review_release` clears the key once a release has actually published.
- follow-ups: |
    1. **Optional EP overlays** — mean ± std, precision, and KL sparklines on
       the state view, deferred from this phase by human decision.
    2. **Phase 6 rollout** — put `graph_state.png` into
       `autofit_workspace/scripts/.../expectation_propagation.py` and the
       HowToFit hierarchical EP tutorial. Both need `visualise_interval=1` so a
       short run actually emits a state figure.
       (`draft/feature/workspaces/model_figures_6_rollout.md`)

## Original prompt

# Model figures phase 5 — EP factor-graph view

Type: feature
Target: PyAutoFit
Repos:
- PyAutoFit
Themes:
- visualization
- graphical-ep
Difficulty: large
Autonomy: supervised
Priority: normal
Status: formalised
Consequence: judge
Review-minutes: 30
Unattended: ready
Epic: model-figures
Phase: 5
Filed: 2026-09-10
Issued: 2026-09-12

**Phase 4 shipped 2026-09-12** — `complete/2026/09/model-figures-graphical.md`
(PyAutoFit#1617, autofit_workspace#153, HowToFit#51 merged); this phase is unblocked.
(Deliberately not in a `Blocked-by:` header: that key is graded against GitHub
refs and cannot name a Mind prompt path.)

Phase 5 of the `model-figures` epic. Ledger (brief, full design record, full
independent review): `draft/feature/autofit/model_figures_epic.md`. Phase 4
drew the teaching view; this phase draws the **diagnostic** one — an explicit
factor graph with the EP run's state on it. The review approved the separation:
they answer different questions and should not be one figure.

## The figure

An **explicit factor graph** — factor nodes and variable nodes, both drawn —
**plate-grouped** so it survives large dataset counts, with an EP overlay.

Overlay, in the review's priority order (start with the first three; the rest
are optional detail):

1. **Factor status** — converged / working / stale, from `EPHistory` /
   `FactorHistory` / `Status` / `EPDiagnostics`.
2. **Update age** — how many EP iterations since this factor last successfully
   updated. A factor with zero SUCCESS updates is the STALE state the library
   now warns about (PyAutoFit#1562).
3. **Confirmed reverted updates** — read the **`reverted_variables` set**
   (per-(factor, variable) tracking, PyAutoFit#1576, and present in
   `ep_history.csv`). **Do not** use `Status.changed[v] is False` as the
   reversion signal: "unchanged" and "reverted" are different facts requiring
   different explanations, and only `reverted_variables` establishes rejection.
4. **Variable `mean ± std`** — optional detail, off by default.
5. **Message precision** — optional, and only with **defined handling of signed
   or invalid site precisions**. It must not be presented casually as "how
   strongly this factor constrains the variable"; a negative or invalid site
   precision needs a stated rendering, not an accidental one.
6. KL sparklines per factor — optional polish.

**Collapsed plates must not hide failures behind an average.** At large dataset
counts a collapsed plate shows **status aggregates plus the exceptional
members** by name, with individual factor access available. A plate showing
"mean KL 0.02" while one member has never converged is the failure mode to
design against.

## Files

- `graph_model.png` beside `graph.info` — the static structure, written once.
- `graph_state.png` — the overlay, rewritten on the `visualise_interval` tick.

Both gated by the same `output.yaml` `model_figure` key introduced in phase 2
(never `model_graph`, which gates the graphical-model *text* dump — see the
ledger's Trap section).

## Layout engine — still open

This is the one phase where **graphviz is permitted**, if justified. The
containment layout that serves phases 2–4 is chosen for nesting; an explicit
factor graph is edge-dominated and rank layout may genuinely win. The
constraints that made graphviz unacceptable elsewhere still apply and must be
answered in the plan if it is chosen: the `dot` binary is absent locally, on the
GitHub `ubuntu-24.04` runner and often on Colab, and is not pip-installable — so
a graphviz path needs a matplotlib fallback, or the figure is simply unavailable
in CI and for most users. Present both options in the plan with that cost
stated; the human decides.

## Traps

- `fgm.graph` rebuilds on every access and renames `PriorFactor`s — cache it.
- `factor.name` is not unique across `_HierarchicalFactor`s; use
  `factor.name_for_variable(v)`, never `variable.label`.
- Declarative variables have `plates=()`; plates are inferred (phase 4's
  machinery), not read.

## Acceptance

- An EP run over a small hierarchical model produces `graph_model.png` and a
  sequence of `graph_state.png` files across `visualise_interval` ticks.
- A deliberately stalled factor (zero SUCCESS updates) is visibly stale in the
  figure.
- A run with entries in `reverted_variables` shows them as reverted, and a run
  with merely unchanged variables does **not**.
- A collapsed plate containing one failing member names that member.
