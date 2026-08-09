# PyAutoArray#333: constructor validation guards — and the shared `_validate_*` home

Type: bug
Target: autoarray
Repos:
- @PyAutoArray
Difficulty: medium
Autonomy: supervised
Priority: high
Status: draft

## Why this exists

[PyAutoArray#333](https://github.com/PyAutoLabs/PyAutoArray/issues/333), filed
2026-05-23 by @rhayes777 while auditing released `2026.5.21.1`. Five findings —
B5, B6, B7, B8, B13 — all re-verified against `main` on 2026-07-28 and **all five
still reproduce**. Answered on the issue 2026-07-28
(`#issuecomment-5105855009`); the epic
[PyAutoArray#415](https://github.com/PyAutoLabs/PyAutoArray/issues/415) is the
public watch point promised to the reporter.

This is the **anchor prompt of phase 2**. It carries the one decision the other
two validation prompts wait on: *where the shared `_validate_*` helper lives*.
PyAutoArray is the natural floor — PyAutoGalaxy and PyAutoLens both depend on it —
so the helper is defined here and imported downstream. Ship this first, or the
three repos emit inconsistent messages for the same class of mistake.

## Scope — five findings

Each is "raise a clear `ValueError` at construction instead of a confusing
NumPy/numba traceback three calls later".

| ID | Surface | Today | Wanted |
|---|---|---|---|
| B6 | `Array2D.no_mask(pixel_scales=…)` | `0.0`, `-0.1`, `nan` all accepted; `ps=0` then `ZeroDivisionError` on the first `derive_grid`, `-0.1` silently flips the geometry, `nan` propagates | `ValueError` naming `pixel_scales`, requiring finite and positive |
| B7 | `Mask2D.circular_annular(inner_radius > outer_radius)` | accepted, `pixels_in_mask == 0` | `ValueError` — almost always swapped arguments |
| B8 | `Grid2D.uniform(shape_native=(0, 0))` / `(0, 5)` | accepted, `shape_slim == 0` | `ValueError` — both axes must be positive |
| B5 | `Imaging(data 10x10, noise_map 5x5)` | built; `shape_native` reports `(10, 10)`, the mismatch is swallowed | `ValueError` naming both shapes |
| B13 | `reg.Constant(coefficient=-1.0)` | accepted, stored as `-1.0` | `ValueError` — negative is unphysical |

B5 is filed on this issue rather than PyAutoLens because `Imaging` lives at
`autoarray/dataset/imaging/dataset.py`.

## B13 is not inert — sharpened beyond the original report

`constant.py:43` computes `regularization_coefficient = coefficient * coefficient`,
which is why `log_evidence` comes out identical for `+1.0` and `-1.0` and why the
reporter read the value as merely cosmetic. **But `regularization_weights_from`
(`constant.py:127`) returns the raw, un-squared `self.coefficient`** — so a
negative coefficient leaks negative regularization weights into every consumer of
that method. Reject it at construction.

## Binding constraint — JAX

These constructors sit on **JAX-traced** paths. Guards must stay correct under
tracing and cost nothing when traced: **no Python `if` on a value that may be a
tracer** without first establishing it is concrete. This constraint is carried
forward from phase 1, where it held.

## The decision this prompt owns

Before writing any guard, settle and record in the PR description:

1. **Where the helper lives** — module path within PyAutoArray, and its public
   or private status, given PyAutoGalaxy and PyAutoLens will import it.
2. **The message shape** — one template all three repos reuse, e.g.
   `f"pixel_scales must be a finite positive number; got {pixel_scales!r}"`.
   Name the parameter, state the rule, show the received value.
3. **The tracer-safe form** — how a guard distinguishes a concrete value from a
   tracer, written once so the downstream prompts copy rather than reinvent it.

## Verification

- Regression test per finding, built from the reporter's own snippet in the issue
  body (they are self-contained).
- Assert the message names the offending parameter, not just that *something*
  raised.
- Controls that must keep passing: valid `pixel_scales`, a well-ordered annulus,
  a non-degenerate `shape_native`, matched `data`/`noise_map` shapes, and
  `reg.Constant(coefficient=1.0)`.
- Library unit tests stay **numpy-only** (no JAX), per phase 1.

Repro environment gotchas (from the 2026-07-28 verification run): run from a
workspace root with `PYAUTO_SKIP_WORKSPACE_VERSION_CHECK=1`,
`NUMBA_CACHE_DIR=/tmp/numba_cache`, `MPLCONFIGDIR=/tmp/matplotlib`,
`PYAUTO_DISABLE_JAX=1`. The PSF constructor is `al.Convolver.from_gaussian` —
`al.Kernel2D` no longer exists.

## Out of scope

- The `adapt_images` precondition error (#332) — `rhayes_332_adapt_images_precondition_error.md`.
- Profile-constructor guards (PyAutoGalaxy#440) — `rhayes_440_profile_validation_guards.md`.
- `Tracer` guards (PyAutoLens#532) — `rhayes_532_tracer_validation_guards.md`.

## Do not route to `start_dev_for_user`

@rhayes777 offered "Happy to PR if useful". The human declined that warmly on
2026-07-28 — these are JAX-traced hot paths and are not a fair hand-off. **We
implement in-house.**

## Provenance

- Epic: PyAutoArray#415 (open — phases 2-4)
- Campaign prompt: `draft/bug/autoarray/rhayes_audit_validation_and_crashes.md`
- Registry: `planned.md` § `rhayes-audit-validation-phases-2-4`
- Phase 1 shipped 2026-07-28: PyAutoArray#417 (`9411904d`) + PyAutoLens#662 (`2a3f1a63`)
