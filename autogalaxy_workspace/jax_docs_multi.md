# Phase 4c — `__JAX__` sections in `autogalaxy_workspace/scripts/multi/*.py`

> **⚠ DEFERRED — author/issue only after Phase 4a, 4b have shipped clean.**
>
> Per design doc (`admin_jammy/notes/jax_interface.md` §3.6) scope anchor:
> autogalaxy multi-wavelength is secondary to imaging + interferometer.
> Wait for the core autogalaxy phases to ship before taking this on.

Mirror of Phase 3c (autolens multi) for the autogalaxy workspace.

**Authoritative design doc:** `admin_jammy/notes/jax_interface.md`.
**Depends on:** Phase 2 shipped + Phase 4a/4b shipped clean.
**Run in Opus** per [[feedback_tutorial_prose_opus]].

## Scope (if authored)

Files in `autogalaxy_workspace/scripts/multi/`:

1. `start_here.py` — refresh existing `__JAX__` content at lines 22, 259
   (per Phase 0 audit).
2. `simulator.py` — `__JAX__` prose if appropriate.
3. `modeling.py` — `__JAX__` prose mirroring 4a's fit.py with the multi-band
   `af.FactorGraphModel(use_jax=True)` addition.

**Out of scope:** `features/`.

## Validation

Standard.

## References

- Phase 0 design doc.
- Sibling: `autogalaxy_workspace/jax_docs_imaging.md` (4a — canonical
  autogalaxy template).
- Reference for multi-specific framing: `autolens_workspace/jax_docs_multi.md`
  (3c).
