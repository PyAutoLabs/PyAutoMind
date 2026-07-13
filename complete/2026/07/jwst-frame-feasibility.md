## jwst-frame-feasibility
- completed: 2026-07-10
- issue: https://github.com/PyAutoLabs/PyAutoReduce/issues/24 (closed)
- pr: https://github.com/PyAutoLabs/PyAutoReduce/pull/26 (merged dfa0d96, squash; docs-only)
- summary: JWST per-frame feasibility answered — GO, phased. Should: strongest case = NIRCam SW undersampling (subpixel dithers exist to recover what mosaics destroy) + Roman multi-epoch-beats-coadd shear benchmarks + correlated-noise removal; tempered by mosaic-based published practice (we'd lead the field) and raw 1/f/wisp/snowball artifacts at frame level (recorded caveat). Can: 7 modest deltas (crf capture, MJy/sr branch, BKGLEVEL sky, ramp-jump+outlier CR provenance no deepCR, gwcs target_pixel, peak_max=None ePSF + STPSF tier-2b, guard relax). Design note in docs/design/jwst.md; user accepted GO ("go --auto")
- followups: feature/pyautoreduce/jwst_frame_products.md filed (scoped to the 7 deltas, COSMOS-Web ring anchor)
