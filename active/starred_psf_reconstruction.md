# STARRED super-sampled ePSF back-end for PyAutoReduce

Type: research
Target: PyAutoReduce
Difficulty: medium
Autonomy: supervised
Priority: medium
Status: issued
Issue: https://github.com/PyAutoLabs/PyAutoReduce/issues/35

STARRED (STARlet REgularized Deconvolution; Michalewicz, Millon et al.,
COSMOGRAIL/EPFL; arXiv:2402.08725 = AJ 2024, JOSS 10.21105/joss.05340) is
named across the PSF tiering docs (HST `hst_acs_pipeline.md` Tier 3; JWST
`jwst.md` tier-3 row; Keck `keck_ao.md` Tier C) as a "high-fidelity
reconstruction back-end" for lensed quasars/AGN "where the point source itself
constrains the PSF." **Deep design research (2026-07-11) shows that framing is
wrong, and re-scopes the work substantially.** This prompt now carries the
resolved design; implementation follows from it.

## Design research findings (2026-07-11)

STARRED is two separable capabilities that fall on **opposite sides** of the
reduction / modelling boundary (arXiv:2402.08725, §2.1 vs §2.4/§3; full-text
verified):

1. **PSF reconstruction** — takes a set of **field-star** cutouts (HST worked
   example: 6 stars, §3.2), *standalone and science-target-agnostic* (§2.1:
   PSFs "constructed from stars in the field of view," built before the target
   is touched), runs **single-epoch** (per-epoch inverse problem; multi-epoch
   only to track variation, not required). Output is a **super-sampled narrow
   PSF** = analytic Moffat core + ℓ1-starlet-regularised pixel residual grid,
   Nyquist-sampled (Eq. 2, FWHM ≈ 2 px in the deconvolved frame). **No lens
   model, no science target, no `autolens` — its input is the same field-star
   sample the shipped Tier-1 photutils ePSF already selects** (`psf/stars.py`).
2. **Two-channel deconvolution / light-curve extraction** — decomposes the
   *target* into a point-source channel + an extended channel; the extended
   channel is a **generic starlet-regularised pixel grid with no physical
   model** (Eq. 9, explicitly *not* a lens/galaxy model). This is a
   science-analysis/photometry step, not a reduction product.

**Consequences that rewrite the plan:**

