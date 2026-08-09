# PyAutoArray#333 — constructor input-validation guards (B5, B6, B7, B8, B13)

Type: bug
Target: autoarray
Repos:
- @PyAutoArray
Difficulty: medium
Autonomy: supervised
Priority: high
Status: draft

## Why this exists

This is the **PyAutoArray half of phase 2** of @rhayes777's 2026-05-23 API audit, split
out of `draft/bug/autoarray/rhayes_audit_validation_and_crashes.md` per the Mind rule
*one prompt = one task = one PR*. That parent prompt carries the full audit, the phase-1
completion record, and the phases 2-4 table; read it for context, not for scope.

Scope here is **[PyAutoArray#333](https://github.com/PyAutoLabs/PyAutoArray/issues/333)
only** — the five findings that live in PyAutoArray. The PyAutoGalaxy half of phase 2
(#440: B9, B11, B12) and the negative-redshift item from PyAutoLens#532 are a **sibling
task**, deliberately sequenced *after* this one because they consume the shared validation
helper this task establishes.

All five findings were re-verified against `main` on 2026-07-28 and **all five still
reproduce**. Epic: [PyAutoArray#415](https://github.com/PyAutoLabs/PyAutoArray/issues/415)
(stays open). Phase 1 shipped 2026-07-28 as PyAutoArray#417 + PyAutoLens#662.

## The five findings

| ID | Reproduction (verified 2026-07-28) | Today's behaviour |
|---|---|---|
| B6 | `Array2D` / `Mask2D` with `pixel_scales=0.0`, `-0.1`, `nan` | all accepted; `ps=0` then `ZeroDivisionError` on the first `derive_grid`; negative silently flips the geometry |
| B7 | `Mask2D.circular_annular(inner_radius=0.8, outer_radius=0.3)` | accepted, `pixels_in_mask = 0` (a silently empty mask from swapped arguments) |
| B8 | `Grid2D.uniform(shape_native=(0, 0))` and `(0, 5)` | accepted, `shape_slim = 0` |
| B5 | `Imaging(data=<10x10>, noise_map=<5x5>)` | constructed; `shape_native` reports `(10, 10)`, the conflict is swallowed |
| B13 | `reg.Constant(coefficient=-1.0)` | accepted and stored as `-1.0` |

**B13 — the sharpened finding (not in the reporter's original).** `constant.py:44` does
`regularization_coefficient = coefficient * coefficient`, which is why `log_evidence` is
identical for `+1.0` and `-1.0` — the reporter concluded the value is inert. It is not:
`Constant.regularization_weights_from` (`constant.py:126`) returns the **raw, un-squared**
`self.coefficient`, so a negative value leaks negative regularization weights into every
consumer of that method. Rejecting at construction is what closes this.

## Binding constraints (carried from phase 1)

1. **These constructors sit on JAX-traced paths.** `coefficient` in particular is a free
   model parameter, so under a traced fit the constructor is handed a JAX tracer. A plain
   Python `if coefficient < 0:` on a tracer raises `TracerBoolConversionError`. Every
   guard must therefore be **type-gated on a concrete scalar** and skip anything it does
   not recognise — never a truth-test on an arbitrary value. The house idiom already
   exists at `autoarray/dataset/imaging/simulator.py:271` (`if xp is np and ...`, with the
   comment explaining why); follow it.
2. **Decide where the shared `_validate_*` helper lives before writing it.** This was the
   stated blocker on phase 2 in `planned.md`. PyAutoArray is the natural floor —
   PyAutoGalaxy and PyAutoLens both depend on it — and the sibling #440 task will import
   whatever this task lands. Three repos writing their own helpers is the failure mode to
   avoid.
3. **Guards raise, they do not warn.** All five are unambiguously invalid input. (The one
   genuinely judgement-call finding in the audit, `z_lens > z_source`, is phase 4 and is
   HELD on the reporter's answer — it is not in this task.)

## Code sites (read against PyAutoArray `main` @ 5867db0)

- **B6** — `autoarray/geometry/geometry_util.py:190 convert_pixel_scales_2d` is the single
  chokepoint: every `Mask2D` factory and `Grid2D.uniform` funnel through it. Its 1D sibling
  is `convert_pixel_scales_1d` at line 32.
- **B7** — `autoarray/mask/mask_2d.py:393 Mask2D.circular_annular`. Its sibling
  `elliptical_annular` (line 504) has the same inner/outer shape and the same hole.
- **B8** — `autoarray/mask/mask_2d.py:47 Mask2D.__init__` is the chokepoint; every factory
  returns through `cls(...)`, and `Grid2D.uniform` → `Grid2D.no_mask` →
  `Mask2D.all_false` (`uniform_2d.py:272`) lands there too.
- **B5** — `autoarray/dataset/abstract/dataset.py AbstractDataset.__init__`, where
  `self.data` and `self.noise_map` are assigned. Guarding here covers `Imaging`,
  `Interferometer` and every other dataset subclass, not just the reported one.
- **B13** — `autoarray/inversion/regularization/`. Eight classes assign `self.coefficient`
  (`constant`, `zeroth`, `brightness_zeroth`, `curvature_mask`, `fourth_order_mask`,
  `exponential_kernel`, `gaussian_kernel`, `matern_kernel`); `adapt` and
  `matern_adapt_kernel` carry `inner_coefficient`/`outer_coefficient`; `constant_zeroth`
  carries `coefficient_neighbor`/`coefficient_zeroth`. `ConstantSplit` and `AdaptSplit`
  inherit. The reported class is one of thirteen entry points.

## Precedents to follow (do not invent a new style)

- `autoarray/dataset/imaging/dataset.py:24 _validate_convolve_over_sample_size` — the
  existing module-level private validator, raising `TypeError` for a wrong type and
  `exc.DatasetException` for a bad value.
- `autoarray/inversion/pixelization.py:155` — phase 1's own construction-time rejection,
  and the template for message quality: it names the offending classes, explains *why* the
  combination is unsupported, and lists the working alternatives.
- `autoarray/exc.py` already has `MaskException`, `ArrayException`, `GridException`,
  `DatasetException` — use the matching one rather than a bare `ValueError` where the
  module already has a home exception.

## Definition of done

- All five reproductions from the issue body raise a clear, named error at construction.
- Guards are proven inert under tracing (a JAX-traced construction still works).
- Regression tests assert the **failure**, one per finding, built from the reporter's own
  snippets.
- The shared helper has one documented home in PyAutoArray that the sibling #440 task can
  import.
- Full `test_autoarray` suite green — a guard at a chokepoint this central will surface
  existing tests that construct degenerate objects on purpose; each one is triaged, not
  bulk-suppressed.
- #333 gets a closing comment; epic #415 stays open for phases 3-4.

## Verification recipe

Snippets in the issue body are self-contained. Environment:
`PYAUTO_SKIP_WORKSPACE_VERSION_CHECK=1`, `NUMBA_CACHE_DIR=/tmp/numba_cache`,
`MPLCONFIGDIR=/tmp/matplotlib`, `PYAUTO_DISABLE_JAX=1`. Note the PSF constructor is
`al.Convolver.from_gaussian` — `al.Kernel2D` no longer exists.
