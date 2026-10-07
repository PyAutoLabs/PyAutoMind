## padded-single-image-recovery
- issue: https://github.com/PyAutoLabs/PyAutoLens/issues/771
- completed: 2026-10-07
- library-pr: https://github.com/PyAutoLabs/PyAutoLens/pull/772

Merged PyAutoLens#772 (384e86e06) into main 2026-10-07 via human-typed /prm; issue #771 closed.

`Result.image_plane_multiple_image_positions` and the inward walk in `image_plane_multiple_image_positions_for_single_image_from` now count finite rows (new private helper `Result._finite_multiple_images_from`) rather than array rows, so single-image recovery fires for the inf-padded static-shape output of the JAX point solver exactly as for the numpy solver, and only finite rows reach `PositionsLH` and the cached `files/multiple_image_positions.json`. No pins move (identity for numpy/finite input). Four new tests in `test_autolens/analysis/test_result.py`; witness 3/4 red on unfixed source; full `test_autolens` 831 passed, 1 xfailed.

Pending release: merged is not released — the `pending-release:` key above stays until `/review_release` clears it.

## Original prompt

# PyAutoLens: single-image recovery in `Result.image_plane_multiple_image_positions_from` is blind to inf-padded JAX solver output

Type: bug
Target: PyAutoLens
Repos:
- PyAutoLens
Difficulty: medium
Autonomy: safe
Priority: normal
Memory: wiki/galaxies/sources/massive-ellipticals.md; wiki/lensing/sources/dark-matter-substructure.md; wiki/galaxies/sources/light-profile-fitting.md
Issued: 2026-10-07
Status: formalised
Consequence: judge
Witness: a new test in test_autolens feeding `image_plane_multiple_image_positions_from` a 1-image array padded with inf rows fails on main and passes with the fix
Review-minutes: 20
Unattended: ready

PyAutoLens: single-image recovery in `Result.image_plane_multiple_image_positions_from` is blind to inf-padded JAX solver output.

Found while reviewing community PR PyAutoLens#765 (@samlange04, discussion https://github.com/orgs/PyAutoLabs/discussions/23 sibling report #30). In `autolens/analysis/result.py` (around line 138) the inward-walk recovery for a single-image solve tests `multiple_images.shape[0] <= 1`. With a JAX-backed analysis the point solver (`xp=jnp`, `remove_infinities` defaults to `xp is np` since #759) returns a static-shape array padded with `(inf, inf)` rows (20 rows), so the shape test is always false and the recovery can never fire under JAX. After #765 (which drops non-finite rows at `PositionsLH` construction and raises `PositionsException` when fewer than 2 finite rows remain) a 1-image JAX solve now raises at construction instead of silently scoring zero penalty. Fail-loud is better than silent zero, but SLaM chains on JAX could start erroring where they used to run.

Fix: count finite rows (`np.isfinite(...).all(axis=1).sum()`) before the `<= 1` check, or strip non-finite rows before it, so the recovery path triggers for padded output exactly as it does for the numpy solver. Add a unit test feeding a padded 1-image array and asserting the recovery path runs (and a 2-image padded array does not). Not yet reproduced with a real 1-image JAX solve; severity unknown. Check that the cached `files/multiple_image_positions.json` written from padded positions still round-trips.

<!-- formalised by the Intake (Conception) Agent on 2026-10-07 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/b718db7a-3dd7-461b-aa15-d27db7e34ca3/scratchpad/community/intake_al.md -->
