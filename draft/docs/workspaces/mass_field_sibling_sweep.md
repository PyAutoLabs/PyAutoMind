# MassField sibling sweep: HowToLens and autolens_assistant move to `fields=`

Type: docs
Target: workspaces
Repos:
- HowToLens
- autolens_assistant
Themes:
- cluster
Difficulty: medium
Autonomy: safe
Priority: low
Consequence: notify
Witness: in HowToLens `grep -rnE "al\.Galaxy\(.*shear=" scripts/` returns nothing — every chapter's external shear is an `al.MassField` in `fields=` (23 files at HowToLens survey 2026-09-17); autolens_assistant wiki/skill pages describing model composition show the `fields=` slot; HowToLens smoke green; notebooks regenerated.
Review-minutes: 2
Unattended: ready
Epic: mass-field
Phase: 5
Blocked-by: phase 3 (`draft/docs/workspaces/mass_field_workspace_sweep.md`) merged (which itself waits on the PyAutoGalaxy/PyAutoLens release)
Filed: 2026-09-17

Fifth phase of `draft/feature/autogalaxy/mass_field_epic.md`. Re-scoped
2026-09-17 on the human's ruling that the user-facing API is `fields=`
everywhere (no shear or other field on a `Galaxy` in any workspace script):

- `HowToLens`: every galaxy-attached `ExternalShear` (23 files: chapter 1 ×1,
  chapter 2 ×5, chapter 3 ×10, chapter 4 ×1, optional ×1, simulators ×5) moves
  to `al.MassField` in `fields=` by phase 3's idiom table; the chapter-2
  tutorial that introduces the shear teaches the field as its own model object.
  Committed datasets are bit-identical and are not regenerated.
- `autolens_assistant`: wiki / skill pages that describe model composition or
  quote `shear=af.Model(al.mp.ExternalShear)` on a galaxy; re-provenance edited
  wiki bodies.
- `autolens_workspace_test` was folded into phase 3 on 2026-09-17 (its one
  legacy regression script is phase 3's deliverable) and is not in scope here.

If the grep is empty for a repo, record that in the PR and skip it.
