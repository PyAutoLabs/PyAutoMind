# dPIE: optional central-dispersion (sigma_0) parameterization

Type: feature
Target: PyAutoGalaxy
Repos:
- PyAutoGalaxy
- autolens_workspace
Themes:
- cluster
Difficulty: small
Autonomy: supervised
Priority: low
Status: draft
Consequence: judge
Review-minutes: 20
Unattended: ready
Parent: draft/docs/autolens/split_lensing_regimes.md
Filed: 2026-07-25 (backfilled from git)

The contributed derivation note (H. Ding 2026, "On the definitions of b0 and
velocity dispersion in Lenstool / dPIE") establishes that Lenstool's fiducial
dispersion sigma_LT is a bookkeeping convention (E07-style b0 coefficient
paired with the K93/L05 deflection amplitude), and recommends the physical
central dispersion sigma_0 — with b0 = 4 * pia_c2 * sigma_0^2 — as the
cleaner parameter for scientific interpretation, unless exact Lenstool
parameter parity is required.

`dPIEMass` deliberately keeps sigma_LT so fitted posteriors read like
Lenstool results tables (docstrings corrected on the doc-reorganization
branch, 2026-07-25). This prompt proposes ADDING the sigma_0 option without
disturbing that default:

- Either a `dPIEMassSigma0` sibling class (constructor takes `sigma_0`,
  internal b0 = 4*648000*(sigma_0/c)^2*(D_LS/D_S)) or a
  `sigma_convention="lenstool"|"central"` constructor switch — pick
  whichever composes more cleanly with af.Model priors and the CSV API.
- Docstrings cross-reference the two conventions and the sqrt(3/2) mapping.
- Unit tests: sigma_0 = sqrt(3/2)*sigma_LT inputs produce identical
  deflections; Lenstool parity tests untouched.
- One workspace example line in `cluster/mass_parameterizations.py` showing
  the physical-convention alternative.

Motivation for prioritising later: no behaviour is wrong today; this is an
interpretability convenience for users comparing fitted dispersions with
measured stellar kinematics.
