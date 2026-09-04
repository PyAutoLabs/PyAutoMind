- issue: https://github.com/PyAutoLabs/PyAutoReduce/issues/61 + https://github.com/PyAutoLabs/PyAutoReduce/issues/62 (both CLOSED 2026-09-04 via /community — the reporter's own grid showed no erosion on well-dithered, correctly-aligned data, so the default stays STScI driz_cr and no default-flip decision remains pending; a degenerate-dither validation would be a new issue)
- library-pr: https://github.com/PyAutoLabs/PyAutoReduce/pull/66 (merged 2026-08-06, head 2168738e)
- shipped: 2026-08-06
- repos: PyAutoReduce
- tests: 265 passed / 15 skipped, up from the 246/15 baseline (+19, numpy/astropy-only house style). Re-verified on main (9955812) 2026-08-18: kwargs/dial suite 34/34, star-pass decoupling 4/4.
- record-note: reconciliation record (2026-08-18) — the implementation shipped from a `/wake_up` session branch (`claude/wake-up-q6ajyq`) without advancing this prompt out of `draft/`; this record closes that drift. No new code shipped with this record.

Community-reported (@samlange04, PyAutoReduce#61 + #62): AstroDrizzle's unconditional
`driz_cr=median=blot` stack rejection compares each frame against a blotted-median
reference that reads systematically low at steep gradients, so genuine core flux can
be flagged as CR — eroding deflector cores and holing field-star PSFs before
`find_stars` ever sees them. Shipped as PR #66: a user-facing CR-method dial plus the
decoupling of PSF-star measurement from the shipped science CR pass. **The science
default is unchanged** — flipping it stays human-gated on the SLACS validation.

## What shipped (PR #66)

- **`TargetSpec.cr_method: "driz_cr" (default) | "deepcr"`** (#61). `driz_cr` keeps
  byte-identical kwargs (pinned by regression test, including that no `resetbits`
  key appears). `deepcr` = per-frame CR masks (reusing `package/cosmic_rays.py`, the
  machinery frame products already run) written into each exposure's DQ as the
  AstroDrizzle CR bit 4096 via the pure, idempotent `dq_with_cr_flags`, then a plain
  weighted-mean drizzle (`driz_cr=median=blot=False`) — no blotted-median reference
  anywhere. Fail-fast in `reduce_target` for non-astrodrizzle backends and
  instruments without a registered deepCR model (e.g. `wfc3_ir`, whose CRs calwf3
  already flags per-frame).
- **The #61 `resetbits` trap is pinned by a named unit test**: the per-frame route
  must emit `resetbits=0` — AstroDrizzle's default (4096) clears exactly the DQ bit
  the masks live in, silently producing an unmasked drizzle that still looks
  plausible (the reporter's first attempt scored a "flawless" core=1.000 that was
  the no-CR image scored against itself).
- **`TargetSpec.psf_star_pass: "auto" (default) | "science" | "no_cr"`** (#62).
  `pipeline.py::_psf` draws star finding **and** stamp extraction from
  `_star_pass_image(...)` instead of unconditionally from the science mosaic.
  `auto` never adds a drizzle (uses the least-CR-rejected pass that costs nothing
  extra); `no_cr` is the explicit opt-in second AstroDrizzle pass on the identical
  grid with CR DQ flags treated as good (`final_bits | 4096`) and `resetbits=0` so
  the science pass's flags survive in the inputs. The `reduction.json` `psf` block
  **always** records `star_source_pass` (+ reason or star-pass kwargs) so the
  coupling cannot silently regress — the #62 wiring requirement.
- **Design doc**: `docs/design/hst_acs_pipeline.md` Stage 3 documents the dial as a
  deviation-in-waiting (default stays STScI `driz_cr`; flip gated on SLACS
  reference-bar validation vs *tuned* driz_cr, scale 1.5/1.2 per published STScI
  reprocessing vs the 1.2/0.7 pipeline defaults we inherit); Stage 5 documents the
  star-pass decoupling.

## Traps and findings worth keeping

- **Naming honesty: the dial is `"deepcr"`, not `"lacosmic"`.** The prompt title
  says LACosmic (the reporter's method), but the per-frame masker this pipeline
  already runs is deepCR — labelling it `"lacosmic"` would falsify provenance. Same
  method class (per-frame, no median reference). An astroscrappy/LACosmic backend is
  a clean follow-up **only if** validation shows a gap between the two.
- **The reporter's follow-up grid (issue #61, 2026-08-09) overturned the headline
  number.** The ~37% core erosion was an artifact of a dither-erasing TweakReg
  misalignment in *their* pipeline (every frame aligned onto the first, collapsing
  the stack to a single pointing — the degenerate condition the blotted-median
  mechanism needs). With correct MAST alignment, driz_cr holds core ratio 0.998 vs
  no-CR at **every** snr/scale/combine_type setting they tried; dither-erased,
  driz_cr's incremental damage is ~23%. So driz_cr is fine on well-dithered,
  correctly-aligned stacks; the failure regime is degenerate/small dither (or
  erased dither). PyAutoReduce's stage-2 default (trust a-priori WCS, TweakReg only
  on trigger) preserves dither, so the erosion likely never reproduces in our
  default config.
- **That correction reshapes the validation, and weakens the default-flip case.**
  The discriminating test for deepCR-vs-tuned-driz_cr is a **poorly-dithered**
  target (few exposures, small/degenerate dither, true single-exposure SNAP), not a
  clean 4-dither box. The remaining case for per-frame as default is robustness
  (clean core regardless of dither quality) rather than a fixed erosion on typical
  data.
- **`psf_star_pass="auto"` deliberately never doubles combine time**: on driz_cr
  runs AstroDrizzle keeps no less-rejected intermediate (the median image IS the
  biased reference), so auto = science mosaic + recorded reason; the dedicated
  no-CR pass is an explicit opt-in.
- **Honest gaps at ship time**: the deepcr route and no_cr star pass are exercised
  through unit-tested pure functions and monkeypatched plumbing — no
  drizzlepac/deepCR execution or real-data validation in that environment;
  `no_cr` + `psf_backend="starred"` weights stamps with the science-pass noise map
  (documented approximation); JWST image3's `outlier_detection` has the analogous
  median-reference failure mode but `cr_method` there is rejected, not addressed.

## Remaining (tracked elsewhere, not this task)

- Default-flip decision: human-gated on the SLACS reference-bar validation
  (`active/pyautoreduce_slacs1430_acs_comparison.md`) with a tuned-driz_cr arm, now
  targeted at the poorly-dithered regime per the reporter's grid. #61/#62 close
  with that decision, either way.
- The reporter's 2026-08-09 correction comment on #61 is unanswered; a reply is
  a `/community` (human-gated) action.

## Original prompt

# LACosmic per-frame CR masking option + decouple PSF-star pass from the science CR pass

Type: feature
Target: PyAutoReduce
Difficulty: medium
Autonomy: supervised
Priority: high
Status: draft

Community-reported (@samlange04, PyAutoReduce#61 + #62, measured on SLACS
ACS/WFC F814W): the unconditional `driz_cr=median=blot` route in
`autoreduce/drizzle/combine.py::drizzle_kwargs_for` systematically erodes flux
at steep gradients — the blotted-median reference reads low at any sub-pixel-
shifted peak, so genuine core flux is flagged as CR. Reporter measured ~37%
deflector-core flux loss, worse with looser thresholds (the reference model is
the fault, not the cut), and full core preservation (peak 1.000, 1" 0.979)
with LACosmic per-frame masking + plain weighted-mean drizzle. The same
mechanism holes field-star cores before `psf/stars.py::find_stars` ever sees
them (#62): rebuilding from a no-CR pass took their usable star count
344 → 599 (+74%) and rescued 4 lens/filter pairs from model-PSF fallback.

Scope (one task — the halves are coupled through the no-CR pass):

1. **CR-method dial** on `TargetSpec` (sibling of `final_pixfrac` /
   `final_kernel`): `cr_method: "driz_cr" | "lacosmic"`. LACosmic route =
   per-frame Laplacian masking (van Dokkum 2001; `astroscrappy` or deepCR —
   `frame_products` already runs deepCR per-frame, so there may be a lever to
   reuse) written into the DQ array, then plain weighted-mean drizzle
   (`median=False, blot=False, driz_cr=False`).
   **Trap (reporter hit it, verify with a test):** the LACosmic drizzle pass
   must set `resetbits=0` — the AstroDrizzle default 4096 clears exactly the
   DQ bit the CR mask lives in, silently producing an unmasked drizzle.
2. **Decouple star-finding from the science pass**: `pipeline.py::_psf`
   currently measures stars on whatever `_combine` produced. Tier-1/1b star
   extraction should draw from the least-CR-rejected pass available,
   independent of which pass ships as the science mosaic (kernel shape is
   pass-independent). Provenance records which pass fed the stars.
3. **Default decision is human-gated**: whether `lacosmic` becomes the
   default (reporter suggests so) is a documented deviation from STScI
   defaults — justify against the SLACS reference-quality bar
   (`docs/design/hst_acs_pipeline.md`) and validate on the
   slacs1430+4105 comparison task (`active/pyautoreduce_slacs1430_acs_comparison.md`)
   before flipping; landing it as an option first is acceptable.

Validation: unit tests for the pure kwargs/decision functions (house style);
real-data before/after on a SLACS ACS target measuring core-flux retention
and usable-star count, mirroring the reporter's numbers. Include a tuned
`driz_cr` comparison arm: our adapters set no `driz_cr_snr`/`driz_cr_scale`,
so we run AstroDrizzle's aggressive pipeline defaults (scale 1.2/0.7) — the
STScI-documented mitigation for bright-source flagging is raising
`driz_cr_scale` (published reprocessing used 1.5/1.2), and the default-flip
decision should compare LACosmic against *tuned* driz_cr, not only against
our current untuned defaults.

<!-- filed from /community triage of PyAutoReduce#61 + #62 (2026-07-31) -->
