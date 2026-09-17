# After the phase-8c releases: bump the autonerves floor, drop the defensive fallback, revert the HowTo mesh guards

Type: maintenance
Target: PyAutoArray
Repos:
- PyAutoArray
- HowToLens
- HowToGalaxy
Difficulty: small
Autonomy: safe
Priority: low
Status: formalised
Consequence: glance
Witness: PyAutoArray's autonerves floor names the release carrying PyAutoNerves#160, the `try/except` fallbacks around `disable_jax()` and `SMALLSHP` from #529 are gone (a plain import, the duplicated-literal drift test removed), and the four `mesh_shape` guards in HowToLens and HowToGalaxy are reverted with notebooks regenerated and their smoke gates green.
Review-minutes: 3
Filed: 2026-09-06

Two loose ends the phase-8c library leg of the ci-timing-fast-tests epic left on purpose,
both gated on releases that do not exist yet:

1. PyAutoArray#529 imports `autonerves.test_mode.disable_jax()` and the `SMALLSHP`
   constant defensively (`try/except`), so an older autonerves degrades to the previous
   behaviour. Once the PyAutoNerves release carrying #160 is out and PyAutoArray's floor is
   bumped to it, delete the fallbacks and the duplicated literal's drift test can become a
   plain import.
2. HowToLens#77 and HowToGalaxy#73 added four script-level `mesh_shape` guards; the mesh
   cap in PyAutoArray#529 resolves to the same `(16, 16)` and makes them redundant. Revert
   the four guards (and regenerate the notebooks) once the PyAutoArray release with the cap
   is what the HowTo smoke gates install.
