# Profiles light mass factory and lmp modules

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
Phase: 2
Consequence: glance
Witness: `test_autogalaxy/profiles/files/public_surface.json` byte-identical (no regeneration), `pytest test_autogalaxy` and `pytest test_autolens` green including `test_autogalaxy/analysis/test_chaining_util.py` and the `mge_model_from` tests, `profiles_jit.py` passes, the `standard_lp_parent` dictionary is gone, and `light_and_mass_profiles.py` + `light_linear_and_mass_profiles.py` fall from 1,393 lines to under 200
Review-minutes: 3
Unattended: ready
Lane: any

Phase 2 of the profiles-unified-api epic (`draft/refactor/autogalaxy/profiles_unified_api_epic.md`;
report §4.1, §7 phase 2). Depends on phase 1 (`variants.py`) being merged.

## Change

1. `light_mass(light_cls, mass_cls, *, module, name=None)` in
   `@PyAutoGalaxy/autogalaxy/profiles/variants.py`: a class with bases
   `(light_cls, mass_cls, LightMassProfile)` whose generated `__init__` takes the union of the two
   signatures in today's order (light parameters, then the mass-only ones such as
   `mass_to_light_ratio`) and calls `light_cls.__init__` then `mass_cls.__init__` exactly as the
   31 hand-written classes do (`@PyAutoGalaxy/autogalaxy/profiles/light_and_mass_profiles.py:17-60`
   is the pattern). For the linear case it records `_standard_cls` = the matching `lmp` class.
2. Rewrite `light_and_mass_profiles.py` (17 classes, 720 lines) and
   `light_linear_and_mass_profiles.py` (14 classes, 601 lines) as tables of factory calls, with
   `spherical()` for the `*Sph` members. `LightMassProfile` itself stays hand-written.
3. Delete the 14-entry `lmp_linear → lmp` dictionary in `standard_lp_parent`
   (`@PyAutoGalaxy/autogalaxy/profiles/light/linear/abstract.py:131-152`, self-described as "the
   ugly dictionary ... should be removed"); the method returns `_standard_cls`.
4. Extend the `.pyi` generator to these two modules.

## Witnesses beyond the golden file

`analysis/chaining_util.py:430-446` and `:522-529` and `analysis/model_util.py:177-210` map
between `lp`, `lp_linear`, `lmp`, `lmp_linear` classes by identity — their tests must stay green;
`deflections_memo._gaussian_class_pair` (`profiles/mass/abstract/deflections_memo.py:469-485`)
splits the L2 memo on `lmp.Gaussian` / `lmp_linear.Gaussian` by class — `test_deflections_memo.py`
(18 tests) must stay green; `Galaxy` classifies an lmp instance as both light and mass through
`isinstance` on the two bases.

<!-- formalised by the Intake (Conception) Agent on 2026-11-09 from file:/tmp/claude-0/-home-user/cd6c1ec3-dd35-55c4-a663-eb8c309de811/scratchpad/intake_raw/p2.md -->
