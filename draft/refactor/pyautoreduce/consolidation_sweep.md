# Consolidation sweep: mine PyAutoReduce for code-consolidation refactor opportunities

Type: refactor
Target: pyautoreduce
Repos:
- pyautoreduce
Difficulty: medium
Autonomy: safe
Priority: normal
Status: formalised

Run the refactor agent on PyAutoReduce and look for more opportunities to consolidate the code.

## Mined candidates (Refactor Agent + source survey, 2026-07-16)

Refactor Agent verdict: invariant = behaviour observable through
`PyAutoReduce/test_autoreduce` unchanged; API guard none-expected; autonomy
cap safe. Witness now registered in Brain policy (was a registry gap).

Ranked candidates from a read-only survey of `autoreduce/` (58 files, ~6.6k
lines):

1. **Move per-instrument conditionals in `pipeline.py` stage dispatchers onto
   `InstrumentAdapter`.** `_psf` branches on `adapter.observatory` to extract
   the max single-exposure time (HST `EXPTIME` vs Keck `ITIME`×`COADDS`) and
   the peak cap; `_noise`/`_combine` branch on `combine_backend` for the
   noise recipe / exptime requirement. That is instrument header knowledge
   living outside `instruments/`, straining the repo's own adapter-boundary
   contract ("no module outside `autoreduce.instruments` may name a
   detector"). Candidate methods: `adapter.single_exposure_seconds(header)`,
   a peak-cap hook, a noise-recipe selector. Direct payoff for the planned
   ground-based instrument feature (fewer if/elif chains to extend per new
   instrument).
2. **Consolidate the four private FWHM helpers** — `psf/epsf.py:_fwhm_of`
   (radial half-max), `psf/nirc2_star.py:_fwhm_arcsec` (equivalent-area),
   `psf/frame_combine.py:_moment_fwhm` and `psf/starred_epsf.py:_size_fwhm`
   (second-moment; these two are mathematically identical). At minimum merge
   the two second-moment copies into one shared `psf` helper; keep the other
   two only if their algorithmic difference is load-bearing, and say so where
   they live.
3. **Small tidy:** `noise/jwst_rms.py` (48 lines, one function) could fold
   into `noise/rms.py`; `mad_sigma` and friends in `noise/rms.py` are generic
   robust stats imported by `sky/`, `calibrate/`, `psf/` — a `stats` home
   would read better (cosmetic; only worth it riding along with #1/#2).

Checked and rejected as candidates: `mad_sigma` is already shared (no
duplicates); combine-backend dispatch is already centralised in
`drizzle/combine.py`; `package/frames.py` vs `package/keck_frames.py`
divergence is deliberate and documented in the keck_frames module docstring
(and they already share `MANIFEST_VERSION`/`frame_cutout_shape`).

<!-- formalised by the Intake (Conception) Agent on 2026-07-16 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/59a19942-c45f-4f2a-ad18-6bcc3dd8a7ba/scratchpad/chunk1_refactor.md -->
<!-- 2026-07-16: Refactor Agent run + candidate mining appended; difficulty small->medium (candidate 1 touches pipeline + adapter surface); autonomy supervised->safe per refactor work-type cap -->

