# Phase 5e — `__JAX__` sections in `autogalaxy_workspace/scripts/guides/api/{data_structures,galaxies}.py`

Mirrors Phase 5a + Phase 5b for the autogalaxy workspace. Two files,
shorter sections than the autolens versions (no lensing-specific framing).

**Authoritative design doc:** `admin_jammy/notes/jax_interface.md`.
**Run in Opus** per [[feedback_tutorial_prose_opus]].
**Depends on:** Phase 5a + Phase 5b shipped (the autolens versions are the
canonical references; 5e adapts).

## Scope

Files in `autogalaxy_workspace/scripts/guides/api/`:

1. `data_structures.py` — `__JAX__` section mirroring Phase 5a, with
   lensing-specific examples (Tracer, source-plane) dropped.
2. `galaxies.py` — `__JAX__` section mirroring Phase 5b, with the
   single-galaxy and Galaxies-container framing; no Tracer.

**Out of scope:**
- A `tracer.py` or `lens_calc.py` mirror — those don't exist in
  autogalaxy_workspace (no lensing). The lensing-specific advanced material
  stays in autolens_workspace's Phase 5d guide.

## Notes for `data_structures.py`

Mirror of Phase 5a section. Adjustments:

- Drop the `tracer.image_2d_from(grid)` examples; use
  `galaxy.image_2d_from(grid)` or `galaxies.image_2d_from(grid)` instead.
- Drop the cross-reference to `lens_calc.py` (it doesn't exist in
  autogalaxy). Replace with: "For the canonical advanced 'JIT-it-yourself'
  treatment, see `autolens_workspace/scripts/guides/lens_calc.py` `__JAX__`
  section — the patterns there (decorator-on-def vs `jax.jit(bound_method)`,
  closure vs traced-argument, the `@jax.jit + xp=jnp` pairing rule) apply
  to autogalaxy primitives equally, just with `Galaxy` / `Galaxies` in place
  of `Tracer` / `LensCalc`."
- Length: similar to 5a (~80-120 lines), maybe slightly shorter.

## Notes for `galaxies.py`

Mirror of Phase 5b section. Adjustments:

- Replace every `Tracer` mention with `Galaxies` (the autogalaxy container).
- Adapt the `AnalysisImaging._register_fit_imaging_pytrees()` reference
  to the autogalaxy `ag.AnalysisImaging` (which does the same walk via
  the corresponding registration helper).
- Length: ~60-90 lines.

## Validation

Standard. Verify cross-references to Phase 5a/5b/5d resolve.

## References

- Phase 0 design doc.
- Phase 5a, 5b (autolens canonical versions — adapt from these).
- Phase 5d (cross-referenced for the advanced JIT-it-yourself patterns
  that apply across both workspaces).
