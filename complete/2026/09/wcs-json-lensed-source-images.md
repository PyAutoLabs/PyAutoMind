## wcs-json-lensed-source-images
- issue: none — asked for directly in session (no Mind prompt; recorded at close-out so the trap below is findable)
- completed: 2026-09-12
- workspace-pr: https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/pull/71 (merge `214db2aa`)
- repos:
  - euclid_strong_lens_modeling_pipeline
- summary: `util.AnalysisImaging.save_results` wrote `files/wcs.json` with only the
  max-likelihood lens light centre on the sky (`crval_ra_deg` / `crval_dec_deg` —
  the fitted centre, not the cut-out's reference pixel, despite the name — plus
  `crpix_x` / `crpix_y`). It now also records the source light centre in the
  source plane and the lensed source's multiple images in image-plane arcsec and
  RA / Dec: the lens equation solved for that centre with `al.PointSolver` at the
  simulator's own settings (`pixel_scale_precision=0.005`,
  `magnification_threshold=0.1`), so on `dataset/simulated/euclid_dr1_like` the
  images replay `truth["positions"]` bit for bit. Built by a new module-level
  `util.wcs_dict_from` (+ `source_centre_from`, `lensed_source_image_positions_from`)
  so it is testable without a search; a solver raise is logged and the image
  lists left empty rather than losing a finished search to its record. For
  `vis_lp` the centre is the MGE `Basis`'s shared centre; a pixelized source
  (`vis_pix`) has no light centre and gets no source keys.
- tests: `tests/test_wcs_dict.py` (fast, JAX-free): lens centre vs the simulated
  header's CRVAL/CRPIX; images vs `truth["positions"]`; every sky value by hand
  against the header's north-up CD matrix; MGE-basis centre; pixelized and
  solver-failure branches. `tests/test_latent_run_level.py` (slow): the real fit
  writes the record with four finite images, read back through `al.from_json`.
  Fast 103 → 112, slow 3 → 4.
- trap: **`output_to_json` drops every `None`.** PyAutoFit's dictable envelope
  (`{"type": "dict", "arguments": {...}}`, lists as `{"type": "list", "values":
  [...]}`) omits `None`-valued keys on write, so the "fixed schema with `null`
  for a pixelized source" this PR documented never reaches disk — `vis_pix`
  gets the four lens keys only. Found while probing nested round-trips for the
  follow-up; the follow-up (pixelized-source clumps via the mapper) restates
  the contract as *absent when unavailable* with an always-present
  `source_model` key, and fixes the README wording. Never test on-disk shape
  with `json.dumps`; go through `output_to_json` + `al.from_json`.
- trap: **positive `y` is south.** PyAutoArray loads FITS without a row flip, so
  native row 0 is FITS row 1 and PyAutoLens's +y is the FITS row-1 direction —
  south on a north-up CD matrix. Sky values are right because they go through
  the FITS pixel; a raw `y_arcsec` must not be read as "north of the lens". A
  1.4e-9 deg residual against the small-angle formula is the gnomonic cross
  term at Dec −51, not a sign error.
- trap: **test mode writes no `wcs.json` at all.** `skip_fit_output()` gates the
  whole of `save_results` (`abstract_search.py:617`), so a `PYAUTO_TEST_MODE`
  run cannot prove the write; only the slow real-mode fit can.
- ci: every pytest job on the PR reported `skipped` — the Heart smoke-gate gap
  already filed as `draft/bug/pyautoheart/smoke_gate_skips_pytest_runners_on_pr.md`
  (a `util.py` + `tests/` + docs diff changes nothing under `scripts/`,
  `config/` or `.github/`). Merged on the local fast + slow suites, as pipeline
  #65 and #67 were; the push to `main` runs the full matrix.
- session: web (session clone, no worktree, no `gh`, no Heart); PR opened and
  merged through the GitHub MCP surface.
