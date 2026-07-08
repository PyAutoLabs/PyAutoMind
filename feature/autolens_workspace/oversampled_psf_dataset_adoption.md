# Adopt oversampled PSFs in the start-here dataset chain (option a)

Type: feature
Target: autolens_workspace
Repos:
- autolens_workspace
Difficulty: large
Autonomy: supervised
Priority: normal
Status: formalised

Option (a) of the phase-4 fork (PyAutoLabs/PyAutoArray#362, decided
2026-07-08): flip the executed start-here simulator to
`convolve_over_sample_size=2`, save the fine-resolution `psf.fits`, and
update every loader of that dataset chain so examples stay exactly
self-consistent. Deliberately its own prompt because the survey found
**76 scripts auto-load the start-here dataset and 127 call
`Imaging.from_fits`** — this is a loader-migration project, not a kwarg flip.

## Scope

1. `scripts/imaging/simulator.py`: executed simulation at s=2 (fine
   `from_gaussian` PSF, adaptive radial evaluation via the k×s coupling —
   already library-supported); saved `psf.fits` at the fine resolution.
2. **Loader migration**: every script loading the start-here `simple`
   dataset passes `convolve_over_sample_size_lp=2`,
   `convolve_over_sample_size_pixelization=2` (and relies on `from_fits`'s
   default `psf_pixel_scales = pixel_scales / s`). Survey first: enumerate
   the exact loader list (~76) and any that reuse the psf for other
   purposes; migrate mechanically; the diff is wide but shallow.
3. Feature-dataset simulators stay s=1 in this prompt — stage them as
   follow-ups per dataset chain once the start-here pattern is proven.
4. Re-baselining: any script or smoke entry pinning numbers against the
   start-here dataset re-baselines in the same PR; navigator catalogue
   regenerated.
5. autolens_workspace_test / autogalaxy_workspace parity: survey whether
   their scripts load the start-here dataset (they mostly self-simulate);
   fix any that do.

## Risks

- Wide mechanical diff — review by sampling + full smoke subset run, not
  line-by-line.
- Notebook regeneration (PyAutoBuild) must follow the merged scripts.

## Sequencing

Builds on `oversampled_psf_visible_input.md` (the option-c visible-input
pass, user-refined 2026-07-08): with the knob exposed everywhere at 1, this
prompt becomes "flip the exposed values to 2 + save the fine psf.fits" plus
the re-baselining survey.

## Sequencing (original)

After the k×s series completes (phase 3 workspace tests + refactor
exercise). The k×s machinery it depends on is merged (PyAutoArray#363,
PyAutoGalaxy#486, autolens_workspace#236).
