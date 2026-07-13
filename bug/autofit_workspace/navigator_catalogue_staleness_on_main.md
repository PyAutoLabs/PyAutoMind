# autofit_workspace navigator catalogue is stale on main (navigator_check CI red)

Type: bug
Target: autofit_workspace
Repos:
- autofit_workspace
Difficulty: easy
Autonomy: safe
Priority: low
Status: formalised

`autofit_workspace` main has been failing the `navigator / Catalogue staleness` CI check
(PyAutoBuild's reusable `navigator_check.yml`) since at least 2026-07-12 — a pre-existing
broken window, independent of any dataset work. Surfaced 2026-07-13 while merging the Group B
dataset purge (PyAutoBuild#151, autofit_workspace#92): that PR's navigator check was red, but
autofit main itself was already red (failures at 09:14–09:20 on 2026-07-13), and the catalogue
(`workspace_index.json`, `llms*.txt`) does not reference `dataset/`, so the purge was not the
cause.

Fix: regenerate the navigator catalogue via PyAutoBuild's generate tooling and commit the
refreshed `workspace_index.json` / `llms*.txt` (same class as the earlier autofit_workspace#87
fix — it recurs when scripts change without a catalogue regen). CAUTION (per prior experience):
a full regen can surface unrelated drift (e.g. `multi/features` notebooks); stage only the
navigator-catalogue files, revert incidental churn. Verify `navigator_check` goes green on main.

Note the recurrence: consider whether the catalogue should be regenerated automatically in
`pre_build` / a pre-commit so it cannot drift on main again.
