# Inject stage phase 2b: Keck injection into prepared frames (offset-based registration)

Type: feature
Target: pyautoreduce
Repos:
- pyautoreduce
Difficulty: medium
Autonomy: supervised
Priority: low
Status: formalised

Phase 2b of the simulated-data verdict (`docs/design/simulate.md`).
Extend `autoreduce/inject/` to the Keck `nirc2_native` path — the hard
part is registration, and it needs a design decision before code:

- Inject into the pipeline's own *prepared* frames (electrons,
  running-sky-subtracted), so the hook moves after `_ground_prepare`
  for the KOA path.
- **Design question (resolve in planning): placement without WCS.**
  Raw NIRC2 header WCS is arcsecond-grade (tens of native pixels at
  0.01"/pix) — placing the source per frame via header WCS smears it
  across the stack. The frame-relative offsets that define registration
  are measured by phase correlation *inside* the combine
  (`nirc2_combine.offsets_to_reference`, a pure function over frame
  arrays) — injection can call it directly on the prepared frames to
  place the source consistently (reference-frame position from its WCS
  once, offsets thereafter), then render through the same
  distortion-as-pixmap route (`build_pixmap`), not `all_world2pix`.
  Confirm this two-pass shape (measure offsets → inject → combine
  re-measures on injected frames, where the injected source now also
  contributes to the correlation — assess whether that bias matters at
  typical injected fluxes).
- PSF: the tier-A PSF-star path ships per-epoch candidates; injection
  convolution should use the epoch-matched candidate (provisional by
  contract), else `inject_psf`.
- Validate with injection-recovery on the B1938+666 anchor.

<!-- filed 2026-07-16; split from inject_stage_jwst_keck.md (Feature Agent large/split); supervised: the registration design question is judgment-shaped -->
