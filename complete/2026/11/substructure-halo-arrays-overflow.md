`galaxies_to_halo_arrays` / `los_realizations_to_arrays` no longer drop halos silently. An overflowing integer `max_n` raises a ValueError naming each plane, its count and the `max_n` needed, and `max_n=None` sizes the arrays to the fullest plane (across the batch). On main, 5 halos on one plane with max_n=3 kept 3 and raised nothing; the workspace `simulator_jax` example's fullest plane held 304 halos against max_n=200. It now keeps 1100/1100 halos ("Padded to 304 slots per plane").

Decision taken and accepted by the human at /prm (merged unchanged): autolens_workspace#682 uses `max_n=None` rather than a larger fixed integer.

Witness: `pytest test_autolens/lens/test_substructure_util.py`, 10 passed (5 new, 4 fail on main); `simulator_jax.py` full run PASS.

- adversary: CLEAN, from Fable 5.2 (author Opus 5.5), 2026-11-19. No off-by-one at n == max_n; the check runs before any traced code; 180 arrays identical to main for a sufficient integer max_n; padded slots give exactly zero deflection; the three autolens_workspace_test substructure scripts pass. Note: `jax.grad` is NaN with zero-padded slots, pre-existing on main and not fixed by PyAutoGalaxy#737.

Related, already filed: `draft/bug/autolens/substructure_jax_grad_is_nan_when_a.md`.

Shipped in PyAutoLens#870 (https://github.com/PyAutoLabs/PyAutoLens/pull/870) and autolens_workspace#682 (https://github.com/PyAutoLabs/autolens_workspace/pull/682), merged 2026-11-19 by human /prm. Done by shift worker 2026-11-19-pm (4b5218b2).

## Original prompt

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
Verified: 2026-11-19 a79a6b22 (PyAutoLens), 4674ae89 (autolens_workspace)
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
