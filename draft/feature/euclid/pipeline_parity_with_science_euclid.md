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
| Full SLaM | — | `scripts/full_model.py` | keep; see the Delaunay question below |
| MGE lens only | — | `scripts/mge_lens_only.py` | keep or justify |

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

## The Delaunay question — put this to the user before changing meshes

The request says `full_model.py` should "use Delaunay and mirror the Delaunay SLaM on
the autolens_workspace". Two facts contradict the premise:

- `euclid_strong_lens_modeling_pipeline/scripts/full_model.py` currently uses
  `RectangularAdaptImage` / adaptive-rectangular meshes (see its SOURCE PIX docstrings
  and `mesh_pixels_yx = 28`), not Delaunay.
- `autolens_workspace/scripts/guides/modeling/slam_start_here.py` — the canonical
  workspace SLaM — uses `RectangularBilinearAdaptDensity` (init, line ~611) and
  `RectangularBilinearAdaptImage` (main, line ~620). **There is no Delaunay SLaM in
  autolens_workspace to mirror.**

So: ask the user whether they want (a) `full_model.py` switched to Delaunay meshes, (b)
`full_model.py` brought into line with the workspace's *rectangular* SLaM as it actually
exists, or (c) a Delaunay SLaM authored in autolens_workspace first. Do not guess.
Note that the rectangular default was itself a deliberate decision (PyAutoArray#153).

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
- The Delaunay question has an explicit user decision recorded, not an assumption.
- Gates phases 2, 3 and 4.
