## keck-ao-reduction
- completed: 2026-07-09
- issue: https://github.com/PyAutoLabs/PyAutoReduce/issues/11 (closed)
- pr: https://github.com/PyAutoLabs/PyAutoReduce/pull/12 (merged 44a8d1a, squash)
- summary: Keck NIRC2 AO reduction live (phase 4) — KOA acquire seam, ground calibrate/sky stages, nirc2_native drizzle-pixmap combine, MCDS-aware noise, provisional-PSF epoch candidates; validated on SHARP I B1938+666 (closure 0.883, FWHM 72 mas, 110 tests); review gate 9 findings fixed
- followups: acceptance checks 3-4 (HST astrometry + PyAutoLens Einstein-radius invariance) and keck_ao.md open items — file as new prompts

## Original prompt

# Keck NIRC2 AO reduction — implement phases K1–K3

Type: feature
Target: PyAutoReduce
Difficulty: large
Autonomy: supervised
Priority: high
Status: formalised

Original request: "A large refactor of PyAutoReduce just merge in, so combine
that with this research to get keck-ao data reduction live --auto"

Implement the Keck NIRC2 AO reduction designed in PyAutoReduce#9 (research
task keck-ao-reduction-plan; full draft design + K1–K3 phasing on the issue),
building on the post-phase-3 consolidated layout (PR #10, merged 371721f).
Decisions adopted from the batched set on #9: drizzle-package combine
backend; B1938+666 (SHARP I) validation anchor.

Scope (the K1–K3 phases, one branch):

- Ship `docs/design/keck_ao.md` (the parked write leg of #9, adopting
  post-refactor module names) + `docs/design/roadmap.md` update.
- K1 — acquire + calibrate + sky: KOA/PyKOA acquire backend behind an
  archive seam; new calibrate stage (DN→e⁻, dark, flat, bad-pixel) and sky
  stage (temporally adjacent object-masked running sky) for ground-based
  data.
- K2 — dewarp + combine + noise: Yelda 2010 / Service 2016 distortion
  solutions as the pixel mapping through the `drizzle` package; registration
  by cross-correlation; first-principles noise map (sky + dark + read/coadds
  + Poisson, coverage-propagated, × Casertano R).
- K3 — PSF tiers + package + validation: provisional-PSF contract
  (candidate PSF-star products, `psf_provisional` provenance, AO-conditions
  block); unchanged `al.Imaging.from_fits` output contract; B1938+666
  validation per the four acceptance checks on #9 (internal closures, FWHM
  65–70 mas, astrometric parity vs HST, PyAutoLens fit reproduces the
  published Einstein radius).

Constraints: unit tests numpy/astropy-only (no network, no drizzlepac);
KOA/network work in `prototypes/` or scripts; FITS never committed; new deps
(pykoa, drizzle) via pyproject. Validation-with-real-data runs as a script
leg and its results are reported, not committed.
