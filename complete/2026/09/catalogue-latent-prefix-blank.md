## catalogue-latent-prefix-blank
- issue: https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/issues/64
- completed: 2026-09-10
- workspace-pr: https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/pull/65
- summary: `catalogue/scripts/lens_mass.py` and `catalogue/scripts/magnitudes.py`
  requested their latents from `af.AggregateCSV` under a retired `latent.`
  prefix, so every latent column came out silently blank at full DR1 header
  width (5 of `lens_mass.csv`'s 42 columns on 10/10 dr1_prelim rows; 48 of
  `magnitudes.csv`'s 52 once the SED chain lands). The producers now name the
  latents bare, exactly as `util.LatentEuclid` writes them; both docstrings
  describe the real mechanism; the tutorial twin's dead shear path
  (`gamma_0`/`gamma_1` as `mass_ell_comps_*`) requests `gamma_1`/`gamma_2`.
- trap: autofit's `Row` merges the latent summary into the *same* kwargs dict as
  the model paths, under the bare keys the fit wrote, and `Column.value` turns a
  `KeyError` into `None` — a wrong `add_variable` argument is written blank, never
  raised. Header-only parity tests cannot see it; only a populated-cell check can.
- test: `tests/test_catalogue_latent_columns.py` (fast suite, ~3 s, no search, no
  JAX) writes a completed result tree with PyAutoFit's own serializers
  (`DirectoryPaths.save_all`, `save_samples_summary` for both the samples and the
  `latent/latent_summary` names, `completed()`), runs each producer's real
  `main()` over it and asserts no blank cell plus the DR1 header; a hermetic
  guard reads every `add_variable` argument out of the producers' syntax trees
  and requires each non-`galaxies.` one to be a `util.LatentEuclid` key. All four
  fail with the old arguments. Fast suite 89 → 93 passed serially.
- ci-gap: PyAutoHeart's reusable `smoke-tests.yml` skips the matrix on
  `pull_request` when no path under `scripts/`, `config/`, `.github/` or the
  smoke lists changed — even when the caller passes a pytest `runner`. This
  `catalogue/`+`workflow/`+`tests/` diff therefore ran no test on CI; merged on
  the human's call over the local run (five libraries' source mains); the push
  to `main` runs the full matrix. Filed: `draft/bug/pyautoheart/` (this close-out).
- pre-existing, not touched: `tests/test_util.py` drops one or two
  `FileNotFoundError` failures under `pytest -n auto` on `main` too; serial and
  CI (serial) are clean.
- out of scope: the 3σ latent bounds reading autofit's 1σ values —
  `draft/bug/autofit/aggregate_csv_latent_sigma3_and_silent_none.md`; the
  `vis_lp` stage writing no latents —
  `draft/bug/autolens/vis_lp_mge_stage_writes_no_latents.md`.
- science follow-up: rebuild the catalogue from the 342398 results and re-score
  the Cortex task `euclid_dr1_prelim/ordered_rerun_catalogue_parity` before the
  SED chain is submitted.
- session: web-github (session clone, no task worktree, no `gh`, no
  `pyauto-heart`); issue and PR driven through the GitHub MCP surface;
  implementation and ship delegated to execution-tier subagents.

## Original prompt

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
