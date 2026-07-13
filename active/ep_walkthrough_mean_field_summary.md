# `@autofit_workspace` Wire mean_field_summary into the EP walkthrough

Type: docs
Target: autofit_workspace
Difficulty: easy
Autonomy: safe
Priority: low
Status: formalised

Follow-up from PyAutoFit#1335 (merged #1349): the Phase-4 diagnostics
module exports `mean_field_summary()` / `EPDiagnostics` /
`check_sigma_collapse` from `autofit.graphical`. Wire an end-of-example
`mean_field_summary()` call (and a pointer at the emitted
`ep_history.csv` / `mean_field_evolution.png` artifacts) into
`scripts/features/expectation_propagation.py` (merged via
autofit_workspace#82), so the walkthrough demonstrates the built-in
diagnostics instead of stopping at the raw mean field.

<!-- filed 2026-07-10 at #1335 close-out -->
