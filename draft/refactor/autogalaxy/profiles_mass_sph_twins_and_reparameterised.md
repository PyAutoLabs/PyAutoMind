# Profiles mass Sph twins and reparameterised

Type: refactor
Target: PyAutoGalaxy
Repos:
- PyAutoGalaxy
- PyAutoLens
- autolens_workspace_test
Themes:
- hygiene
- mge
Difficulty: medium
Autonomy: safe
Priority: high
Status: formalised
Filed: 2026-11-09
Epic: profiles-unified-api
Phase: 3
Consequence: glance
Witness: `test_autogalaxy/profiles/files/public_surface.json` byte-identical (no regeneration), `pytest test_autogalaxy` and `pytest test_autolens` green including `mass/dark/test_nfw_mcr.py`, `test_nfw_scatter.py`, `test_nfw_truncated_mcr*.py`, `test_yang24.py` and `profiles/test_scaling_relations.py`, `profiles_jit.py` passes, and the eleven hand-written numerics-bearing `*Sph` classes listed in the report §2.2 are unchanged by `git diff`
Review-minutes: 3
Unattended: ready
Lane: any

Phase 3 of the profiles-unified-api epic (`draft/refactor/autogalaxy/profiles_unified_api_epic.md`;
report §2.2, §2.3, §7 phase 3). Depends on phase 1 being merged; independent of phase 2.

## Change

1. Every thin `*Sph` class under `@PyAutoGalaxy/autogalaxy/profiles/mass/**` becomes
   `spherical(<Ell>, module=__name__)`. **Excluded by name** (they carry their own spherical
   numerics and stay hand-written): `IsothermalSph`, `PowerLawSph`, `PowerLawCoreSph`, `NFWSph`,
   `NFWTruncatedSph`, `cNFWSph`, `KaplinghatCoredNFWSph`, `YangSIDMSph`, `dPIEMassB0Sph`,
   `dPIEMassSph`, `dPIEPotentialSph`. A `*Sph` class that overrides any method other than
   `__init__` is never generated.
2. `reparameterised(base, *, name, module, parameters, converter)` in `variants.py`: the generated
   `__init__` prepends the physical parameters in today's order (e.g. `mass_at_200`,
   `redshift_object`, `redshift_source`, plus `scatter_sigma` / `f_c` / `log10m_vir` / `c_2` /
   `overdens` / `inner_slope` where a class has them), stores each on the instance as today, calls
   the named `mcr_util` converter and forwards the base parameters. Rewrite the 18 classes:
   `NFWMCRDuffySph`, `NFWMCRLudlow`, `NFWMCRLudlowSph`, `NFWMCRScatterLudlow(Sph)`,
   `cNFWMCRLudlow(Sph)`, `cNFWMCRScatterLudlow(Sph)`, `gNFWMCRLudlow`, `gNFWVirialMassConcSph`,
   `gNFWVirialMassgNFWConcSph`, `NFWVirialMassConcSph`, `NFWTruncatedMCRDuffySph`,
   `NFWTruncatedMCRLudlowSph`, `NFWTruncatedMCRScatterLudlowSph`, `KaplinghatCoredNFWMCRLudlowSph`,
   `YangSIDMMCRLudlowSph` (`profiles/mass/dark/*_mcr*.py`, `*virial*.py`; 734 lines today). Where a
   class today inherits from another reparameterised class (e.g. `NFWMCRLudlowSph(NFWMCRScatterLudlowSph)`)
   keep the same base so `isinstance` and the MRO are unchanged.
3. Extend the `.pyi` generator to the mass modules.

## Gotchas

`validate.validate_scale_radius` etc. are called inside some base `__init__`s and must still run
on the converted values; the `mcr_util` converters take `xp` in places — forward it as today;
`extract_attribute`-style readers (`galaxy/mass_aggregate.py:154`) look up the stored physical
attributes by name, so the instance attribute set must be identical (the golden file's
`to_dict(cls())` pins it).

<!-- formalised by the Intake (Conception) Agent on 2026-11-09 from file:/tmp/claude-0/-home-user/cd6c1ec3-dd35-55c4-a663-eb8c309de811/scratchpad/intake_raw/p3.md -->
