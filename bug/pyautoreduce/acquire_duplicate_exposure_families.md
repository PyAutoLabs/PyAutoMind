# acquire downloads duplicate exposures (HAP + standard-cal product families)

Type: bug
Target: pyautoreduce
Repos:
- PyAutoReduce
Difficulty: medium
Autonomy: safe
Priority: normal
Status: resolved — fixed by PyAutoReduce PR #18 (merged f4a4824, 2026-07-09)

PyAutoReduce acquire downloads duplicate exposures: download_exposures (autoreduce/acquire/mast.py) filters MAST products by productSubGroupDescription=FLC then globs all *_flc.fits — MAST delivers both the HAP family (hst_<prop>_<visit>_..._flc.fits, GAIA-aligned) and the standard cal family (<ipppssoot>q_flc.fits) for the same exposures, so the same photons are stacked twice (slacs1430+4105: 8 files = 4 unique exposures, EXPTIME doubled to 4256s). Fix: dedupe by exposure identifier (ipppssoot), preferring the HAP product when both families are present; add a unit test with a fabricated file list. Also audit whether slacs0008-0004's 7-exposure production run (issue #2) contained duplicates. Found during the slacs1430 validation (issue #17), where the duplicate set was worked around by cache-manifest surgery.

<!-- formalised by the Intake (Conception) Agent on 2026-07-09 from user-intake -->
<!-- resolved 2026-07-09 by the frame-products session (issue #16 / PR #18), which hit
the same bug independently on slacs0008: is_direct_observation now rejects all hst_*
HAP obs_ids, is_direct_product filters the product table + download glob, frames
packaging fails loudly on duplicate ROOTNAMEs, and a usability screen drops failed
0-second exposures. DESIGN DELTA vs this prompt: the fix keeps the DIRECT cal family
and drops HAP copies (consistent with the align stage's a-priori-WCS design), not
prefer-HAP-as-suggested — that choice, plus the slacs0008 audit (confirmed: acceptance
mosaics drizzled 3 exposures twice; parity re-measured in the hst_acs_pipeline.md
addendum) and regeneration of pre-fix reductions, is tracked in
research/pyautoreduce/acceptance_noise_rebaseline.md.
NOTE for slacs1430 (#17): its cache-manifest surgery workaround is superseded — evict
and re-acquire on main to get the filtered download path. -->
