# substructure_util galaxies_to_halo_arrays drops halos beyond max_n

Type: bug
Target: PyAutoLens
Repos:
- PyAutoLens
- autolens_workspace
Difficulty: small
Autonomy: supervised
Priority: medium
Status: formalised
Consequence: glance
Witness: A unit test passes more halos on one plane than `max_n` to `galaxies_to_halo_arrays` and asserts it raises with a message naming the plane and the count needed; and a second test shows `max_n=None` sizes the arrays to the fullest plane and keeps every halo.
Review-minutes: 3
Unattended: ready
Lane: any

## Finding

`@PyAutoLens/autolens/lens/substructure_util.py` `galaxies_to_halo_arrays` fills a padded
`(n_planes, max_n, n_params)` array. When a plane holds more than `max_n` halos, the extra halos
are skipped by the `if slot < max_n` test with no warning and no count returned.
`los_realizations_to_arrays` inherits this.

Measured on PyAutoLens `main` a79a6b22c, 2026-11-19: a line-of-sight population with a lower mass
limit of 1e6 solar masses has 10,389 halos, with 2,761 on the fullest plane. With `max_n=1000`,
3,708 halos were dropped. The negative convergence sheets, which are computed for the full
population, were kept.

## Why it matters

The simulated image is missing a third of its halos while the compensating sheets remove the mass
of all of them, so mass is no longer conserved and nothing reports it. The workspace example uses
`max_n=200`, which is enough at a 1e7 lower limit only for some plane counts.

## Ask

1. Raise when any plane overflows, naming the plane and the `max_n` needed.
2. Accept `max_n=None` to size the arrays to the fullest plane (and, in
   `los_realizations_to_arrays`, to the fullest plane across the batch).
3. Add the witness tests, and update `@autolens_workspace` `los_halos/simulator_jax.py` if its
   fixed `max_n=200` can overflow with its own settings.

Related: `draft/feature/jax_substructure/6_deflection_equivalence_test.md`.

## Provenance

[from: research dm-sightlines-cdm] Check 9 of the verification run. Script and logs:
`Science/scratch/dm_sightlines_research_2026-11-19/evidence/verify/check9_jit_timing.py`,
`check9_jit_1e6_maxn1000.log`, `check9_jit_1e6_full.log`.

<!-- formalised by the Intake (Conception) Agent on 2026-11-19 from file:/tmp/claude-1000/-home-jammy-Science/4c8e2ded-c0f1-44a2-878a-797321efeaa7/scratchpad/raw/b4.md -->
