# Test-mode representative outputs — Phase 4: docs

Type: feature
Target: autofit
Repos:
- PyAutoFit
Difficulty: small
Autonomy: supervised
Priority: normal
Status: formalised

Phase 4 of 4 of `draft/feature/autofit/test_mode_representative_outputs_size_realistic.md`.
Blocked until phase 2 is merged. Minimal-docs discipline applies: flag/value plus a
one-line note wherever `PYAUTO_TEST_MODE` is already documented — no new ported
runnable blocks.

## Scope

- Survey first: find where `PYAUTO_TEST_MODE` levels are currently documented
  (@PyAutoFit docstrings/RTD, autofit_workspace cookbooks) and add
  `PYAUTO_TEST_MODE_SAMPLES` there in the same register, including the default-4
  back-compat and the `output/test_mode/` namespacing note.
- Record the representativeness limits (phase 1 D4) alongside: timing-honest,
  not science-honest.
- If the survey finds no existing library-side test-mode docs surface, say so on the
  issue and fold the residue into phase 3's README rather than inventing a new docs
  page — then close this phase as absorbed.

## Ship

`ship_library` (docs-only PR) or close-as-absorbed per the survey outcome.
