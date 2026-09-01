# MultiStart quick-update workspace leg: retune start_here prose + AST guard

Type: docs
Target: autolens_workspace
Repos:
- autolens_workspace
- PyAutoFit
Themes:
- workspace
Difficulty: small
Autonomy: safe
Priority: normal
Status: formalised
Consequence: glance
Witness: the three start_here.py scripts (imaging/interferometer/multi_galaxy) pass iterations_per_quick_update/live_visual_update with prose describing the now-real behaviour and the per-gradient-step unit; an AST guard in the workspace test suite asserts no MultiStart* call site in scripts/ passes a kwarg the search does not honour.
Review-minutes: 3
Unattended: ready
Filed: 2026-09-01

Phase 2 of PyAutoFit#1552 (library leg shipped 2026-09-01 via PyAutoFit#1556,
complete/2026/09/multistart-quick-update-wiring.md). The unit semantics are now
settled: quick updates count per GRADIENT STEP (each step evaluates all n_starts
lanes), not per batched evaluation; LiveDisplay/BackgroundQuickUpdate flow
through the standard Fitness path; the startup message states the unit.

Do, in autolens_workspace:
1. Retune the three start_here.py scripts (imaging, interferometer,
   multi_galaxy) — the __Iterations Per Update__ / __Live Visual Update__ prose
   currently describes updates that (pre-#1556) never happened and is wrong on
   the unit; rewrite against the live behaviour and pick sensible cadence
   values for a n_steps~300 budget.
2. Add the AST guard from the original prompt's witness: no MultiStart* call
   site in scripts/ passes a kwarg the search does not honour.
