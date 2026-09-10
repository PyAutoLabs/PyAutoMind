# autofit_assistant: a skill that owns loading the user's data and its selection cuts

Type: feature
Target: autofit_assistant
Repos:
- autofit_assistant
Themes:
- assistants
Difficulty: small
Autonomy: safe
Priority: medium
Consequence: notify
Witness: a new `skills/af_load_data.md` (name open) is registered in `skills/README.md` and cited from `af_adapt_to_domain` (interview step 2) and `af_wrap_likelihood`; running the start-here Part 2 on `dataset/sne_cosmology/` records the column meanings, units and every selection cut (e.g. `is_calibrator == 0`, `z_hd > 0.023`) in `wiki/project/` with a one-line justification each, before the data-inspection gate fires.
Filed: 2026-09-10
Parent: complete/2026/09/start-here-mode.md

Found during the start-here-mode dry run (autofit_assistant#38): no skill owns
**loading the user's data and the selection cuts applied to it**.
`af_adapt_to_domain` covers papers, likelihood and model; `af_wrap_likelihood`
only asks in passing how the data are loaded; the data-inspection gate fires
*after* loading. In the Part-2 dry run on `dataset/sne_cosmology/` the two
consequential science decisions — parsing the CSV columns and the
`is_calibrator == 0`, `z_hd > 0.023` cut — had no skill guiding or recording
them. `modes/start_here.md` P0 mitigates with one sentence (state every cut
back and record it); the skill is the real fix.

## Scope

- @autofit_assistant/skills/af_load_data.md: read the user's format (CSV /
  FITS / HDF5 / npy / JSON) into the arrays the Analysis takes; name units and
  column meanings; surface every selection cut and its scientific justification
  back to the user; record both in `wiki/project/` (profile "data shapes" +
  dated entry). Python-first per `_style.md`; the data-inspection gate follows
  immediately.
- Register in `skills/README.md` (Domain adaptation) and `.claude/skills/`
  symlink; cite from `af_adapt_to_domain` and `af_wrap_likelihood`.
