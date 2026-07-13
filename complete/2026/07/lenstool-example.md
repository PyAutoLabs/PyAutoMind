## lenstool-example
- issue: https://github.com/PyAutoLabs/autolens_workspace/issues/239 (closed)
- completed: 2026-07-09
- pr: autolens_workspace#240 (merged)
- notes: The flagship "PyAutoLens for Lenstool users" example — scripts/cluster/lenstool/
  {data,modeling,README}. Anchored to Mahler et al. 2023's public Lenstool release of SMACS J0723
  (github.com/guillaumemahler/SMACS0723-mahler2022 ICLv2: best.par/input.par/arcs.dat/galcat.cat,
  runtime-downloaded with attribution — GPL repo, nothing redistributed). data.py verifies the
  Lenstool relative frame against the data itself (x = -dRA·cosd0·3600, positive West) and
  propagates sigposArcsec=0.4427" as the chi² noise. modeling.py reconstructs all 149 dPIE
  potentials via from_lenstool and achieves **0.068" median source-plane rms** across 21 systems
  (all ≤0.29"; published image-plane rms 0.32") — one-number validation of the entire convention
  chain — then composes the exact refit (input.par prior bounds in Lenstool units via
  dPIEMassLenstool; potfile tier = shared sigma*/r_cut* with fixed L^0.25/L^0.5 exponents;
  72 free params = 30 mass + 42 source positions; search/forward-solve/figures gated for runtime).
  KEY CONVENTION discovered en route: multi-plane Tracer normalizes profile deflections to the
  FINAL plane — from_lenstool must take the tracer's highest source redshift as redshift_source
  (z=2 normalization mis-scaled deflections ~15% → 2" source smear, measured then fixed).
  Gotchas: (a) navigator catalogue regen required for any workspace script change; (b) critical
  curves through 149 profiles cost ~10 min/plane in numpy — JAX-side speedup filed as follow-up
  idea; (c) galcat.cat has 146 uncommented rows vs 144 best.par members (2 potfile exclusions) —
  refit uses the catalogue, documented. NEXT: beta-tester iteration loop on this example.
