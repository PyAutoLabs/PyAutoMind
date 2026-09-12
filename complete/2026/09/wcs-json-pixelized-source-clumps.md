## wcs-json-pixelized-source-clumps
- issue: none — asked for directly in session as the follow-up to `wcs-json-lensed-source-images`
- completed: 2026-09-12
- workspace-pr: https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/pull/72 (merge `d82fd428`)
- repos:
  - euclid_strong_lens_modeling_pipeline
- summary: `files/wcs.json` now covers a pixelized source (`vis_pix`, the Delaunay
  stages). `util.wcs_dict_from` takes the max-likelihood `fit`; when the source
  plane is a `Pixelization` it finds the reconstruction's bright clumps with
  `Inversion.source_clumps_from` at the library's `subplot_mappings` defaults
  (threshold 0.5 × max, ≥ 3 mesh pixels, 5 brightest — PyAutoArray#517, the
  `image-source-mappings` epic phase 1) and reads each clump's multiple images
  off the fit's mapper as connected image regions (`Inversion.mappings_from`),
  reported as the brightest model pixel per region. Written as `source_clumps`
  (peak, peak value, mesh pixels, images in arcsec and RA/Dec, brightest first).
  The solver keys (`source_centre_*`, `lensed_source_image_*`) are filled by
  solving the lens equation for the brightest clump's peak mesh pixel, so they
  mean the same thing for every stage. Simulated lens: peak 0.004" from the
  truth source centre, solver images within 0.035" of `truth["positions"]`,
  mapper images within 0.13" (data pixels).
- decision: **two routes, both kept.** The solver keys are the sub-pixel
  lens-equation solution for one point; the mapper keys are data pixels of every
  clump and can merge two images into one arc or split one across a critical
  curve. A consumer wanting "where to point a fibre" reads the mapper route; one
  wanting "the multiple images of the source centre" reads the solver route.
- contract: the record never holds `None` (`output_to_json` drops it): an
  unavailable value is an absent key and an always-present `source_model`
  (`light_profile` / `pixelized` / `none`) says why. Both failure branches
  (clump finder, point solver) log and leave keys absent; `save_results` also
  tolerates a fit that cannot be rebuilt.
- tests: `tests/test_wcs_dict.py` 9 → 17 — a zero-free-parameter `vis_pix` fit
  (mesh mirrored from `test_compute_latent_variable.py`), the clump, its peak,
  both image routes and their sky positions vs `truth.json` and the header, the
  no-fit and clump-finder-failure branches; on-disk shape asserted through
  `al.output_to_json` + `al.from_json`, and a null-free invariant. Fast 112 → 120,
  slow 4 (also asserts `source_model`).
- trap: `Mapping.source_centre` is the **mean** of the clump's mesh pixel
  centres, not its peak; the record uses the argmax of the reconstruction over
  `pix_indexes` instead, which is what "the peak in the source plane" means.
- ci: as on #71, every pytest job on the PR reported `skipped` (the Heart
  smoke-gate gap, `draft/bug/pyautoheart/smoke_gate_skips_pytest_runners_on_pr.md`);
  merged on the local suites; the push to `main` runs the full matrix.
- session: web (session clone, no worktree, no `gh`, no Heart); the designated
  branch was restarted from `main` after #71 merged, per the merged-branch rule.
