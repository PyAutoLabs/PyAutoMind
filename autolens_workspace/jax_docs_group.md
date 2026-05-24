# Phase 3e — `__JAX__` sections in `autolens_workspace/scripts/group/*.py`

> **⚠ DEFERRED — optional. Author/issue only if Phase 3a/3b/3d/3c have shipped
> and group is judged worth the cleanup.**
>
> Per design doc (`admin_jammy/notes/jax_interface.md` §3.6) scope anchor:
> group is an advanced/niche dataset type and the user audience is small.
> The Phase 0 audit confirmed group/start_here.py has no `__JAX__` content
> today. Don't add prose unless the group dataset type sees regular user
> traffic that warrants it.

**Authoritative design doc:** `admin_jammy/notes/jax_interface.md`.
**Run in Opus** per [[feedback_tutorial_prose_opus]].

## Scope (if authored)

Files in `autolens_workspace/scripts/group/`:

1. `start_here.py` — add fresh `__JAX__` section (none exists today),
   mirroring 3a's framing but lighter — group is a niche dataset type and
   the prose should reflect that.
2. `simulator.py` — `__JAX__` prose. `__JAX Variant__` only if the group
   simulator is `SimulatorImaging`-shaped enough that the 3a variant
   translates cleanly.
3. `fit.py`, `modeling.py`, `likelihood_function.py` — `__JAX__` prose
   sections as per 3a.
4. `source_science.py`, `slam.py` — JAX-aware refresh only if these
   tutorial scripts directly demonstrate analysis instantiation. Otherwise
   skip.

**Out of scope:** `features/`.

## Group-specific notes

Group lensing has unique modeling patterns (multiple main galaxies + extra
galaxies + group halo) that may or may not affect the JAX framing. Verify
at authoring time. If the group pipeline calls `tracer.image_2d_from`
directly anywhere, those sites might benefit from the lens_calc.py
JIT-it-yourself pattern (Phase 5d) cited inline.

## Validation

Standard.

## References

- Phase 0 design doc.
- Sibling: `autolens_workspace/jax_docs_imaging.md` (3a — canonical template).
