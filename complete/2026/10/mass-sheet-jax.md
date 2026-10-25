# MassSheet JAX deflections

- completed: 2026-10-25
- PRs: PyAutoGalaxy#662; autogalaxy_workspace_test#128
- pending-release: PyAutoGalaxy@https://github.com/PyAutoLabs/PyAutoGalaxy/pull/662

Unwrapped radial array before the Cartesian transform. NumPy/eager JAX/JIT/vmap and derivative regression passes; baseline fails. Full suite 1356 passed, 6 skipped.

All exact-head Actions runs and jobs passed: Python 3.12/3.13, no-JAX and docs; companion workspace smoke 3.12/3.13 where applicable. No test job skipped. Heart freeze clear. Human authorized `/prm on all`; merged unchanged from the published, tested tree. Remote head ancestry in main verified; local commit trees equal merged remote trees. No independent-review claim.

Routine local pytest outputs are reproducible test products, not user analysis data. Worktree cleanup follows lifecycle close. Library change awaits the next published release.

## Original prompt

# `@PyAutoGalaxy` MassSheet deflections fail under JAX (ArrayIrregular into `xp.multiply`)

Type: bug
Target: autogalaxy
Repos:
- @PyAutoGalaxy
Themes:
- jax
- mass-profiles
Difficulty: small
Autonomy: supervised
Priority: low
Status: formalised
Consequence: glance
Witness: `ag.mp.MassSheet(kappa=0.5).deflections_yx_2d_from(grid=aa.Grid2DIrregular([(0.1, 0.2)]), xp=jnp)` returns (0.05, 0.1), matches NumPy, and works under `jax.jit`; a unit test covers it.
Filed: 2026-10-23
Issue: https://github.com/PyAutoLabs/PyAutoGalaxy/issues/658

## Why

Found while reproducing PyAutoLens#799: a `MassSheet` host reproduced the singular-core candidate in NumPy but could not run under JAX. Verified 2026-10-23:

```
TypeError: multiply requires ndarray or scalar arguments, got <class 'autoarray.structures.arrays.irregular.ArrayIrregular'> at position 0.
```

`MassSheet.deflections_yx_2d_from` (`autogalaxy/profiles/mass/sheets/mass_sheet.py`) passes `radius=self.kappa * grid_radii`, where `grid_radii` comes from the decorated `radial_grid_from` as an `ArrayIrregular`. `GeometryProfile._cartesian_grid_via_radial_from` then calls `xp.multiply(radius[:, None], ...)`, which jnp rejects. NumPy accepts the wrapper.

## Deliverables

1. Pass the raw array (e.g. `grid_radii.array`). Audit other `_cartesian_grid_via_radial_from` callers for the same pattern.
2. Unit test of eager-NumPy vs `xp=jnp` vs `jax.jit` parity for `MassSheet` deflections.

Issued: 2026-10-25

## Execution 2026-10-25
User authorized selecting and implementing four related tasks. Scope: Fix MassSheet JAX deflections. Separate branch and PR; no merge authorization. Related group executes serially with non-overlapping source edits.

## Implementation evidence (2026-10-25)

- Library PR: https://github.com/PyAutoLabs/PyAutoGalaxy/pull/662 at `36ec41b232d827f5342831f4d62939a9e7b4b64f`; published Git tree equals the tested local tree.
- Full library suite: `python3 -m pytest -q -n auto test_autogalaxy`, 1356 passed, 6 skipped; Python 3.12, released 2026.10.25.1 dependencies.
- Log: `/workspace/scratch/e0d55f00a4c5/evidence/mass-sheet-jax-suite.log`.
- Heart readiness GREEN, score 100, no reasons; evidence timestamp 2026-10-25T20:54:46Z.
- GitHub Tests and Docs for the exact PR head were running at the final check; no CI success or merge claimed.
- Merge mode: human `/prm`; no merge, close-out or release authorized/performed.
- Workspace regression PR: https://github.com/PyAutoLabs/autogalaxy_workspace_test/pull/128 (draft). Direct script passes with JAX 0.11.2 on this branch and fails against unmodified main; smoke-list entry added. Full workspace CI pending library availability.
- JAX log: `/workspace/scratch/e0d55f00a4c5/evidence/mass-sheet-jax-jax.log`.
