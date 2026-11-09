# Profiles hygiene sweep

Type: refactor
Target: PyAutoGalaxy
Repos:
- PyAutoGalaxy
Themes:
- hygiene
- mge
Difficulty: small
Autonomy: safe
Priority: low
Status: formalised
Filed: 2026-11-09
Epic: profiles-unified-api
Phase: 5
Consequence: glance
Witness: `test_autogalaxy/profiles/files/public_surface.json` byte-identical (no regeneration), `pytest test_autogalaxy` green including `profiles/mass/total/test_dual_pseudo_isothermal_mass.py` and `test_dual_pseudo_isothermal_potential.py`, and `dual_pseudo_isothermal_mass.py` shrinks by at least 150 lines
Review-minutes: 3
Unattended: ready
Lane: any

Phase 5 of the profiles-unified-api epic (`draft/refactor/autogalaxy/profiles_unified_api_epic.md`;
report §1.4, §7 phase 5). Depends on phase 3.

## Change

1. `dPIEMassB0.potential_2d_from` stacks `@aa.over_sample @aa.decorators.to_array
   @aa.decorators.transform @aa.decorators.to_array @aa.decorators.transform`
   (`@PyAutoGalaxy/autogalaxy/profiles/mass/total/dual_pseudo_isothermal_mass.py:791-796`). Harmless
   today because `transform` is idempotent via `is_transformed`
   (`autoarray/structures/decorators/transform.py:71`), but a doubled wrap: reduce to the canonical
   stack and assert the potential values unchanged.
2. The five classes of `dual_pseudo_isothermal_mass.py` (1,359 lines: `PIEMass`, `dPIEMassB0`,
   `dPIEMassB0Sph`, `dPIEMass`, `dPIEMassSph`) each re-declare `deflections_yx_2d_from`,
   `convergence_2d_from` and `analytical_hessian_2d_from` around the same `_ci05` / `_ci05f` /
   `_mdci05` / `_pi05` helpers; where two bodies are literal copies up to the parameters passed,
   share them through one private method with the differing parameters as attributes. Do not touch
   the helpers' arithmetic.
3. `lp_snr.SersicSph`'s docstring documents an `intensity` argument the class does not take — if
   phase 1 did not already regenerate it, fix it.
4. Optional, if cheap: regenerate `docs/api/light.rst` and `docs/api/mass.rst` autosummary lists
   from the eight namespaces' exports so a newly generated class cannot be missed.

<!-- formalised by the Intake (Conception) Agent on 2026-11-09 from file:/tmp/claude-0/-home-user/cd6c1ec3-dd35-55c4-a663-eb8c309de811/scratchpad/intake_raw/p5.md -->
