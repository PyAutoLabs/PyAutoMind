## wfc3-reduction
- issue: https://github.com/PyAutoLabs/PyAutoReduce/issues/4 (closed)
- completed: 2026-07-09
- prs: PyAutoReduce#5 (squash-merged)
- notes: |
    WFC3 UVIS + IR adapters (phase 2). UVIS validated against published
    Bayer et al. 1803.05952 F390W reduction of J0252+0039 (sky RMS 0.00226
    vs ~0.002 e-/s, R=1.5 shift-and-add); IR F160W internally validated
    (71-star ePSF post saturation-cap fix). Two loud-failure guards
    demonstrated (pixfrac speckle; detector-defect blob) -> dial fixes
    documented in wfc3.md. Review 1 HIGH (per-exposure saturation cap,
    fixed) + 2 LOW. 62 tests. UVIS ePSF refresh deferred to next natural
    UVIS reduction (maintainer).

## Original prompt

# PyAutoReduce phase 2: WFC3 (UVIS + IR) reduction support

Type: feature
Target: PyAutoReduce
Difficulty: large
Autonomy: supervised
Priority: normal
Status: formalised

Extend PyAutoReduce to HST/WFC3, per `docs/design/roadmap.md` — the first
test of the instrument-adapter boundary (nothing outside `instruments/` may
name a detector). User instruction 2026-07-08: begin after phase 1 shipped at
PR-open (PyAutoReduce#3).

Scope:
- **WFC3/UVIS adapter** — ACS-like path: CTE-corrected `_flc`, `iref`
  references, native 0.0396″/pix, cps/IVM; validate against the published
  Bayer et al. (arXiv:1803.05952) F390W reduction of SDSS J0252+0039
  (0.0396″/pix, pixfrac 1.0, σ_sky ≈ 0.002 e-/s) — a literature anchor, since
  no legacy in-house UVIS products exist.
- **WFC3/IR adapter** — the genuinely different path: `_flt` (no CTE
  correction; up-the-ramp sampling already CR-rejected per read), native
  ~0.128″/pix so the `final_scale` dial default needs choosing (document the
  choice; literature spans 0.06–0.13), IR-specific DQ/saturation semantics.
- The `ajshajib/hst-lens` notebooks (WFC3 IR + UVIS) serve as a step
  checklist to audit coverage against — not as architecture.
- Design doc: new `docs/design/wfc3.md` (or a WFC3 section in the HST doc)
  recording per-stage deltas vs ACS; roadmap updated.
- Unit tests numpy/astropy-only (adapter registry, kwargs assembly per
  channel, IR-vs-UVIS branch differences); integration script per channel on
  a real MAST target (J0252+0039 for UVIS F390W; an IR F160W lens found at
  the same or a nearby SLACS system).
- Any generalization the adapters force on phase-1 stage code (e.g.
  suffix/reference-key assumptions) lands here with tests; behaviour of the
  ACS path must not change (existing 53 tests stay green).

Acceptance: both adapters reduce a real target end-to-end from MAST; UVIS
noise/data products consistent with the Bayer published parameters; IR
products internally validated (noise closure vs empirical sky, WHT
uniformity, PSF diagnostics); ACS regression suite green.
