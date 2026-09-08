# dataset.fits written twice per search (files/ and image/): write once, always, to image/

Type: bug
Target: autogalaxy
Repos:
- PyAutoGalaxy
- PyAutoLens
- autolens_workspace
- autogalaxy_workspace
Themes:
- output
- aggregator
- hygiene
Difficulty: small
Autonomy: safe
Priority: medium
Status: active
Consequence: judge
Review-minutes: 15
Unattended: ready
Filed: 2026-09-08
Issued: 2026-09-08
Issue: https://github.com/PyAutoLabs/PyAutoGalaxy/issues/608

Since PyAutoGalaxy#479 / PyAutoLens#574 (2026-07-08, fix for #478) every imaging and
interferometer search writes `dataset.fits` twice: `AnalysisImaging.save_attributes` /
`AnalysisInterferometer.save_attributes` write `files/dataset.fits` unconditionally via
`paths.save_fits`, and the plotter interface writes an identical `image/dataset.fits`
gated on `visualize/plots.yaml` `dataset.fits_dataset`. Spotted in a
`euclid_strong_lens_modeling_pipeline` `vis_lp` output folder; it is generic library
behaviour, not a pipeline one.

User request (verbatim): "I do not want duplication and I want dataset.fits to always be in
image, so I guess the unconditional writing should just put it there? To be honest it sounds
like we pretty much dont allow a user to not output the dataset.fits, which is fine but yeah
avoid duplication."

## Facts

- `autofit.aggregator.SearchOutput._outputs_by_suffix` already scans both `files/` and
  `image/` for `.fits`, so `fit.value(name="dataset")` resolves `image/dataset.fits` with
  no aggregator change.
- `autolens_workspace/scripts/guides/results/start_here.py` already documents and reads
  `image/dataset.fits` — `image/` is the user-facing location.
- The ellipse plotter writes `image/dataset.fits` unconditionally and has no `files/`
  twin; it is not duplicated today.
- `DatabasePaths.save_fits` stores fits in the database. Writing directly to
  `paths.image_path` (as the plotters already do) means the database route no longer
  receives `dataset` — which is the pre-July behaviour, not a new gap.

## Deliverable

- Skip the write when `image/dataset.fits` already exists (user, 2026-09-08: "we should save a bit
  of time ... whereby it does not overwrite a new dataset.fits if one exists"), so a resumed
  search does not rewrite it.

- Single unconditional `image/dataset.fits` write in `save_attributes` (Galaxy + Lens
  imaging; Lens interferometer; Galaxy interferometer if it has the same pair).
- Remove the `fits_dataset`-gated plotter writes and the `fits_dataset` key from the
  packaged `plots.yaml` (PyAutoGalaxy, PyAutoLens) and the workspace copies.
- Update the two `save_attributes` regression tests to assert `image/dataset.fits`, and
  the plotter tests that assert the gated write.
