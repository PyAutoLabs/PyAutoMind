# Phase 3c — `__JAX__` sections in `autolens_workspace/scripts/multi/*.py`

> **⚠ DEFERRED — author/issue only after Phase 3a, 3b, 3d have shipped clean.**
>
> Per design doc (`admin_jammy/notes/jax_interface.md` §3.6) scope anchor:
> the core API user surface is `imaging`, `interferometer`, `point_source`.
> Multi-wavelength is secondary. Wait for the core to ship clean before
> taking this on so the lessons from those rollouts carry over.

The multi/start_here.py already has `__JAX__` sections at lines 38, 306 and
shows `use_jax=True` at line 317 (`AnalysisImaging(..., use_jax=True)`) and
line 348 (`af.FactorGraphModel(..., use_jax=True)`). This prompt's job is
**cleanup**, not addition.

**Authoritative design doc:** `admin_jammy/notes/jax_interface.md`.
**Depends on:** Phase 2 shipped + lessons from 3a/3b/3d rollout.
**Run in Opus** per [[feedback_tutorial_prose_opus]].

## Scope

Files to edit, all in `autolens_workspace/scripts/multi/`:

1. `start_here.py` — refresh existing `__JAX__` content at lines 38 and 306
   to align with the Phase 0 contract. Drop any framing that contradicts
   the contract; add the multi-specific note about `FactorGraphModel(use_jax=True)`.
2. `simulator.py` — add `__JAX__` prose. (Multi simulators may not warrant
   an `__JAX Variant__` block — the multi pattern composes per-band imaging
   simulators; check what makes sense at authoring time.)
3. `modeling.py` — `__JAX__` prose mirroring 3a's fit.py with the
   multi-band addition.

**Out of scope:** `features/`, `plot.py`.

## Multi-specific notes

- `af.FactorGraphModel(*analysis_factor_list, use_jax=True)` is the
  multi-band entry point — Phase 0 audit confirmed it exists at
  `multi/start_here.py:348`. The prose should note this is the same
  default-on, opt-out story as single-dataset Analysis.
- Per-band `AnalysisImaging(use_jax=True)` is already shown at line 317.

## Validation

Standard: all scripts run on NumPy, smoke test passes, `check_sizes.sh`
passes.

## References

- Phase 0 design doc.
- Sibling: `autolens_workspace/jax_docs_imaging.md` (3a — canonical
  template).
- Phase 2 (library dependency): `autoarray/simulator_use_jax.md`.
