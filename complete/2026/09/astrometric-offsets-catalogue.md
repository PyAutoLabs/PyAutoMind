## astrometric-offsets-catalogue
- issue: https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/issues/83
- completed: 2026-09-17
- workspace-pr: https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/pull/85 (merge 53f3c2322)
- summary: |
    The SED chain's per-band fits (`scripts/lens_model_waveband.py::fit_waveband`) have exactly two free
    parameters, the `DatasetModel` grid offset `(y, x)` of the band's grid relative to VIS in arcsec (uniform
    prior ±0.2"), and no catalogue producer read them. New `catalogue/scripts/astrometric_offsets.py` writes
    `astrometric_offsets.csv` as inspection-bundle stage 9/9: one row per (lens, waveband) with median,
    max-log-likelihood, ±1σ and ±3σ of `grid_offset_y` / `grid_offset_x`, plus the `lens_name`, `waveband`
    and `crval_ra_deg` labels `magnitudes.csv` carries. VIS results (no `dataset_model` in the model) are
    excluded via a `model.paths` filter rather than written blank; re-run bands de-duplicate to the newest
    result through `magnitudes.latest_result_per_lens_band`. The convention (offset subtracted from the
    band's grids, so +y means the band's sky lies +y arcsec from the VIS frame) is documented in the producer
    and `catalogue/README.md`. Wiring: bundle script (nine stages), `no_run.yaml`, `compare_catalogues.py`
    product registry, waveband-driver docstring, and the two top-level READMEs that still said seven stages
    / 13 files. Tests: header pin fixture, numeric known-answer test on a synthetic completed result tree
    (hand-built `SamplesSummary` over a `DatasetModel` model), VIS exclusion, empty-query survival; the
    latent-key invariant now admits `dataset_model.` paths.
- witness: |
    Real data, `Science/euclid_dr1_prelim/output_sed/dr1_prelim_grade_ab`: 64 completed results → 9 VIS
    excluded → 55 rows (nir_y/j/h × 9 tiles, decam_g/r/i/z × 7); every one of 55 × 12 value cells equals
    its zip's `samples_summary.json` exactly (max discrepancy 0.0). Reference row Tile102005065…/nir_h:
    grid_offset_y 0.01603864719489669, 1σ (0.013155106919663265, 0.019523833574959102), 3σ
    (0.006898507834378906, 0.02605318110413765) — the issue Witness. One band (nir_y) re-fitted with the
    branch: vis_lp/vis short-circuited, nir_y refit ~49 s, new median y 0.0095085 vs 09-11's 0.0091920,
    inside 3σ; with both zips present the producer keeps the newer one. Red control: disabling the filter
    fails the new test on an empty grid_offset_y cell. Fast suite 150 passed; smoke euclid 9/9.
- notes: |
    Heart RED at ship time (install-verify testpypi F, release-validation integrate fail — release-side,
    unrelated) acknowledged by the human typing /prm. CI on PR #85: Smoke Tests 3/3 green; Tests unit
    3.12/3.13 + slow 3.13 green, slow 3.12 RED = the filed drawer_pix InitializerException flake
    (draft/bug/euclid/drawer_pix_initializer_exception_flake.md, also red on main run 34677820679);
    merged over it on the human's explicit /prm authorisation ("i authorise you to override the red and
    continue"), not on a re-run. Two dr1_prelim rows sit at the ±0.2" prior edge
    (Tile102008165…/nir_j x = 0.19082, Tile102008219…/decam_g y = 0.19665): science QA flags, not producer
    faults. Follow-ups, not filed as prompts: pull the pipeline into `Science/euclid_dr1` and
    `Science/euclid_dr1_prelim` and re-run `scripts/build_inspection_bundle.sh` so the DR1 bundles gain the
    CSV (a Cortex action); `catalogue_util.py`'s docstring still says "six catalogue producers".

## Original prompt

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
