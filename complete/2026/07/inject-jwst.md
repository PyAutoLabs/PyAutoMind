## inject-jwst
- issue: https://github.com/PyAutoLabs/PyAutoReduce/issues/52
- completed: 2026-07-17
- library-pr: https://github.com/PyAutoLabs/PyAutoReduce/pull/53 (squash c7283f50e)
- Phase 2a of simulate.md: JWST _cal injection. Per-adapter input-units contract (InstrumentAdapter.inject_units): HST e-/s per pixel; JWST Jy per pixel via the frame's own PIXAR_SR — electrons_per_input × sci_per_electron reduces to 1/(PIXAR_SR·1e6), injected MEAN flux-exact and gain-free; nominal e_per_dn=2 sizes Poisson width only (disclosed in provenance units_note). _chip_units replaces the scalar factor; injected variance enters frame ERR before image3 resamples (the JWST noise stage reads propagated ERR). Gate = (hst,astrodrizzle)|(jwst,jwst_image3). Suite 246/3skip.
- Trap: review caught a REAL NameError — no-overlap injection referenced units_note before assignment; initialize loop-note vars before the loop. Regression test added.
- OPEN: COSMOS-Web recovery run (prototypes/inject_recovery_jwst.py, F150W prog 1727) never run — heavy (image3 twice); schedule with 2b validation.
- Next: phase 2b Keck (registration design: offsets_to_reference pre-pass, NOT header WCS) in flight; phase 3 ALMA simobserve in draft.

## Original prompt

# Inject stage phase 2a: extend synthetic-source injection to JWST _cal frames

Type: feature
Target: pyautoreduce
Repos:
- pyautoreduce
Difficulty: medium
Autonomy: safe
Priority: normal
Status: formalised

Phase 2a of the simulated-data verdict (`docs/design/simulate.md`;
phase 1 = PyAutoReduce#46/PR#47, merged and recovery-validated on
slacs0008 at ratio 0.971). Extend `autoreduce/inject/` to the JWST
`jwst_image3` path (`_cal` frames):

- Units differ structurally from HST — native MJy/sr surface brightness,
  no EXPTIME division (`_injection_units_factor` currently rejects
  MJY/SR loudly, by design). The adapter should own the flux → MJy/sr
  conversion (PHOTMJSR / pixel area per the _cal photometry headers);
  the Poisson realisation needs the electron-rate view of the same
  signal (document any nominal-gain approximation loudly in provenance).
- The JWST noise path reads propagated ERR (`rms.noise_map_from_error`),
  so the injected variance must be added to the frame ERR *before*
  image3 resamples it — same-units propagation as the SCI addition.
- Relax the `reduce_target` phase-1 gate for `jwst_image3`; extend
  `test_inject.py` with the MJy/sr unit contract; validate with
  injection-recovery on the COSMOS-Web ring anchor, prototypes-style.

Traps recorded in phase 1 (see `complete/2026/07/inject-stage-hst-imaging.md`):
the standalone drizzle resampler preserves surface brightness, not flux
(`render_to_chip` applies the WCS pixel-area ratio); the combine chdir
breaks relative cache paths (always absolute).

<!-- filed 2026-07-16; split from inject_stage_jwst_keck.md on the Feature Agent's large/split-into-phases sizing (JWST = units problem, Keck = registration problem) -->
