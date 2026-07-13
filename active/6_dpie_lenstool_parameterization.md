# LensTool-native dPIE parameterization and numerical parity validation

Type: feature
Target: cluster
Difficulty: large
Autonomy: supervised
Priority: high
Status: formalised

Add a LensTool-native parameterization of the dPIE mass profile and validate numerical parity against LensTool.

`autogalaxy/profiles/mass/total/dual_pseudo_isothermal_mass.py` (`dPIEMass` / `dPIEMassSph`) is
already a direct port of LensTool's C code, parameterized as (ra, rs, b0) in arcsec with the
pseudo-elliptical radius r_em^2 = x^2/(1+eps)^2 + y^2/(1-eps)^2 (LensTool's convention, not
intermediate-axis). The docstring already records the conversion b0 = 4*pi*sigma_0^2/c^2 * D_LS/D_S
and the Eliasdottir-2007 E0 relation.

LensTool users parameterize the dPIE as (sigma [km/s], r_core [arcsec or kpc], r_cut [arcsec or kpc]),
so a "same model in both codes" workflow needs:

1. A LensTool-facing constructor or profile — e.g. `dPIEMass.from_lenstool(sigma=..., r_core=..., r_cut=..., redshift_object=..., redshift_source=..., cosmology=...)`
   (or a thin `dPIEMassLensTool` wrapper) that converts (sigma, r_core, r_cut) → (b0, ra, rs),
   handling the sigma vs sigma_dPIE (Eliasdottir Table A.1) subtlety explicitly. Beware LensTool's
   historical factor conventions (the 4pi vs 6pi issue between Kassiola & Kovner 1993, Eliasdottir 2007
   and the LensTool implementation) — read Eliasdottir et al. 2007 (arXiv:0710.5636) Appendix A and
   Limousin et al. 2005 before fixing the conversion.
2. Ellipticity convention mapping: LensTool .par files give ellipticity + position angle; map to
   ell_comps, and document whether LensTool's eps is (a^2-b^2)/(a^2+b^2) (potential ellipticity) vs
   (a-b)/(a+b), since dPIE in LensTool is pseudo-elliptical in the potential for some code paths.
3. Numerical parity validation: convergence, potential and deflection angles of the converted profile
   against reference values — either by running LensTool itself, using published values, or using
   an independent implementation (e.g. the `lenstronomy` dPIE or Galan's work) as a cross-check.
   A parity script belongs in autolens_workspace_test (cross-package checks live there, not library
   unit tests); library unit tests cover the pure conversion math numpy-only.

Outcome: a documented, tested parameter mapping that the later "PyAutoLens for LensTool users"
workspace example (and any real LensTool .par ingestion) can rely on. This is the foundation prompt
of the LensTool-parity series — file findings on any irreconcilable convention differences
prominently, since they determine how close the flagship example can get.

<!-- formalised by the Intake (Conception) Agent on 2026-07-08 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/fa55f70e-2cea-4887-bf12-61f81cff042f/scratchpad/p1_dpie_lenstool_param.md -->

__Research findings (deep-research pass, 2026-07-08)__

- **Velocity-dispersion chain (confirmed):** LensTool's .par `v_disp` is the *fiducial*
  sigma_LT, related to the dPIE central velocity dispersion by sigma_0 = sqrt(3/2) * sigma_LT
  (Bergamini et al. 2019, arXiv:1905.13236; Eliasdottir et al. 2007 App. A). sigma_LT is
  Eliasdottir's sigma_dPIE. Chain to autolens: E0(Eliasdottir) = 6*pi*(sigma_LT/c)^2 * D_LS/D_S,
  and b0 = E0 * (rs^2 - ra^2)/rs^2 = 4*pi*(sigma_0/c)^2 * D_LS/D_S in the rs->inf limit — both
  relations already in the dPIEMass docstring. `from_lenstool` should take sigma_LT (what users
  read out of .par files / papers) and document the sqrt(3/2) trap loudly.
- **Ellipticity (the main open trap):** the port's `_ellip()` uses |ell_comps| directly as the
  Kassiola & Kovner eps in r_em^2 = x^2/(1+eps)^2 + y^2/(1-eps)^2, i.e. eps = (a-b)/(a+b) —
  consistent with PyAuto's standard ell_comps magnitude. LensTool .par files and papers quote
  ellipticity as e = (a^2-b^2)/(a^2+b^2) (verify against LensTool source `ci05`/`piemd` — the
  wiki page projets.lam.fr/projects/lenstool/wiki/piemd was unreachable during research; use the
  public git repo git-cral.univ-lyon1.fr or github mirror). The converter must map
  e_par -> q -> eps=(1-q)/(1+q) and be validated numerically, including position-angle convention
  (LensTool angle is counter-clockwise from x-axis? — verify) vs PyAuto's phi from north.
- **Radius units:** LensTool .par `core_radius` / `cut_radius` are in arcsec (variants
  `core_radius_kpc` / `cut_radius_kpc` in kpc); support both in the converter via cosmology.
- **Parity references:** M(R) closed form for ra=0: M(R) = (pi*sigma_0^2/G)(R + r_cut -
  sqrt(r_cut^2 + R^2)) (Bergamini 2019 App. C) — good analytic anchor for the mass/convergence
  parity test alongside lenstronomy's PJAFFE/dPIE as an independent implementation.
