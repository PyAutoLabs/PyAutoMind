# acquire downloads duplicate exposures (HAP + standard-cal product families)

Type: bug
Target: pyautoreduce
Repos:
- PyAutoReduce
Difficulty: medium
Autonomy: safe
Priority: normal
Status: formalised

PyAutoReduce acquire downloads duplicate exposures: download_exposures (autoreduce/acquire/mast.py) filters MAST products by productSubGroupDescription=FLC then globs all *_flc.fits — MAST delivers both the HAP family (hst_<prop>_<visit>_..._flc.fits, GAIA-aligned) and the standard cal family (<ipppssoot>q_flc.fits) for the same exposures, so the same photons are stacked twice (slacs1430+4105: 8 files = 4 unique exposures, EXPTIME doubled to 4256s). Fix: dedupe by exposure identifier (ipppssoot), preferring the HAP product when both families are present; add a unit test with a fabricated file list. Also audit whether slacs0008-0004's 7-exposure production run (issue #2) contained duplicates. Found during the slacs1430 validation (issue #17), where the duplicate set was worked around by cache-manifest surgery.

<!-- formalised by the Intake (Conception) Agent on 2026-07-09 from user-intake -->
