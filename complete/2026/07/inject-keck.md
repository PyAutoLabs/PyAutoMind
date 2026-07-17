## inject-keck
- issue: https://github.com/PyAutoLabs/PyAutoReduce/issues/54
- completed: 2026-07-17
- library-pr: https://github.com/PyAutoLabs/PyAutoReduce/pull/55 (squash 78ac5d303)
- Phase 2b of simulate.md: Keck prepared-frame injection, offset-based placement — offsets_to_reference pre-pass + mosaic_geometry (lifted from combine, shared) + target-at-mosaic-centre convention + frame-products pixmap inversion; NEVER raw header WCS. inject_position = offset-from-target. inject_psf REQUIRED (epoch-specific AO PSF; auto tier-A = follow-up). No ERR bookkeeping (keck noise constructed from mosaic downstream). Hook moved post-_ground_prepare for all paths (no-op for HST/JWST). render_via_pixmap shared core. Suite 250/3skip incl. placement-consistency property test.
- Design fact: consistently-placed injection leaves re-measured phase-correlation registration unchanged in expectation; recovery spike (B1938+666) includes the offsets with/without check.
- Trap: mosaic_geometry extraction initially dropped local ny,nx still used by combine — existing nirc2 combine tests caught it pre-commit (the witness working).
- OPEN validation: B1938+666 recovery run (needs KOA spec YAML + tier-A PSF candidate); COSMOS-Web JWST recovery run also still pending.
- Batched judgment items (validated at merge): inject_psf-required; offset-from-target semantics.

## Original prompt

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
