# Re-baseline the slacs0008 acceptance parity after the HAP-dedupe fix

Type: research
Target: pyautoreduce
Repos:
- PyAutoReduce
Difficulty: small
Autonomy: supervised
Priority: normal
Status: formalised

Filed from the frame-products validation session (issue #16 / PR #18,
2026-07-09), which found the MAST acquire stage had been ingesting HAP
visit-level FLC copies (every exposure drizzled twice → IVM weights doubled
→ noise underestimated by √2) plus one failed 0-second exposure. Both fixed
on the frame-products branch; the acceptance-era parity numbers (issue #2:
data 0.941 / noise 0.925) were measured on the buggy mosaics.

Re-measured post-fix (recorded in the hst_acs_pipeline.md parity-appendix
addendum): data ratio 0.959, noise ratio 1.309, and the corrected map is
internally consistent (blank-sky map/empirical = 1.45 vs applied R = 1.36).
The flipped inference: legacy SLACS noise maps sit at our *uncorrected* IVM
noise level — they do not appear to carry the Casertano correlated-noise
correction, contrary to the spike-era conclusion drawn from √2-suppressed
maps.

Task: formally re-baseline the acceptance comparison —

1. Re-run the parity study on 2-3 SLACS systems with the corrected acquire
   stage (dedupe + usability screen), updating the parity-appendix table
   from its duplicated-input numbers.
2. Settle the legacy-noise stance: if legacy maps are R-free, decide and
   document whether our ~30%-higher chi²-faithful noise maps are the
   accepted product (lens-model error bars shrink relative to legacy fits)
   or whether an R-free compatibility mode is worth exposing.
3. Check whether any downstream modeling dataset already reduced with the
   duplicated-input pipeline needs regenerating (any target reduced before
   2026-07-09; cached targets carry duplicates until evicted).
