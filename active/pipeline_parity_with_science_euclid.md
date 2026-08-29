# Pipeline parity: port the DR1 analysis from Science/euclid into euclid_strong_lens_modeling_pipeline

Type: feature
Target: euclid
Repos:
- euclid_strong_lens_modeling_pipeline
- PyAutoLens
Themes:
- euclid
- pixelization
Difficulty: large
Autonomy: supervised
Priority: high
Status: formalised
Epic: euclid-dr1-prep
Phase: 1
Parent: draft/feature/euclid/euclid_dr1_prep_epic.md
Filed: 2026-08-28
Issued: 2026-08-29

Phase 1 of 10 in the Euclid DR1 preparation epic. **Blocks phases 2, 3 and 4.**

User request (verbatim):

"""
1) Firstly, we need to set up the repo "euclid_strong_lens_modeling_pipeline" to make it a first class repo which is
representative of the complete DR1 analysis. This includles:

- Compare to the code and setup in /mnt/c/Users/Jammy/Science/euclid and make sure all of the following funtctionality
can be done in this repo:

- Fit using an initial lens model (e.g. intial_lens_model.py).
- Fit which goes on to use single Sersic model (e.g. sersic_lens_model.py).
- Fit whcih then does multi wavelenght lens model for all NIR / EXT data (e.g. lens_model_waveband.py) and ensure
that this also has a way or option to follow on the single sersic fits (sersic_lens_model_waveband.py).
- Parity on util.py, making sure it has all the PSF_FWHM_WORST stuff and all latent variables.
- Look at catalogue/catalogue/dr1_prelim_grade_ab_catalogue_csvs_20260623/Tile102005065RA0135279431487DECNEG0701599765928e
and make sure all the files in catalogue/scripts required to make its contents (e.g. deblending.py, lens_mass.py, magnitdes.py)
are available and clean and documented in "euclid_strong_lens_modeling_pipeline", be extra careful with pairing here.

Be extra careful to ensure the lens model parameterization uses that in /mnt/c/Users/Jammy/Science/euclid, whic had
some polished upgrades and bug fixes which probabl didnt make their way into "euclid_strong_lens_modeling_pipeline" .

In general, /mnt/c/Users/Jammy/Science/euclid was used to do science without updating "euclid_strong_lens_modeling_pipeline" 
so if there is drift take /mnt/c/Users/Jammy/Science/euclid as a source of truth. full_model.py is definitely ok
and hsoul dbe kept on "euclid_strong_lens_modeling_pipeline" make sure its using Delaunay and mirrors the Delaunay SLaM on the autolens_worksapce
in terms of what it fits.

Documentation on all this stuff is pretty good, but make sure its cleaned up and high quality without stuff
missing where possible.
"""

## Drift rule

`/mnt/c/Users/Jammy/Science/euclid` is the **source of truth**. Where the pipeline repo
disagrees, the science tree wins — it carries the polished parameterization upgrades and
bug fixes from the real DR1 runs. The exception the user names explicitly:
`full_model.py` lives only in the pipeline repo and is kept.

## Script checklist (surveyed 2026-08-28)

`Science/euclid/scripts/` has 15 scripts; the pipeline repo's `scripts/` has 5
(`full_model.py`, `initial_lens_model.py`, `lens_model_waveband.py`, `mge_lens_only.py`,
`sersic_lens_model.py`). Work each row:

| Capability | Science/euclid | pipeline repo | action |
|---|---|---|---|
| Initial lens model | `scripts/initial_lens_model.py` | present | diff + port parameterization |
| Single-Sersic follow-on | `scripts/sersic_lens_model.py` | present | diff + port |
| Multi-waveband (NIR/EXT) | `scripts/lens_model_waveband.py` | present | diff + port |
| Sersic → multi-waveband follow-on | `scripts/sersic_lens_model_waveband.py` | **ABSENT** | port (the request calls this out by name) |
| Pixelized Sersic variants | `sersic_lens_model_pix.py`, `sersic_lens_model_pix_waveband.py`, `multi_lens_model_pix_waveband.py` | **ABSENT** | decide: port, or fold into the above as options |
| Galaxy-only Sersic | `scripts/galaxy_sersic_model.py` | **ABSENT** | decide |
| Latent diagnostics | `diagnose_latent.py`, `diagnose_latent_vis_pix.py` | **ABSENT** | port — phase 2 needs these |
| Full SLaM | — | `scripts/full_model.py` | keep; switch to Delaunay per user decision below |
| MGE lens only | — | `scripts/mge_lens_only.py` | keep (user decision) |

Also absent from the pipeline repo but present in the science tree:
`build_inspect.py`, `build_inspection_bundle.sh`, `audit_sed_outputs.py`,
`audit_unresolved_hpc.sh`, `reorganize_normies.py`. Triage these — some are one-off
operational scripts that need not be public.

## util.py parity

