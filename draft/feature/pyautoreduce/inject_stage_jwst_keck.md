# Inject stage phase 2: extend synthetic-source injection to JWST and Keck frames

Type: feature
Target: pyautoreduce
Repos:
- pyautoreduce
Difficulty: medium
Autonomy: safe
Priority: normal
Status: formalised

Phase 2 of the simulated-data verdict (`docs/design/simulate.md`;
phase 1 = PyAutoReduce#46/PR#47, merged and recovery-validated on
slacs0008 at ratio 0.971). Extend `autoreduce/inject/` beyond the HST
`astrodrizzle` path:

- **JWST** (`jwst_image3` backend): inject into the `_cal` frames.
  Units differ structurally from HST — native MJy/sr surface brightness,
  no EXPTIME division (`_injection_units_factor` currently rejects
  MJY/SR loudly, by design); the adapter should own the e-/s → MJy/sr
  conversion (PHOTMJSR / pixel area). ERR propagation must follow the
  same units. Note the noise path reads propagated ERR (`rms.
  noise_map_from_error`), so the injected variance must be added to the
  frame ERR *before* image3 resamples it.
- **Keck** (`nirc2_native` backend): inject into the pipeline's own
  *prepared* frames (electrons, running-sky-subtracted) — the injection
  hook may need to move after `_ground_prepare` for the KOA path, or
  inject into prepared copies. Registration is offset-based, not WCS
  (the combine measures phase-correlation offsets), so `render_to_chip`
  needs the offset+distortion pixmap route (reuse
  `drizzle/nirc2_combine.build_pixmap`) rather than `all_world2pix`.
- Relax the `reduce_target` phase-1 gate per backend as each lands;
  extend `test_inject.py` with per-backend unit contracts; validate with
  injection-recovery on the existing JWST (COSMOS-Web ring) and Keck
  (B1938+666) anchors, prototypes-style.

Traps recorded in phase 1 (see `complete/2026/07/inject-stage-hst-imaging.md`):
the standalone drizzle resampler preserves surface brightness, not flux
(`render_to_chip` applies the WCS pixel-area ratio — revisit for the
offset-pixmap route); the combine chdir breaks relative cache paths
(always absolute).

<!-- filed 2026-07-16 on user request, per the simulate.md phasing (phase 1 merged same day) -->
