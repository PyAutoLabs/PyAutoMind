# Upstream the DR1 final-catalogue tooling to the pipeline, with a vis_lp-only appendix for excluded tiles

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
Status: formalised
Consequence: glance
Witness: on pipeline main, the chunked build reproduces end to end on a 3-lens fixture split across output/ + output_sed/ (N=2 chunks, ARCHIVE=chunked, PARTS=2) yielding one merged CSV set, band_inventory.csv, lens_index.csv, excluded_tiles.csv and SHA256SUMS
Review-minutes: 3
Unattended: ready
Filed: 2026-10-07

## Relates to / proposed supersession

- Proposed to supersede issue #102 (unpushed branch `feature/vis-lp-inspection-bundle`, commit `c6b514d` — salvage only, see Ask 2) and issue #92.
- Folds in `draft/bug/euclid/bundle_sersic_products_read_output_dir_not_sed_output_dir.md` (fixed in the euclid_dr1 science clone by `126167b`, but not on pipeline main).
- **The human has NOT yet confirmed retiring #102/#92 or the folded draft bug.** Do not close or edit them from this task without that confirmation; this prompt only proposes it.

## Context

The DR1 SWG catalogue `dr1_catalogue_20261005` (chunk array RAL 397070, merge 397071, post-check 397074; 14,905 lenses, 98 excluded for lacking finished vis_lp + vis_pix) was built with tooling that exists only in the euclid_dr1 science clone (~50 unpushed commits ahead of pipeline main). Pipeline main lacks the chunked build, the merge/QA/distribution step, output_sed Sersic routing and the post-build check, so the documented pipeline cannot reproduce the delivered catalogue.

## Ask

1. **Port the generic tooling** (non-manifest, non-job-specific) from the science clone to pipeline main:
   - `126167b` — output_sed Sersic routing, `--datasets_file` selector, wcs/reconstruction collection, `deduplicate_deblending_fits.py`
   - `0ad3c49` / `ef9c5a2` / `62c1e0d` / `d2703bf` / `cec4a3e` — `hpc/batch_cpu/submit_catalogue_chunked.sh` + chunk/merge submitters, `scripts/tools/merge_catalogue.py`
   - `fd44569` — catalogue README
   - `3cdc179` / `a8e757b` — `build_image_catalogue`, `mass.csv`
   - `d313c0a` — `build_wcs_package`
   - `sed_completeness.py`
   - `scripts/tools/catalogue_post_build_check.py` (currently **uncommitted** in the clone)

   Leave run manifests and dated submit scripts in the science repo. Work by cherry-picking into a task worktree; **never edit the science clone**, which has another session's staged changes.
2. **From `c6b514d` keep only:**
   - the `--initial_search_name=vis_lp` mode in `build_inspect.py` (`coolest_vis_lp.json`, `vis_lp_`-prefixed deblended FITS);
   - the lens_mass fixed-centre fallback (`add_variable_with_fixed_fallback`);
   - `catalogue/CATALOGUE_ENTRIES_AND_METADATA.md`, reconciled with the edited untracked science copy and updated for the merged catalogue (grades / wcs / lens_index / QA files).

   Do **not** port `DATASET_NAMES_PATH` / `SERSIC_OUTPUT_DIR` / `TAR_TO` or the old submitter edits. Use the `${X[@]+"${X[@]}"}` form for empty arrays under `set -u`.
3. **Optional vis_lp-only appendix:** build the `excluded_tiles.csv` tiles with `INITIAL_SEARCH_NAME=vis_lp` into a separately named catalogue part, flagged in `lens_index.csv`.
4. **Post-build check** covers magnitude rows vs completed bands (the Tile102015606 dropped-VIS-row case) and lenses lacking `model.fits`.

## Acceptance witnesses

- Pipeline main reproduces the chunked build end to end on a 3-lens fixture split across two samples (output/ + output_sed/), N=2 chunks, ARCHIVE=chunked, PARTS=2: one merged CSV set, `band_inventory.csv`, `lens_index.csv`, `excluded_tiles.csv`, `SHA256SUMS`.
- A lens with `sersic_lens_model` only under output_sed yields lens_sersic/source_sersic rows, `fit_sersic.png` and `coolest_sersic.json` (closes the folded draft bug).
- vis_lp-only fixture (no vis_pix): `build_inspect` writes `vis_lp_fit.png` + `coolest_vis_lp.json` and no `coolest.json`; `lens_mass.csv` carries the fixed centre with equal median/bounds.
- `catalogue_post_build_check.py` flags a fixture lens with a completed VIS band but no VIS magnitude row.
- `diff -r` of the ported generic tools vs science-clone HEAD shows only intentional changes, listed in the PR.

## Unverified (record, do not assume)

- Live RAL state of jobs 397070 / 397071 / 397074.
- 350581 exit status — success is *inferred* from the local bundle `inspect/dr1_sep1_rest_vislp_full_20260923` and its 5 GB tar, not checked against SLURM.
- Whether vis_pix mass centres are also fixed (affects whether the fixed-centre fallback is vis_lp-only).
- RAL bash version (matters for the empty-array `set -u` idiom).

<!-- formalised by the Intake (Conception) Agent on 2026-10-07 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/ee9e30af-64fe-426d-ac1b-fc663fcd5a94/scratchpad/upstream_dr1_final_catalogue_tooling.md -->
