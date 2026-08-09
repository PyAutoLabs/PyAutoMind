Phase 2 (PyAutoArray half) of the @rhayes777 API audit. Five findings on
[PyAutoArray#333](https://github.com/PyAutoLabs/PyAutoArray/issues/333) — B5, B6, B7,
B8, B13 — all reproducing on `main` at the start, all closed at construction.

**Shipped:** PyAutoArray#440, squash-merged `f2f7a4f` 2026-08-09. Issue #333 closed;
tracking issue #439 closed. Epic #415 stays open for phases 3-4.

## Delivered

Guards went in at **chokepoints**, not the five reported call sites, so coverage
exceeded the report:

| Finding | Guard site | Reach beyond the report |
|---|---|---|
| B6 `pixel_scales` ≤ 0 / nan | `geometry_util.convert_pixel_scales_{1d,2d}` | every `Mask2D` factory + `Grid2D.uniform` funnel through it |
| B8 zero-length `shape_native` | `Mask2D.__init__` | every factory returns through it |
| B7 annulus `inner >= outer` | `circular_annular` + `elliptical_annular` | the elliptical sibling had the identical hole |
| B5 `noise_map` shape ≠ `data` | `AbstractDataset.__init__` | covers `Interferometer` and every subclass, not just `Imaging` |
| B13 negative coefficient | all **14** regularization schemes | reporter named `Constant`; 13 siblings had the same hole |

## The decision this task owned (the recorded phase-2 blocker)

**Shared helper home: `autoarray/validate.py`**, public — `is_concrete_scalar`,
`validate_positive_finite`, `validate_non_negative_finite`, `validate_pixel_scales`,
`validate_shape_native`, `validate_radii_ordered`.

**Message shape:** name the parameter, state the rule, show the received value, plus
an optional sentence of guidance.

**Tracer-safe form:** every value guard is gated on `is_concrete_scalar` and passes
non-concrete values straight through, so a Python truth-test never reaches a tracer.
Shape checks need no gate — shapes are static under tracing.

This unblocks the two siblings, which import rather than reinvent it.

## Verified, not assumed

- **B13 was a live bug, not cosmetic.** Confirmed the leak empirically *before*
  fixing: `Constant(-1.0).regularization_weights_from` returned `[-1. -1. -1. -1.]`.
  `regularization_matrix_from` squares the coefficient and hides the sign;
  `regularization_weights_from` returns it unsquared. The reporter had read it as
  inert; it wasn't.
- **Tracer-safety against real JAX 0.11.0**, not just the test stand-in: construction
  of `reg.Constant` / `reg.Adapt` under `jax.jit` works, `jax.grad` flows through a
  traced coefficient (grad `16.0` for `sum((c·1)²)` at `c=2` over 4 params), and a
  concrete `-1.0` outside a trace is still rejected.

## Validation

- Full suite **980 passed / 52 skipped**, **+44 new tests** in
  `test_autoarray/test_validate.py` — one regression test per finding from the
  reporter's own snippets, plus a control per finding so no guard can pass by
  rejecting everything.
- The 3 `test_transformer.py` pynufft failures are **pre-existing** — baselined by
  stashing the branch and re-running on clean `main` (identical 3). Tracked by
  `draft/bug/autoarray/pynufft_scipy_pinv2_dev_extra.md`.
- CI green on both `unittest (3.12)` and `unittest (3.13)`.
- **Zero regressions.**

## What the planning got wrong (worth carrying forward)

- **The Bug Agent and sizing faculty both returned `too-large` (score 10) with a
  "too large for one PR" risk.** The human chose one PR. The final diff was 130
  insertions / 0 deletions across 16 files — small and uniform. The heuristic keys
  off prompt length, and this prompt was long because it carried phase-1 evidence,
  not because the change was large. **Do not let prompt length stand in for diff
  size on a mechanical sweep.**
- **The flagged risk of triaging existing degenerate-construction tests was ZERO.**
  Nothing in the suite relied on a zero pixel scale, an empty shape, a swapped
  annulus, a mismatched noise map, or a negative coefficient. Chokepoint guards were
  cheaper than expected.
- **A concurrent session split the same campaign on main** (`520dafc9`) while this
  session was doing it independently. Cost one reconciliation commit. Both splits
  reached the same four-prompt shape. Check `origin/main` for campaign-level
  restructuring before splitting a multi-issue prompt.

## Follow-ups

- **Adjacent defect, found and deliberately not fixed:**
  `geometry_util.convert_pixel_scales_2d` tests `type(pixel_scales) is float`, so an
  `int` pixel scale is never widened to a tuple. Needs its own prompt.
- Siblings now unblocked: `draft/bug/autogalaxy/rhayes_440_profile_validation_guards.md`
  and `draft/bug/autolens/rhayes_532_tracer_validation_guards.md`.
- `draft/bug/autoarray/rhayes_332_adapt_images_precondition_error.md` (phase 3) was
  never blocked and can start any time.

## Original prompt

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
