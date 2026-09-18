# euclid pipeline: `skip_fit_output` docs say it gates the whole of `save_results`, but the smoke run still writes wcs.json and coolest.json

Type: maintenance
Target: euclid_strong_lens_modeling_pipeline
Repos:
- euclid_strong_lens_modeling_pipeline
Themes:
- euclid
- docs
Difficulty: low
Autonomy: safe
Priority: low
Status: draft
Consequence: glance
Witness: Either `AGENTS.md` and `catalogue/README.md` no longer claim `skip_fit_output` gates the whole of `save_results` (and say what it does gate), or a test proves the gate by asserting no `wcs.json`/`coolest.json` is written under `PYAUTO_SKIP_FIT_OUTPUT=1`.
Review-minutes: 3
Filed: 2026-09-16

Found on 2026-09-16 while adding `files/coolest.json` (PyAutoLens#739 pipeline leg): a
`python3 .github/scripts/run_smoke.py` run under the smoke profile (`PYAUTO_SKIP_FIT_OUTPUT=1`,
`PYAUTO_TEST_MODE=2`) wrote both `wcs.json` and `coolest.json` for every stage. `AGENTS.md`
and `catalogue/README.md` both state that `skip_fit_output` "gates the whole of `save_results`",
which no longer holds.

## Scope

- Establish which of the two is intended: `save_results` writing its records in test/smoke mode
  (cheap, and the run-level tests rely on it), or the documented gate. Fix the one that is wrong,
  most likely the two doc statements.
- If the gate is meant to hold, add a test that proves it; if not, delete the claim (do not
  document the trap).
