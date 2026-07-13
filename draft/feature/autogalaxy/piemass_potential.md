# `PIEMass.potential_2d_from`: implement the missing lensing potential

Type: feature
Target: PyAutoGalaxy
Difficulty: too-large
Autonomy: supervised
Priority: normal
Status: formalised

Follow-up from the dark-matter potential work (PyAutoGalaxy
`feature/dark-matter-potentials`). That branch implemented
`potential_2d_from` for every elliptical/spherical NFW/gNFW variant and
fixed `NFWSph`. `PIEMass` was deliberately scoped out because, unlike the
NFW family, it has no decomposition hook to reuse.

## Symptom

`PIEMass` (the Lenstool-ported Pseudo-Isothermal Elliptical Mass
Distribution, Kassiola & Kovner 1993) has `deflections_yx_2d_from` and
`convergence_2d_from` but no `potential_2d_from`. It therefore inherits
the abstract base `MassProfile.potential_2d_from`, which now raises a
clean `NotImplementedError` (post `feature/dark-matter-potentials`; it
previously raised a confusing `TypeError: ... unexpected keyword argument
'xp'`). Any tracer/galaxy containing a `PIEMass` crashes when the
visualizer writes the `potential` extension to `tracer.fits`.

This is the same class of bug as the original NFW report (visualization
calls `tracer.potential_2d_from`; the likelihood path never does), just
for a different profile.

## Where the code lives

`autogalaxy/profiles/mass/total/dual_pseudo_isothermal_mass.py`, class
`PIEMass` (~line 218). The sibling `dPIEMass` (~line 359) in the same file
*does* implement an analytic `potential_2d_from` (~line 586) — `PIEMass`
is the single-core limit of `dPIEMass`.

## Why MGE doesn't drop in

The NFW family reuses `MGEDecomposer(mass_profile=self).potential_2d_via_mge_from(...)`,
but `PIEMass` has neither `decompose_convergence_via_mge` nor
`decompose_convergence_via_cse` (verified: both `hasattr` return False),
so the MGE route raises `NotImplementedError`.

## Plan (two options)

1. **Analytic (preferred).** Port the PIE lensing potential from Kassiola
   & Kovner (1993) / Lenstool, or specialise `dPIEMass.potential_2d_from`
   to the `r_s -> infinity` (no-truncation) limit — note the convergence
   normalisations differ (`dPIE` carries an `r_s/(r_s-r_a)` factor), so it
   is not a verbatim copy.
2. **MGE convergence hook.** Add a `decompose_convergence_via_mge`
   (2D, `three_D=False`) hook to `PIEMass` so the existing
   `potential_2d_via_mge_from` can integrate it.

## Validation

Self-consistency via finite differencing (the `dark.py` pattern in
`autolens_workspace_test/scripts/mass/`, or a new `total.py` case):
`grad(psi)=alpha` and `lap(psi)=2 kappa` must agree to ~1e-3 (med). Add a
`test__potential_2d_from` to `test_autogalaxy/profiles/mass/total/`. If
the analytic route is taken, also cross-check it against an MGE potential
of the same profile at zero/low ellipticity.

<!-- formalised retroactively by the Intake (Conception) Agent on 2026-07-08 -->