- **Question 0 (reduction vs modelling) is resolved.** STARRED's PSF step is
  squarely reduction-stage: it is a **higher-fidelity, super-sampled ePSF built
  from field stars** — a drop-in upgrade/alternative to Tier-1, not the exotic
  "reconstruct the PSF from the lensed images" method the doc imagined. The
  two-channel deconvolution of the target is out of reduction scope. So of the
  two contradicting design docs, **`keck_ao.md` was right** ("a *modelling-stage*
  concern, out of reduction scope") and **`hst_acs_pipeline.md`'s Tier-3 wording
  is misleading** and should be corrected when this lands (see below).
- **The Tier-3 taxonomy is wrong and must be fixed.** STARRED (PSF from stars)
  and PSFr (Birrer — genuinely reconstructs the PSF from the *science* point
  sources, iterative, modelling-adjacent) are **not the same kind of tool** and
  should not be lumped as co-equal "Tier-3 back-ends." STARRED's reduction-side
  contribution is really **Tier-1b: a super-sampled ePSF back-end**, parallel to
  the photutils Tier-1, fed by the same `psf/stars.py` selection.
- **Licensing is a hard constraint.** STARRED is **GPL-3.0-or-later** (copyleft;
  gitlab.com/cosmograil/starred/LICENSE) while PyAuto* are permissive. It can
  therefore only be an **optional extra**, imported only when the user selects
  that PSF back-end, isolated so it never imposes GPL on PyAutoReduce's core —
  exactly the optional-back-end pattern `psf/fallback.py` already establishes.
- **JAX is a hard constraint.** STARRED "heavily depends on jax" (autodiff +
  optional GPU). PyAutoReduce unit tests are numpy/astropy-only (AGENTS.md
  boundary), so STARRED runs in `prototypes/` / integration only, behind
  `pytest.importorskip` — the same exception the standalone `drizzle` resampler
  already uses. Its JAX pin must not collide with the workspace JAX story
  (manageable because it is optional and isolated).

## Re-scoped plan

The boundary question is answered; what remains is one real technical problem
plus the packaging. In order of information per hour:

1. **Drizzle-consistency — THE open technical question.** STARRED emits a
   super-sampled, Nyquist PSF in a "deconvolved frame"; the PyAutoReduce
   invariant is that the delivered PSF is the *drizzled* PSF (same kernel,
   pixfrac, scale, orientation as the mosaic — `psf/__init__.py`). Work out how
   to bring STARRED's super-sampled Moffat+starlet PSF onto the mosaic grid
   consistently — resample/rebin to the mosaic scale, or the `frame_combine.py`
   route (build STARRED PSFs per frame in native pixels, then drop-convolve +
   WCS-Jacobian resample). This is the crux; validate on a real ACS field
   against the Tier-1 photutils ePSF on a residual metric.
2. **Optional back-end seam.** Wire STARRED behind an optional interface
   mirroring `psf/fallback.py` — inputs: the `psf/stars.py` star cutouts + an
   initial Moffat guess; outputs: the two modeling kernels (`psf.fits` 21×21,
   `psf_full.fits` 61×61, odd/centred/unit-normalised, drizzle-consistent);
   provenance fields recording the STARRED version, star count, regularisation.
   GPL-isolated optional dependency group `pyautoreduce[starred]`; import lazily.
3. **Spike placement.** Feasibility spike lives in `prototypes/` (JAX allowed
   there); reuse an existing star-rich ACS mosaic already reduced by the
   pipeline so the only new variable is the PSF back-end.
4. **Doc correction (deliverable, not optional).** When this lands: rewrite the
   `hst_acs_pipeline.md` Tier-3 paragraph — STARRED becomes **Tier-1b
   (super-sampled ePSF from stars)**; the "point source constrains the PSF /
   PSFr-style reconstruction of the target" strand is separated out and marked
   modelling-stage per `keck_ao.md`. Mirror into `jwst.md`/`keck_ao.md` rows.

## Out of scope (record, do not build here)

- STARRED's **two-channel deconvolution / light-curve extraction** of the
  lensed quasar/AGN — a modelling/science-analysis step, not a reduction
  product; PyAutoReduce ships the inputs (cutouts + the STARRED PSF) and stops.
  PyAutoLens has no imaging-deconvolution path today either (its point-source
  route is image positions/flux-ratios; imaging fits take the PSF as a fixed
  convolution kernel), so this is genuinely un-owned future science work.

## References

- STARRED — arXiv:2402.08725 (AJ 168, 2024; IOP 10.3847/1538-3881/ad4da7);
  JOSS 10.21105/joss.05340. Repo gitlab.com/cosmograil/starred (docs
  cosmograil.gitlab.io/starred, v1.4.3); **GPL-3.0-or-later**; deps jax/numpy/
  scipy/matplotlib. Key sections: §2.1 PSF-from-N-stars, Eq. 2 Moffat+starlet,
  §2.4/Eq. 9 two-channel (starlet extended channel, no physical model).
- Boundary precedent: `keck_ao.md` Tier C (reconstruction = modelling-stage);
  the mistaken framing: `hst_acs_pipeline.md` Stage 5 Tier 3.
- Seams to mirror: `psf/fallback.py` (optional back-end + provenance contract),
  `psf/frame_combine.py` (drizzle-consistency machinery), `psf/stars.py` (the
  shared star selection that also feeds STARRED).
- Not needed for SLACS-style galaxy-galaxy lenses; the payoff is a
  higher-fidelity PSF for demanding (quasar/AGN, weak-lensing-grade) work.
