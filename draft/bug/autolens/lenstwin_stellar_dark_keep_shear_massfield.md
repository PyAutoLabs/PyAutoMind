# LensTwin: `ReplaceTotalMassWithStellarPlusDark(keep_shear=False)` ignores shear held in a `MassField`

Type: bug
Target: autolens
Repos:
- PyAutoLens
Difficulty: small
Autonomy: supervised
Priority: medium
Status: formalised
Consequence: judge
Witness: on a tracer whose external shear sits in `fields=[al.MassField(shear=ExternalShear(...))]` (the DR1 pipeline layout), `keep_shear=False` removes the shear and records it in `changed` / `removed` / `side_effects`; `keep_shear=True` records it as kept; tests cover both layouts
Epic: lenstwin
Parent: draft/feature/autolens/lenstwin_epic.md
Filed: 2026-10-29

Found by the phase-4a worker (PyAutoLens#811). `autolens/twins/transform/stellar_dark.py` tests each tracer field with `isinstance(field, ExternalShear)`, but real fits store `MassField` objects that hold a `.shear`, so the field shear is never removed or recorded. Phase 4 keeps shear (default), so it is unaffected; a twin that drops shear on a DR1 reference is silently wrong.
