# Bundle stages 1/5/6 read OUTPUT_DIR, but the SED chain writes sersic_lens_model into SED_OUTPUT_DIR — the Sersic products never appear in a documented bundle build

Type: bug
Target: euclid
Repos:
- euclid_strong_lens_modeling_pipeline
Themes:
- euclid
- catalogue
Difficulty: small
Autonomy: supervised
Priority: medium
Status: draft
Consequence: glance
Witness: `build_inspection_bundle.sh dr1_sep1` on a tree whose sersic_lens_model results live in output_sed/ yields lens_sersic.csv (9 rows), source_sersic.csv, fit_sersic.png and coolest_sersic.json; today it yields none of them
Review-minutes: 3
Unattended: ready
Filed: 2026-09-17

## Observed

Seen 2026-09-17 building the `dr1_sep1` bundle in `Science/euclid_dr1` after SLURM array 343381 (the CPU
SED chain, `scripts/sersic_lens_model_waveband.py` under `PYAUTO_OUTPUT_DIR=output_sed`). The chain
writes `sersic_lens_model/vis` (and the bands) into `output_sed/<sample>/<tile>/`. `scripts/build_inspection_bundle.sh`
runs stages 1 (`build_inspect.py` → `fit_sersic.png`, `coolest_sersic.json`), 5 (`lens_sersic.py`) and
6 (`source_sersic.py`) against `OUTPUT_DIR` (default `output`), where the Sersic stage never lands, so
the bundle reports "no completed sersic_lens_model/vis results" and ships without `lens_sersic.csv`,
`source_sersic.csv`, `fit_sersic.png` or `coolest_sersic.json`. Run by hand with `--output_path=output_sed`,
`lens_sersic.py` and `source_sersic.py` produce 9 rows each — the fits are fine, only the wiring is wrong.
`euclid_dr1_prelim/inspect/dr1_prelim_grade_ab_342629/` has the identical gap, so this has been silently
true since the prelim run; `catalogue/README.md`'s "Fits the bundle expects" documents exactly this
three-command recipe, so the documented path cannot produce 4 of the 19 bundle files.

## Ask

Decide where the Sersic stage canonically lives (the SED chain's `output_sed`, since `sersic_lens_model.py`
run standalone is the exception, not the rule) and make stages 1, 5 and 6 read it from there — e.g. a
`SERSIC_OUTPUT_DIR` defaulting to `SED_OUTPUT_DIR`, or have stages 5/6 fall back to the SED tree when the
main tree has no `sersic_lens_model` results. Update `catalogue/README.md`'s producer table ("Upstream fit
it needs") and the env table, and add a fast test that a tree with `sersic_lens_model` only under the SED
directory still yields the four products (the `tests/test_catalogue_latent_columns.py` result-tree fixture
is the pattern).

## Evidence

- `Science/euclid_dr1/wiki/project/2026-09-17-sed-chain-sep1.md` ("Drift" section) and the bundle logs
  in the 2026-09-17 session scratchpad.
