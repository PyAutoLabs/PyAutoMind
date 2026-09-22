# Support vis_lp-only products in inspection bundles

Type: feature
Lane: local-dev
Autonomy: human-required
Target: @euclid_strong_lens_modeling_pipeline
Issued: 2026-09-22
Issue: https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/issues/102

## Original request (verbatim)

Ok this looks great, can you now have the same lenses also include the normal lens modeling results from vis_lp, we dont have vis_pix for these yet. If vis_lp doesnt work for this use case yet let me know

## Observed limitation

The completed `dr1_sep1_rest_sersic100_20260922` inspection bundle contains the
SED/Sersic products for 100 lenses. The main `output/dr1_sep1_rest` tree has a
completed `initial_lens_model/vis_lp` result for all of those same 100 lenses,
and no `vis_pix` results.

The current bundle cannot add those products correctly:

- `scripts/tools/build_inspect.py` skips all normal-model images unless both
  `vis_lp` and `vis_pix` exist.
- `lens_mass.py`, `lens_mass_maps.py`, and `witt_wynne.py` can read `vis_lp`,
  but `scripts/build_inspection_bundle.sh` does not expose a search-stage
  selection and defaults them to `vis_pix`.
- Pointing `OUTPUT_DIR` at the main tree would see 300 lenses, while this bundle
  must stay restricted to the same 100-lens SED sample.
- Existing multi-band FITS/CSV/PNG products must remain intact and idempotent.

## Requested outcome

Add an explicit `vis_lp`-only inspection mode that includes every scientifically
valid normal-model product available from `vis_lp`, clearly skips products that
fundamentally require `vis_pix`, and restricts the refresh to the lenses already
selected for the bundle. Add focused regression tests, then use the corrected
tooling to refresh the existing RAL bundle without rerunning any model fit and
pull the verified products locally.
