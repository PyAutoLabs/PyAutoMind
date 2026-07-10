# wfc3_ir needs a DQ-bits dial (blob 512 zero-coverage holes on snapshot dithers)

Type: bug
Target: pyautoreduce
Repos:
- PyAutoReduce
Difficulty: medium
Autonomy: safe
Priority: normal
Status: formalised

PyAutoReduce wfc3_ir (and HST generally) lacks a DQ-bits dial: autoreduce/drizzle/combine.py drizzle_kwargs_for never sets final_bits/driz_sep_bits, so AstroDrizzle's default treats every DQ-flagged pixel as unusable. On WFC3-IR snapshot data (tiny dithers) detector-fixed DQ 512 blob regions then produce structured zero-coverage holes in the mosaic that the packaging guard (correctly) refuses: PJ011646 (program 14653, F160W, 5 exposures, 2-6 px dithers) failed with a single 123-px hole at r=5.3 arcsec, outside the 3.8 arcsec science mask, DQ 512 at the same detector pixels in all five exposures (validation issue #25). Standard IR practice passes 512 (blobs) and often 64 (warm px) as usable; Aris's trusted reduction of the same data has no hole. Fix: expose a bits dial on the adapter/TargetSpec (adapter default for wfc3_ir should include 512), document the choice + blob physics in docs/design/wfc3.md, unit-test drizzle_kwargs_for; also consider whether the packaging guard should distinguish defects inside vs outside the target's science aperture. The slacs1430-style validation script reduce_pj011646.py carries a documented monkeypatch workaround until this ships.

<!-- formalised by the Intake (Conception) Agent on 2026-07-10 from user-intake -->
