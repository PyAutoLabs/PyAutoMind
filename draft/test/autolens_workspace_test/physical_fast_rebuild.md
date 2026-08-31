# autolens_workspace_test physical + fast rebuild (flagship)

Type: test
Target: autolens_workspace_test
Repos:
- autolens_workspace_test
Difficulty: large
Autonomy: supervised
Priority: high
Status: formalised
Consequence: judge
Review-minutes: 25
Unattended: needs-slicing
Epic: ci-timing-fast-tests
Phase: 6

autolens_workspace_test physical + fast rebuild (flagship repo; applies the phase-5 template).

Same one-wave realism+speed rebuild as phase 5, on the 26 smoke-gate entries (158 scripts
total, 92 carrying `# ENV:` declarations). Known concrete defects from the 2026-08-31
survey to fix (and sweep siblings for the same patterns):

- `imaging/jax_likelihood/mge.py`: dataset simulated with elliptical Isothermal+shear lens
  (Sersic+Exp light) but fitted with NFWSph mass + fixed mass_to_light_ratio=10.0
  GaussianGradient basis — structurally mismatched, pinned at a low-likelihood
  prior-median point (pin -86283.10 at line ~248). Rebuild as a consistent, physical,
  high-likelihood setup.
- `imaging/model_fit.py`: fits DevVaucouleursSph + IsothermalSph (no shear) against
  `with_lens_light.py`'s sim of elliptical PowerLaw slope=1.8 + shear; sim source
  ExponentialSph r_eff=0.1" is barely resolved at 0.2".
- `imaging/simulator/simple.py`: lens light intensity 4.0 / sersic_index 3.0 + Exp 2.0 on
  background_sky_level=1.0 — implausibly bright vs the "HST-representative" claim; pixel
  scales in the repo: 0.2 (58x), 0.1 (52x), 0.05 (11x), 0.3 (4x) — move the default test
  resolution coarser (0.3" still just resolves a lens) wherever coverage allows.
- multi_dataset sim is the closest to consistent (shared SIE, per-band Sersic source) —
  use it as the in-repo reference pattern.

Same constraints as phase 5: one pin-regeneration wave at the end; preserve the Eigen-pool
bug-class coverage in `multi_dataset/jax_likelihood/*` (delaunay_mge still hangs
intermittently WITH the flag — do not alter its reproduction conditions without recording
it in the jax-compile-stall epic ledger); unit tests + developer/profiling workspaces
validate; before/after per-script seconds against the phase-4 legacy snapshot. The 900s
`jax_grad/` cap class (measured 41-568s) is in scope — it is the largest single wall-clock
block on the gate.
