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
