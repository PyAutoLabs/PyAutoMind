## inject-stage-hst-imaging
- issue: https://github.com/PyAutoLabs/PyAutoReduce/issues/46
- completed: 2026-07-16
- library-pr: https://github.com/PyAutoLabs/PyAutoReduce/pull/47 (squash 59beb04d4)
- Phase 1 of the simulate.md verdict (#44): opt-in inject stage — Balrog-style synthetic-source injection into real calibrated HST _flc frames. Five default-off TargetSpec inject_* dials; autoreduce/inject/imaging.py (flux-conserving render through each frame's own WCS via standalone drizzle, per-frame tier-1 ePSF convolution, ELECTRONS[/S] contract, seeded Poisson to SCI + variance to ERR, work-dir copies only); _inject hook + loud HST-astrodrizzle-only gate; INJECTED header stamp + reduction.json inject block; 23 new tests (suite 229/3skip).
- Trap: the standalone drizzle kernel preserves SURFACE BRIGHTNESS, not flux — output sums scale by (scale_in/scale_out)²; render_to_chip applies the WCS pixel-area ratio to restore flux semantics. Caught by the flux-conservation test on first run.
- Shipped through unrelated Heart RED on contemporaneous user ack (re-asked: drift count changed 2→4 vs the prior task's list).
- Open: first real-data injection-recovery run on slacs0008 (prototypes/inject_recovery_slacs.py) — launched post-merge, result on #46.
- Follow-ups filed in simulate.md phasing: JWST+Keck injection (phase 2), ALMA simobserve (phase 3).

## Original prompt

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
