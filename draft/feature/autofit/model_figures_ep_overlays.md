# Model figures — optional EP state overlays (mean ± std, precision, KL sparklines)

Type: feature
Target: PyAutoFit
Repos:
- PyAutoFit
Themes:
- visualization
- graphical-ep
Difficulty: medium
Autonomy: supervised
Priority: low
Status: formalised
Consequence: judge
Review-minutes: 20
Unattended: ready
Epic: model-figures
Filed: 2026-09-13

Follow-up split out of phase 5 of the `model-figures` epic at its close-out
(`complete/2026/09/model-figures-ep-view.md`, PyAutoFit#1619 merged
2026-09-13). Phase 5 shipped the EP factor-graph view (`af.EPPlotter`,
`graph_model.png` once + `graph_state.png` per `visualise_interval` tick behind
the `output.yaml` `model_figure` key) carrying the three highest-priority state
overlays from the design review: factor status, update age and confirmed
reverted updates. The human decision at plan approval on 2026-09-12 was to
defer the remaining, optional overlays to this prompt so the base view could
ship on its own evidence.

## Goal

Add opt-in quantitative overlays to the `kind="state"` EP figure, each off by
default so the shipped figure is byte-for-byte unchanged when none is requested:

1. **mean ± std per variable** — the current `EPMeanField` marginal for each
   variable node, rendered as a small `μ ± σ` annotation on (or beside) the
   variable pill. Source: the mean-field approximation's per-variable message
   (`model_approx.mean_field[v]`); use the same reduction the EP history uses
   for its `model.info`-style summaries so figure and text agree.
2. **precision per factor-variable edge** — the precision each factor
   currently contributes to a variable, drawn as edge weight/thickness (and a
   legend), so a factor that has been reverted or is stale visibly contributes
   nothing. Source: the factor's cavity/message in the approximation.
3. **KL sparklines per factor** — a tiny sparkline of the per-update KL
   divergence (or evidence delta, whichever the `FactorHistory` actually
   records) across sweeps, placed in the factor card, so oscillating or
   non-converging factors stand out at a glance.

## Constraints (carry over from phase 5 — do not relitigate)

- networkx + matplotlib only; graphviz stays rejected (no `dot` binary
  locally, on the GH runner or Colab, not pip-installable).
- The reversion signal is `status.changed[v] is False`, never
  `changed is None`; stale = `sweeps >= 1` and 0 updated; age from
  `FactorHistory`. Overlays must not reintroduce either conflation.
- Every drawn element must resolve to a `model.info` / EP history quantity;
  no derived numbers that cannot be pointed at in the text output.
- Never hide a failing plate member behind an aggregate: plate-collapsed
  factors show the worst member's overlay, not the mean.
- Additive API only: new keyword arguments on `EPPlotter.figure(...)` (e.g.
  `overlays=("mean_std", "precision", "kl")`) and an `output.yaml` sub-key under
  `model_figure` for the per-tick hook; nothing renamed, nothing made required.

## Acceptance

- Unit tests on the existing EP doubles
  (`graphical_doubles.hierarchical_graph`,
  `test_factor_failure_recovery.{OverWideFit,PartialRevertFit,make_two_variable_approx}`)
  asserting each overlay's numbers against the approximation directly.
- Regenerated evidence PNGs via `docs/images/model_figures/make_figures.py`
  and a short "Overlays" paragraph in `docs/features/graphical.md`'s
  "Seeing the EP run" section; sphinx warning count stays at baseline.
- With no overlays requested the rendered `graph_state.png` is unchanged from
  phase 5 (pixel-compare in a test, or hash the render).

<!-- formalised by the Intake (Conception) Agent on 2026-09-13 from the human's raw prompt text -->
