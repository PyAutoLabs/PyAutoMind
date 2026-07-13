## jwst-frame-products
- completed: 2026-07-10
- issue: https://github.com/PyAutoLabs/PyAutoReduce/issues/27 (closed)
- pr: https://github.com/PyAutoLabs/PyAutoReduce/pull/28 (merged 7202e98, squash)
- summary: JWST frame products live — 7 feasibility deltas implemented (_crf capture+consume, native MJy/sr + derived manifest units, BKGLEVEL sky, ramp-jump+outlier CR provenance, DO_NOT_USE-only DQ policy [JUMP_DET = good data], filename-stem identity, peak_max=None ePSF, guard HST+JWST); manifest schema v2; registration reliability guard added after F115W validation exposed ~200px mask-geometry artifacts (best-covered reference, >20%-masked pairs flagged, headline needs a clean PAIR else null/UNMEASURED); COSMOS-Web F115W end-to-end: 6 chips, 3/6 tier-1 frame ePSFs, combined mosaic PSF from the 3; 194 tests; human-directed ship+merge ("ship it")
- followups: STPSF tier-2b (next, user-directed "lift PSF coverage"); gwcs target_pixel; duplicate frame-ePSF compute when both flags on

## Original prompt

# JWST frame products: extend frames/registration/PSF chain per the feasibility deltas

Type: feature
Target: pyautoreduce
Repos:
- PyAutoReduce
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: formalised

Implements the GO-phased verdict of `docs/design/jwst.md` §"Per-exposure
frame products — feasibility" (issue #24, merged dfa0d96) — the user
accepted the recommendation on 2026-07-10 ("go --auto"). Extend the HST
frames → registration → PSF chain (issues #16/#19/#21) to JWST/NIRCam,
scoped exactly to the seven deltas in that section:

1. Package the `_crf` outlier-flagged/tweakreg-updated products
   (`steps={"outlier_detection": {"save_results": True}}` in jwst_combine +
   path capture in drizzle provenance); `_cal` fallback with recorded
   absence.
2. Native MJy/sr units branch in `_units_to_cps` (record, don't convert).
3. Sky via skymatch `BKGLEVEL` (subtract + record; 0.0 when absent).
4. `cr_method = "ramp-jump (calwebb stage 1) + image3 outlier_detection
   (crf)"`; JWST DQ flag table in `dq_semantics`; no deepCR.
5. gwcs-anchored `target_pixel`; SIP-approx cutout WCS with recorded
   fidelity; registration block records tweakreg fit metadata (no
   RMS_RA/RMS_DEC equivalents); measured relative residuals unchanged.
6. Per-frame ePSF with `peak_max=None` (surface-brightness convention);
   STPSF as tier-2b; note that SW sampling recovery happens in the
   `psf_from_frames` combination across subpixel dithers, not in a single
   frame's ePSF.
7. Relax the HST-only guard to `observatory in ("hst", "jwst")`.

Validation anchor: the COSMOS-Web ring, all four bands (undersampled SW +
well-sampled LW in one dataset) via `scripts/reduce_cosmos_web_ring.py`.
Frame-level artifacts (1/f striping, wisps, snowballs) ship as recorded
manifest caveats, not blockers. ENV note: jwst pinned 1.14.0 in the venv;
image3 needs `in_memory=False` on this machine (OOM).
