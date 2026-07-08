# PyAutoReduce phase 3: JWST/NIRCam via the COSMOS-Web ring (all four bands)

Type: feature
Target: PyAutoReduce
Difficulty: large
Autonomy: supervised
Priority: normal
Status: formalised

User instruction 2026-07-08 (--auto): extend PyAutoReduce to JWST/NIRCam,
validated on a **COSMOS-Web top-grade lens** — the COSMOS-Web ring
(RA 150.10048, Dec +1.89301; Mercier et al. 2024, arXiv:2309.15986; source
z=5.104) — in **F444W first, then extended to all four COSMOS-Web bands**
(F115W, F150W = SW channel; F277W, F444W = LW channel), since the
autolens_assistant demo dataset (`dataset/imaging/cosmos_web_ring/wavebands/`)
carries modeling-ready products for all four (SW at 0.03″/pix 419², LW at
0.06″/pix 209², stripped headers) — a four-band parity anchor.

Scope (roadmap "JWST (NIRCam first)" section):
- **nircam_sw + nircam_lw adapters**: level-2 `_cal` products
  (calwebb_image2 output, MJy/sr), combination via `jwst` calwebb_image3
  (tweakreg/skymatch/outlier_detection/resample — the drizzle analogue),
  JWST CRDS server (adapter must carry observatory/CRDS-server — a phase-3
  generalization of the HST-hardcoded acquire stage).
- **Combine-backend dispatch**: stage 3 currently calls drizzlepac
  unconditionally; adapters gain a backend concept (astrodrizzle | jwst_image3)
  — the altitude work of this phase.
- **Noise**: i2d products carry ERR/VAR_POISSON/VAR_RNOISE/WHT — stage 4
  becomes read + resample-consistency check per the roadmap; document units
  decision (MJy/sr vs e-/s conversion) against the demo dataset's convention.
- **PSF**: tier-1 ePSF from mosaic stars where present; STPSF (WebbPSF)
  as the model back-end (this phase may implement it as the first tier-2
  since JWST PSFs are the standard use case; judgment gate if heavy).
- **Env**: `jwst` pipeline installed into ~/venv/PyAuto under the existing
  constraints (astropy 6.1.2 pins); blocker escalated if the resolver fights.
- Integration: reduce the ring in all four bands from MAST `_cal` exposures;
  parity vs the assistant demo products (sub-pixel registered ratios, like
  the SLACS study); SW vs LW output scales matching the demo (0.03/0.06).
- Design doc `docs/design/jwst.md` + roadmap tick; unit tests numpy/astropy
  only; ACS+WFC3 regression suites stay green.

Acceptance: four-band reductions complete end-to-end; parity ratios vs demo
products reported per band; the pixfrac/scale dials and diagnostics
(WHT uniformity, correlated-noise reporting) work through the jwst backend.
