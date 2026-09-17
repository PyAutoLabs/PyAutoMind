# Output the multi-band astrometric offsets (DatasetModel grid_offset) with errors to the catalogue

Type: feature
Target: euclid
Repos:
- euclid_strong_lens_modeling_pipeline
Themes:
- euclid
- catalogue
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: active
Consequence: judge
Witness: astrometric_offsets.csv row for Tile102005065.../nir_h reproduces model.results grid_offset_0 = 0.0160 (0.0132, 0.0195) 1σ, (0.0069, 0.0261) 3σ
Review-minutes: 15
Unattended: needs-slicing
Filed: 2026-09-17
Issued: 2026-09-17

## Original request (verbatim)

Ensure that astrometric offsets inferred in multiwavelength fits (E.g. the DatasetModel
values) are output and in catalogue. This basically means that after we do the multi band
fitting after the sersic_initial_fit across the NISP and EXT data in the euclid strong lens
modeling piepline and euclid_dr1 results, that the offset we infer for each fit (which is
the only 2 free parameters of each fit via DatasetModel) is output to the catalogue (e.g.
euclid_dr1/catalogue). I think we do want errors included on this. This is not something I
think we have any exampel scripts or code to do yet and thus needs to be implementred but
carefully tested. Begin working on it, which I guess means you may need to work with a full
multiband fit in  euclid strong lens modeling piepline which in turn means you need to move
the right dataset over? You can see the right fits on which to base these results (e.g.
/mnt/c/Users/Jammy/Science/euclid_dr1_prelim/output_sed/dr1_prelim_grade_ab/Tile102005065RA0135279431487DECNEG0701599765928/sersic_lens_model)

## Context (from the 2026-09-17 survey)

- The per-band fits are `scripts/lens_model_waveband.py::fit_waveband`, run by the SED chain
  `scripts/sersic_lens_model_waveband.py` under `PYAUTO_OUTPUT_DIR=output_sed`. The only free
  parameters are `dataset_model.grid_offset.grid_offset_0/1` (arcsec, uniform prior ±0.2").
  Each band's result zip already carries them in `files/samples_summary.json` (median,
  max-LH, 1σ/3σ values and errors) — e.g. nir_h of the reference tile:
  `grid_offset_0 0.0160 (0.0132, 0.0195)`, `grid_offset_1 0.0070 (0.0054, 0.0097)` at 1σ.
- No catalogue producer reads them. `catalogue/scripts/magnitudes.py` walks exactly the
  right results (one row per (lens, waveband) under `unique_tag=sersic_lens_model`) and is
  the sibling to mirror; `catalogue/README.md` documents the 18 bundle files / 8 stages.
- `Science/euclid_dr1` and `Science/euclid_dr1_prelim` are both clones of this repo;
  `euclid_dr1_prelim/output_sed/dr1_prelim_grade_ab/` has completed multi-band results
  (NISP + DECam) for 9 tiles (~9 MB per tile) and the datasets (~1 MB per tile) — copy
  one tile in for a real-data witness.
- `tests/test_catalogue_latent_columns.py::test_every_non_model_argument_is_a_latent_key`
  only admits `galaxies...` model paths; a `dataset_model...` argument needs that test
  extended, not bypassed.
- Rule 2 of `tests/test_repo_invariants.py`: a new `catalogue/scripts/*.py` must be listed
  in `config/build/no_run.yaml` with a reason (as the other producers are).
