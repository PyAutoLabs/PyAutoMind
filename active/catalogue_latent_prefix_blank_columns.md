# Catalogue producers request latents with a retired `latent.` prefix, columns silently blank

Type: bug
Target: euclid_strong_lens_modeling_pipeline
Repos:
- euclid_strong_lens_modeling_pipeline
Difficulty: small
Autonomy: safe
Priority: high
Status: formalised
Consequence: judge
Witness: `lens_mass.csv` rebuilt from the ten `euclid_dr1_prelim` 342398 `vis_pix` zips has 0 blank cells in its 42 columns, and a fixture-based test asserts no blank column in `lens_mass.csv` and `magnitudes.csv`.
Review-minutes: 15
Unattended: ready
Filed: 2026-09-10
Issued: 2026-09-10

## Symptom

Catalogue producers in `euclid_strong_lens_modeling_pipeline` request latent variables with a
retired `latent.` prefix, so the columns come out silently blank.
`catalogue/scripts/lens_mass.py:248` requests `argument="latent.effective_einstein_radius"` and
`catalogue/scripts/magnitudes.py:320-327` requests eight
`latent.total_*_flux*_mujy` / `latent.magnification` arguments.

Since PyAutoLens's LATENT_FUNCTIONS registry landed (368f2920e 2026-05-23, 05945d1a3
2026-06-09) latent keys are bare (`effective_einstein_radius`, `total_lens_flux_mujy`, ...);
PyAutoFit's AggregateCSV looks a latent up by its own name and `Column.value` returns None on
KeyError, so each stale argument is a silent blank.

## Measurement

Measured on the ten dr1_prelim tiles of RAL job 342398 (euclid_dr1_prelim science project,
2026-09-10): the five `effective_einstein_radius*` columns of `lens_mass.csv` are blank on 10/10
rows while the other 37 columns are populated; 48 of the 52 columns of `magnitudes.csv` would be
blank once the SED chain lands. The June 2026 reference catalogue had these populated because the
old clone's `util.py` LATENT_KEYS named the latents with the prefix. Proven fix: with the bare
name a zip-only rebuild gives 0 blank columns out of 42.

## Do

1. Drop the prefix in both producers.
2. Rewrite the docstrings at `lens_mass.py` ~230-243 and `magnitudes.py` 279-289, which teach
   that the `latent.` prefix "is what selects" the latent
   (`workflow/example/csv/magnitudes.py:116-119` already states the correct bare-name convention).
3. Also fix `workflow/example/csv/lens_mass.py:192-198`, which requests shear `gamma_0`/`gamma_1`
   (a dead path, `ExternalShear` has `gamma_1`/`gamma_2`) under the names
   `mass_ell_comps_0`/`1`.
4. Add a test that builds `lens_mass.csv` from a small result fixture and asserts no blank column.

## Science follow-up

After merge, in the `euclid_dr1_prelim` science project, rebuild the catalogue from the 342398
results and re-score the Cortex task `euclid_dr1_prelim/ordered_rerun_catalogue_parity` before the
SED chain is submitted. The 3-sigma latent columns stay wrong until the separate PyAutoFit
`aggregate_csv` fix lands.

Related: `draft/bug/autofit/aggregate_csv_latent_sigma3_and_silent_none.md` (the 3-sigma /
silent-None half) and `draft/bug/autolens/vis_lp_mge_stage_writes_no_latents.md` (the vis_lp stage
that writes no latents at all).
