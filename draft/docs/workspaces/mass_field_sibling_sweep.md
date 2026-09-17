# MassField sibling sweep: autolens_workspace_test, HowToLens, autolens_assistant mentions

Type: docs
Target: workspaces
Repos:
- autolens_workspace_test
- HowToLens
- autolens_assistant
Themes:
- cluster
Difficulty: small
Autonomy: safe
Priority: low
Consequence: notify
Witness: `grep -rn "shear_galaxy" <each repo>` returns nothing; any parity/round-trip script that builds a separate-shear model uses `fields=af.Collection(field=af.Model(al.MassField, ...))`; smoke/parity suites green where they exist.
Review-minutes: 2
Unattended: ready
Epic: mass-field
Phase: 5
Blocked-by: phase 3 (`draft/docs/workspaces/mass_field_workspace_sweep.md`) merged
Filed: 2026-09-17

Fifth phase of `draft/feature/autogalaxy/mass_field_epic.md`. Decided by grep
after phase 3 lands: sweep the sibling repos for the `shear_galaxy` idiom and
for prose that says the shear "is on `lens_0`" in a multi-deflector context.

- `autolens_workspace_test`: multi-galaxy / group parity scripts and the
  COOLEST round-trip script (`coolest_round_trip.py` — its legacy galaxy-attached
  case must stay as the regression for phase 2's legacy peel; add a `MassField`
  case beside it, do not replace).
- `HowToLens`: single-galaxy chapters keep the galaxy-attached shear (epic
  Decisions); only a chapter that models several deflectors changes.
- `autolens_assistant`: wiki pages that describe model composition for
  multi-galaxy / group systems.

If the grep is empty for a repo, record that in the PR and skip it.
