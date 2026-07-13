# Chase the ~6% flux scale between PyAutoReduce and legacy SLACS reductions

Type: research
Target: PyAutoReduce
Difficulty: medium
Autonomy: supervised
Priority: low
Status: formalised

PyAutoReduce phase 1 (PyAutoReduce#2, PR #3) reduces slacs0008-0004 to data
ratio 0.941 / noise ratio 0.925 vs the legacy modeling dataset — both carry
the same ~6% global scale, so the products are internally self-consistent and
the difference was accepted as documented (design doc parity appendix,
decision 2026-07-08). This prompt tracks understanding it if it ever matters.

Bounded experiments, in order of information per hour:
1. Re-drizzle with `final_kernel='gaussian'` (SLACS IX used Gaussian) and
   re-measure the bright-pixel ratio — kernel-induced resolution difference is
   the cheapest hypothesis to kill.
2. Photometric-era check: legacy reductions predate CTE-corrected FLC and
   possibly current PHOTFLAM; reduce from `_flt` (no CTE correction) and
   compare — CTE correction should *raise* our flux, so if `_flt` closes the
   gap the era hypothesis wins.
3. Aperture (not pixelwise) photometry of the lens galaxy in both reductions —
   separates resampling/PSF effects from true throughput scale.
4. If none close it: sky-subtraction level comparison (`skymethod` variants).

Context: legacy reduction provenance is unrecoverable (stripped headers;
SLACS V used no-drizzle bilinear ACSPROC for snapshots, SLACS IX MultiDrizzle
gaussian for multi-exposure — slacs0008-0004 is the latter regime). Lens-model
inferences are scale-invariant in the relevant regime, hence Priority: low.
