# COOLEST: fix the empty Observation pixel grid, emit coolest.json from the Euclid pipeline by default, carry it into euclid_dr1

Type: feature
Target: PyAutoLens
Repos:
- PyAutoLens
- autolens_workspace
- euclid_strong_lens_modeling_pipeline
Themes:
- coolest
- interop
- euclid
Difficulty: medium
Autonomy: supervised
Priority: high
Status: formalised
Consequence: judge
Filed: 2026-09-16
Issued: 2026-09-16

## Request (verbatim)

> Hi Aaron,
> The models and results for the 3,000 DR1 lenses described in ECLIPSE C are here: Next week I'm planning to model the full DR1 sample (~15,000 lenses). I've also added COOLEST outputs to PyAutoLens, which are described here:
> https://github.com/PyAutoLabs/autolens_workspace/blob/main/scripts/guides/coolest_interop.py
> These aren't included in the 3,000 models above. it's a new feature that I'll use for the full run next week.
> The COOLEST guide and the conversion code above are fairly vibe-coded and have had less human oversight than I'd normally like. If you could take a look and confirm that everything makes sense before I blitz through the full DR1 sample next week, that'd be massively appreciated!
>
> Hey James,
>
> I just wanted to let you know that I checked out the COOLEST conversion code. I noticed one small problem with the json it created. In the "observation/pixels" attribute, "field_of_view_x(/y)" and "num_pix_x(/y)" are all automatically set to 0. It appears that the al.interop.coolest.to_coolest() imports an empty COOLEST Observation object with these values preset to 0.
>
> When I try to plot with these values in the COOLEST api, however, COOLEST doesn't know how to handle them. After editing the values in the json so that they result in a pixel scale equal to the one found in the "instrument" attribute, COOLEST makes a nice-looking plot. This was the only issue I was able to find so far!
>
> Can you 1) Check and fix the issue Aaron brought up; 2) ensure COolest is supported documenting and working on the euclid_strong_lens_modeling_pipeline, dont make it front and centre but ensure runs output coolest by default and that the bottom of the README.md mentions this with citation this includes ensuring its output as a .json file when we do catalogue generation; 3) Add Coolest support to the euclid_dr1 science project and ensure its in the catalogue, if it isnt already!

## Scope

1. **PyAutoLens** — `to_coolest` builds a `PixelatedRegularGrid` for `lazy.Observation` from
   `shape_native` + `pixel_size` (or a `dataset=`), warns when no grid is given, and gains
   `on_unsupported="skip"` which exports the mass model plus any Sersic light and records the
   omitted components (MGE `Basis`, pixelized source) under `meta.skipped_profiles`. Tests.
2. **autolens_workspace** — the COOLEST guide passes a pixel grid and documents the skip policy;
   notebook regenerated.
3. **euclid_strong_lens_modeling_pipeline** — every search writes `files/coolest.json` from
   `save_results` (guarded like `wcs.json`, missing package is a logged warning); the
   inspection bundle collects `coolest.json` / `coolest_sersic.json`; README gains a final
   "COOLEST output" section with the Galan et al. 2023 JOSS citation and `autolens[coolest]`
   in the install line; unit + slow tests.
4. **euclid_dr1 science clone** (after the pipeline PR merges) — merge pipeline main, add
   `hpc/batch_cpu/submit_reload_coolest`, ledger page; RAL reload leg on the human's go.

Decision (user-confirmed at planning): unsupported light/source components are **skipped and
recorded**, not converted. Pixel-grid export (MGE → `PixelatedRegularGrid`, pixelized source →
`IrregularGrid`) is the follow-up prompt `draft/feature/autolens/coolest_pixel_grid_export.md`.
