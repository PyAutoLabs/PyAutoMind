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
