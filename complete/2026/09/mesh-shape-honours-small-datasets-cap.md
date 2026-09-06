# Pixelization mesh shapes honour PYAUTO_SMALL_DATASETS like Grid2D.uniform and Mask2D.circular do

PyAutoArray#529 → `bcd15cd9`, closing PyAutoArray#528, merged 2026-09-06 on branch
`claude/ci-test-timing-epic-ke2lul`. Phase 8c (library leg) of the `ci-timing-fast-tests`
epic; the systemic form of the four script guards HowToLens#77 / HowToGalaxy#73 added.

- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/528
- completed: 2026-09-06
- library-pr: https://github.com/PyAutoLabs/PyAutoArray/pull/529

## What shipped
- `cap_mesh_shape_for_small_datasets` applied in the rectangular mesh family's single
  `self.shape` assignment and `image_mesh.Overlay`, per axis with `min`, with the
  `respect_small_datasets=True` hatch threaded through the subclasses (not stored on the
  instance, so `__eq__` / serialization are untouched). 1449 tests pass.
- With the branch installed: autolens_workspace_test 27/27, autogalaxy_workspace_test
  39/39 (the `_test` JAX scripts run uncapped, so their pins did not move); the four HowTo
  chapter-3 scripts unchanged in time (their guards resolve to the same `(16, 16)`).

## Key traps / findings
- A cap that reaches the data but not the model is worse than no cap: a capped run was
  solving a *harder*, more degenerate inversion (1600–2500 source pixels from ~80 image
  pixels). ~28 further call sites across the four workspaces are now covered.

## Follow-ups
- `draft/maintenance/autoarray/small_datasets_followups_after_8c.md`: revert the four
  now-redundant HowTo script guards in a small workspace PR after the PyAutoArray release.

## Original prompt

# Pixelization mesh shape honours PYAUTO_SMALL_DATASETS like Grid2D.uniform and Mask2D.circular do

Type: feature
Target: PyAutoArray
Repos:
- PyAutoArray
- HowToLens
- HowToGalaxy
- autolens_workspace
- autogalaxy_workspace
Difficulty: medium
Autonomy: supervised
Priority: high
Status: formalised
Filed: 2026-09-06
Epic: ci-timing-fast-tests
Phase: 8c
Issued: 2026-09-06

Library leg of phase 8 (autolens_workspace#536): a shared-machinery finding from the
user-workspace slow-script diagnosis, traced to the unguarded call in the library and written
up as a diff there rather than patched per script. The measurement and the diff below are the
phase-8 executor's; nothing was applied to the library. Library-first gate: this lands before
any workspace script relies on it. Validation: the library unit tests plus a before/after of
the named workspace scripts under the smoke profile.

## (b-lib) PyAutoArray — mesh `shape` does not honour `PYAUTO_SMALL_DATASETS` (the systemic form of the fix landed here)

**Files** the `Rectangular*` / `Overlay` mesh and image-mesh constructors under
`autoarray/inversion/pixelization/`

`Grid2D.uniform` and `Mask2D.circular` both cap `shape_native` to
`SMALL_DATASETS_SHAPE_NATIVE` under `PYAUTO_SMALL_DATASETS=1`
(`autoarray/structures/grids/uniform_2d.py:228,570`). A pixelization's `shape=` does not, so a
capped run reconstructs 1600–2500 source pixels from ~80 image pixels. Capping mesh `shape` the
same way (with the same `respect_small_datasets=True` escape hatch the grid already has) would
subsume every per-script guard added by this phase and reach ~28 further call sites across the
four repos that were left alone here.

**Measured** on the four scripts fixed script-side: 43.6 s -> 17.3 s locally.

If this lands, the four script-level guards below become redundant-but-harmless (they resolve to
the same shape) and can be reverted in one pass.
