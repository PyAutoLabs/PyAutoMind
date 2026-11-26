Corrected the euclid pipeline docs that said `skip_fit_output` gates the whole of `save_results`. The code was right: PyAutoFit calls `analysis.save_results` at the end of every fit, including the test-mode bypass, so a smoke under `PYAUTO_SKIP_FIT_OUTPUT=1` / `PYAUTO_TEST_MODE=2` does write `files/wcs.json` and `files/coolest.json`. `skip_fit_output` gates the pre- and post-fit output around `save_results`.

- Workspace: https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/pull/144 (MERGED 2026-11-26, a1800a0)
- Issue: https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/issues/143 (closed)
- Shift: 2026-11-26-pm; tier glance; merged by the independent close-out session (Opus 5.5) after it ran the witness on head c6b9d66.
- Changes: `AGENTS.md` (two passages), `config/build/no_run.yaml` (`witt_wynne.py` reason), `tests/test_latent_run_level.py` (one docstring). No code changes.
- Witness held: neither `AGENTS.md` nor `catalogue/README.md` claims `skip_fit_output` gates `save_results`; `AGENTS.md` now says what it gates (checked against `abstract_search.py` lines 322/340/488/507).

## Follow-up (not filed)

`catalogue/README.md:102`, `catalogue/scripts/lens_mass_maps.py:74` and the `lens_mass_maps.py` line in `config/build/no_run.yaml` say `skip_fit_output()` is true "in every test mode"; it reads only `PYAUTO_SKIP_FIT_OUTPUT`, which the smoke profile sets.

## Original prompt

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
Verified: 2026-11-26 03f4718c (euclid_strong_lens_modeling_pipeline)
Lane: any
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
