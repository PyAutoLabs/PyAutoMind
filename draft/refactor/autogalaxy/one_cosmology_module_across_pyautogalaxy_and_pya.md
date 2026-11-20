# One cosmology module across PyAutoGalaxy and PyAutoLens; remove `cosmology_astropy`

Type: refactor
Target: PyAutoGalaxy
Repos:
- PyAutoGalaxy
- PyAutoLens
- autolens_workspace
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: formalised
Consequence: judge
Witness: in PyAutoGalaxy and PyAutoLens source (tests excluded), `grep -rn "astropy.cosmology\|cosmology_astropy"` matches only inside `autogalaxy/cosmology/`; every dark-matter mass profile, `Tracer`, the analyses and `LOSSampler`/`mass_function_ab_from` take the one `ag.cosmology` object; and a LOSSampler halo count with a non-Planck `ag.cosmology.FlatLambdaCDM` differs from the Planck15 count instead of being silently ignored.
Review-minutes: 20
Unattended: never
Lane: any

## Request (human, verbatim, 2026-11-20)

"An issue which fixes the different and inconsistent cosmologies going around the source code, which make various dark matter profiles confusing but also lead to inputs like cosmology_astropy which should not exist if cosmology is one unified module through PyautoLens and PyAutoGalaxy"

## What is there now (grep, 2026-11-20)

- `autogalaxy/cosmology/model.py` defines `LensingCosmology` (mixin over a flat ΛCDM) and `Planck15`; most profiles default to `cosmology or Planck15()`.
- Astropy cosmology / `FlatLambdaCDM` / `Planck15|18` references are spread across `profiles/mass/dark/` (`abstract.py`, `nfw_truncated.py`, `mcr_util.py`, `ludlow16.py`, `nfw_virial_mass_conc.py`, `gnfw_virial_mass_*`), `profiles/mass/total/dual_pseudo_isothermal_mass.py`, `profiles/mass/point/smbh.py`, `analysis/analysis/analysis.py`, and in PyAutoLens `lens/los.py` (13), `interop/coolest.py`, `lens/tracer_util.py`, `lens/tracer.py`, `analysis/analysis/{lens,dataset}.py`, `aggregator/tracer.py`, `lens/substructure_util.py`.
- `lens/los.py` keeps a deprecated `cosmology_astropy=` argument on `mass_function_ab_from` and `LOSSampler` that is deprecated with a hidden DeprecationWarning; since PyAutoLens#874 (2026-11-20) a value that disagrees with the colossus cosmology name raises a ValueError instead of being silently ignored.
- Workspace scripts touching astropy cosmology / `cosmology_astropy`: `autolens_workspace/scripts/guides/advanced/multi_plane.py`, `guides/units/mass_to_light_ratio_units.py`, `imaging/features/advanced/los_halos/simulator.py`, `simulator_jax.py`.

## Want

- One cosmology abstraction (`autogalaxy.cosmology`, exposed as `ag.cosmology` / `al.cosmology`) used everywhere: profiles, tracer, analyses, LOS sampling, interop. No second path through raw astropy objects; anything that needs astropy (e.g. the halo mass function) derives it inside the cosmology module from the one object.
- Remove `cosmology_astropy` from `mass_function_ab_from` and `LOSSampler` (pass `cosmology=`), and any other parallel cosmology argument found in the survey.
- Consistent defaults: one default cosmology, defined once.
- Update the affected workspace scripts.

## Notes

- The overlapping bug `lossampler_silently_ignores_a_non_planck_cosmolo` (same `los.py` argument) merged 2026-11-20 as PyAutoLens#874 (https://github.com/PyAutoLabs/PyAutoLens/pull/874), record `complete/2026/11/lossampler-cosmology-mismatch.md`: a `cosmology_astropy` / `cosmology` that disagrees with the colossus name now raises a ValueError. This refactor removes the argument and that check with it.
- Public API change (argument removal): needs a deprecation decision at plan time (remove now vs one release of warning).

<!-- formalised by the Intake (Conception) Agent on 2026-11-20 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/86b988f9-7d16-4d09-8865-10a9d166d677/scratchpad/cosmo_intake.md -->
