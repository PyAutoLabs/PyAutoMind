# Inject stage: synthetic-source injection into real HST calibrated frames

Type: feature
Target: pyautoreduce
Repos:
- pyautoreduce
Difficulty: medium
Autonomy: safe
Priority: normal
Status: formalised

Phase 1 of the simulated-data-through-the-pipeline verdict
(PyAutoReduce#44, `docs/design/simulate.md`): an opt-in `inject` stage
between `acquire` and the combine path for the HST/ACS `astrodrizzle`
route.

Take an arbitrary input image (plain FITS, surface-brightness units +
pixel scale/position — no PyAuto* imports), render it onto each real
calibrated `_flc` frame's native grid through the frame's own
WCS/distortion, convolve with that frame's PSF (tier-1 frame ePSF,
adapter model-PSF fallback), convert to native units via the adapter,
add the source's own Poisson noise, write modified frame copies, then
run the existing pipeline unchanged (align → drizzle → noise → psf →
package). Real cosmic rays / sky / correlated noise come free from the
host frames (Balrog-style SSI). `reduction.json` must carry an explicit
`injected:` block.

Validation: injection-recovery on a SLACS host field — flux in vs
packaged cps out within the parity tolerances.

Open questions to resolve in planning are listed in `simulate.md`
§"Open questions" (input WCS contract, pre-convolved-input guard,
Poisson seeding, frame_products manifest flag, saturation clipping).

<!-- filed 2026-07-16 by the simulate-injection-feasibility research task (PyAutoReduce#44), per the roadmap convention: phase prompts are filed as their predecessor ships -->
