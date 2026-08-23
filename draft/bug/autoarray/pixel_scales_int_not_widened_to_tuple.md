# `pixel_scales` given as an `int` (or `np.float64`) is never widened to a tuple

Type: bug
Target: autoarray
Repos:
- @PyAutoArray
Difficulty: small
Autonomy: supervised
Priority: medium
Status: draft
Filed: 2026-08-09 (backfilled from git)

## Why this exists

Found while implementing PyAutoArray#333 (the `_validate_*` constructor guards,
shipped 2026-08-09 as PyAutoArray#440 / `f2f7a4f`). Noted in that PR's "Out of
scope" section and in `complete/2026/08/autoarray-input-validation-guards.md`;
this prompt is the follow-up it points at. **Pre-existing — not introduced by
that PR.**

## The defect

`autoarray/geometry/geometry_util.py`:

```python
def convert_pixel_scales_2d(pixel_scales):
    if type(pixel_scales) is float:          # <-- exact-type check
        pixel_scales = (pixel_scales, pixel_scales)
    return pixel_scales
```

`type(x) is float` is an exact-type test, so only a literal Python `float`
is widened. Everything else falls through **unconverted**, and the caller then
subscripts a scalar.

Verified against `main` @ `f2f7a4f` (2026-08-09):

```
convert_pixel_scales_2d(1)              ->  1              # not (1.0, 1.0)
convert_pixel_scales_2d(1.0)            ->  (1.0, 1.0)     # OK
convert_pixel_scales_2d(np.float64(1))  ->  np.float64(1)  # not widened
convert_pixel_scales_1d(1)              ->  1              # same bug, 1D sibling

Array2D.no_mask(values=np.ones((5,5)), pixel_scales=1)
    ->  TypeError: 'int' object is not subscriptable
```

`np.float64` matters as much as `int` here: it is what you get from indexing a
numpy array or reading a FITS header, so `pixel_scales=header["CD2_2"]` can hit
this on a path that looks perfectly reasonable.

## Why it is worth fixing

The docstring promises the widening — *"If this is input as a `float`, it is
converted to a `(float, float)` structure"* — and every `Mask2D` factory and
`Grid2D.uniform` funnel through this function, so the promise is repeated across
the public API. An `int` pixel scale is a natural thing for a user to type.

The resulting `TypeError: 'int' object is not subscriptable` names nothing the
caller passed — exactly the class of failure the #333 sweep was about, which is
why it is filed rather than fixed inline there (that task was scoped to the five
findings on #333).

## Suggested fix

Widen the test to any concrete real scalar rather than the exact `float` type.
`autoarray/validate.py` (landed by #440) already has the predicate this needs:

```python
from autoarray import validate

if validate.is_concrete_scalar(pixel_scales):
    pixel_scales = (pixel_scales, pixel_scales)
```

`is_concrete_scalar` accepts `int`, `float`, `np.integer`, `np.floating` and
rejects `bool`, arrays, `None` and JAX tracers — so this both fixes the bug and
keeps the function tracer-safe. Apply to `convert_pixel_scales_1d` (1-tuple) and
`convert_pixel_scales_2d` (2-tuple) together so the two do not drift.

**Check before assuming this is purely additive:** something downstream may rely
on a non-float passing through unconverted. Run the full `test_autoarray` suite
and read any failure rather than adjusting the test.

## Verification

- `Array2D.no_mask(values=..., pixel_scales=1)` builds, with
  `pixel_scales == (1.0, 1.0)`.
- Same for `np.float64(1.0)` and `np.int32(1)`.
- Tuple input is returned unchanged; a JAX tracer still passes through untouched.
- The #440 validation guards still fire on `0`, `-1` and `nan` in **both** the
  scalar and tuple forms.
- Decide and pin whether the widened value is cast to `float` or kept in its
  input type — `(1, 1)` vs `(1.0, 1.0)` — since downstream arithmetic differs.

Repro environment: `PYAUTO_SKIP_WORKSPACE_VERSION_CHECK=1`,
`NUMBA_CACHE_DIR=/tmp/numba_cache`, `MPLCONFIGDIR=/tmp/matplotlib`,
`PYAUTO_DISABLE_JAX=1`.

## Provenance

- Found during: `complete/2026/08/autoarray-input-validation-guards.md`
- Sibling of, but NOT part of, the @rhayes777 audit campaign (`planned.md` §
  `rhayes-audit-validation-phases-2-4`) — this was not one of his 16 findings.