`Science/euclid/scripts/util.py` is 978 lines; the pipeline repo's root `util.py` is 699.
Functions present in the science tree and **missing** from the pipeline repo:
`_find_local_maxima`, `_pixel_to_arcsec`, `_compute_positions_from_source_flux`,
`psf_fwhm_arcsec_from_primary_header`. Port them, and diff the shared functions
(`subplot_rgb`, `ab_mag_via_flux_from`, `flux_mujy_via_ab_mag_from`,
`aperture_flux_from`, `dataset_instrument_hdu_dict_via_fits_from`, `load_vis_dataset`,
`parse_fit_args`) line by line — the science tree's versions carry the bug fixes.

**Correction to the request:** there is no `PSF_FWHM_WORST` symbol anywhere in either
tree. The machinery the user means is the `WORST_BAND` / `WORST_PSF_*` FITS
primary-header handling in `Science/euclid/scripts/lens_model_waveband.py`
(lines ~70-90, ~256, ~298-312, ~489) plus
`scripts/util.py::psf_fwhm_arcsec_from_primary_header`. Port *that*.

## Catalogue-script pairing

The reference tile is
`/mnt/c/Users/Jammy/Science/euclid/catalogue/catalogue/dr1_prelim_grade_ab_catalogue_csvs_20260623/Tile102005065RA0135279431487DECNEG0701599765928`
(the trailing `e` in the request is a typo). It holds 13 files:

`lens_mass.csv`, `lens_sersic.csv`, `source_sersic.csv`, `magnitudes.csv`, `model.fits`,
`pre_psf.fits`, `fit_sersic.png`, `fit_multi_wavelength.png`, `rgb.png`,
`segmentation.png`, `vis_lp_fit.png`, `vis_lp_image_with_positions.png`,
`vis_pix_fit.png`.

Be **extra careful with the pairing**: for each of those 13 outputs, name the script in
`Science/euclid/catalogue/scripts/` that produces it, then make that script available,
clean and documented in the pipeline repo. The candidate producers are `deblending.py`,
`lens_mass.py`, `lens_sersic.py`, `source_sersic.py`, `magnitudes.py`, `lens_model.py`,
`multi_wavelength.py`, `validate_magnitudes.py` (27 files total in that directory,
including a large `plot_*.py` family and DR1-run-specific variants such as
`lens_mass_dr1_prelim_grade_ab.py` and `lens_mass_vis_pix_dr1_prelim_grade_ab.py`).
The pipeline repo currently has **no `catalogue/` tree at all**.

Do not bulk-copy all 27 — port the ones on the pairing path, plus whatever a user needs
to reproduce the bundle, and say explicitly which were deliberately left out and why.

## User decisions (2026-08-28, recorded verbatim-ish — these override the survey's open questions)

- **Delaunay:** "delaunay slam is part of delaunay.py on workspace". The Delaunay
  configuration to mirror is `autolens_workspace/scripts/imaging/features/pixelization/delaunay.py`
  (image mesh + Delaunay mesh + its regularization/interpolation choices). `full_model.py`
  switches to Delaunay meshes matching that script in *what it fits*, while keeping the
  Euclid-specific setup (bands, latents, PSF handling) it already has. Do not ask again.
- **Port scope is conservative:** "large drift expected and lots won't carry over — reduce
  down to what's needed to make results". Port only the scripts on the critical path to the
  catalogue results (initial → sersic → waveband → sersic_waveband, util.py latents/WORST_PSF
  machinery, the catalogue/scripts that produce the reference tile's 13 files, and the
  latent diagnostics phase 2 needs). Do **not** port the `_pix` variants, `galaxy_sersic_model.py`,
  or the operational one-offs (`build_inspect.py`, `audit_*`, `reorganize_normies.py`) —
  leave a short "not ported, available in Science/euclid" note in the docs instead.
  More can be added later.
- **`mge_lens_only.py`:** keep it in the pipeline repo ("include mge lens only").
- **Assistant routing (phase 4):** use the existing `euclid_*` skill family as-is, "with
  euclid stuff included" — no new `euclid_mode` is to be built.

## Deliverables

- Every capability in the checklist above reproducible from the pipeline repo.
- `util.py` at parity, with the WORST_BAND/PSF machinery and all latent variables.
- A `catalogue/` tree in the pipeline repo whose scripts demonstrably produce the
  13 reference-tile outputs, documented.
- Lens-model parameterization matching the science tree everywhere.
- A written drift report: what was ported, what was deliberately not, and why.
- Documentation cleaned up to high quality — no missing pieces where avoidable.

## Acceptance / gate

- A reader of the pipeline repo alone can run the full DR1 analysis chain end to end.
- For each of the 13 reference-tile files, a named script in the pipeline repo produces
  it, and that mapping is written down.
- `full_model.py` fits what `imaging/features/pixelization/delaunay.py` fits (user decision above).
- Gates phases 2, 3 and 4.
