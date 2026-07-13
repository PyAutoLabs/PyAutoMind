## keck-frame-products
- completed: 2026-07-10
- issue: https://github.com/PyAutoLabs/PyAutoReduce/issues/33 (closed)
- pr: https://github.com/PyAutoLabs/PyAutoReduce/pull/34 (merged, squash)
- summary: Keck frame products live — the #31 GO sequence executed: mapping constants (origin/scale_ratio/sci_path) into nirc2 provenance (offsets were ALREADY serialized — feasibility note corrected); frame-vs-stack outlier pass ships per-frame outlier_mask.fits (mask half of the stack CR open item; recombine second pass still open); package/keck_frames.py packages prepared frames as native e-/s stamps + constructed MCDS noise + offset-based registration (no WCS by design) + MJD-matched native tier-A PSF stamps from accepted epochs. B1938: 39/39 frames, target inversion 0.8px band across the dither pattern, ~0.4%/frame outliers, 39/39 PSF stamps. psf_from_frames stays HST/JWST-only (guard split). Plate-scale + #13 acceptance caveats ride the manifest. 202 tests; human-directed ship+merge
- followups: stack-level second-pass recombine using the new outlier masks; plate-scale fix owned by #13; frame chain now covers ALL THREE observatories on real data
