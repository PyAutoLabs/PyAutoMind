# Compose ClipperPriorBoxJoint with a bijector/scaler instead of refusing it

Type: bug
Target: PyAutoFit
Repos:
- PyAutoFit
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: formalised
Issued: 2026-08-28

## Request (verbatim)

ClipperPriorBoxJoint is refused whenever a bijector/scaler is set
(`multi_start_gradient/search.py:365-384`, `clipper.py:522-535`); Phase 8B
`log_reg` arms therefore settle at the `ell_comps` box corner `|e| = 1.414`.
Compose them: resolve each ball pair against the map and refuse only genuinely
non-linear pairs. Also add the in-process F5 pin test.

## Why it matters

The refusal is blanket, and it is stronger than the geometry requires. A ball is
a statement about physical coordinates, but a coordinate whose bijector kind is
`identity` with a linear scale `s` maps a disk of radius `R` to a disk of radius
`R / s` — still a disk, and still exactly projectable. Only a genuinely
non-linear pair (`log`, `logit`, or two identity coordinates with *different*
scales, which gives an ellipse) has no closed-form projection.

Because of the blanket refusal, every gradient arm that wants a `log` or `logit`
reparameterisation anywhere in the model has to drop the joint clipper entirely,
and its `ell_comps` lanes then settle at the box corner `|e| = 1.414` — outside
the disk, where the axis-ratio conversion saturates and the gradient is flat
(autolens_profiling#182: 20.1% of recorded lane best points, 0 of the 246 lanes
that reach the target basin).

## Design (approved — Option B)

- `autofit/non_linear/bijector.py`: add `AbstractBijector.identity_scales`,
  returning `float(self._scale[i])` where `self._kind_code[i] == _IDENTITY` and
  `None` otherwise, guarded by `_check_resolved()`.
- `autofit/non_linear/clipper.py`: replace the blanket raise with
  `_pairs_in_stepped_coordinates(pairs, scale, bijector)`, which returns
  `(i, j, radius / s)` when both members of a pair are identity-kind with a
  common linear scale `s`, and raises the existing `ValueError` — now naming the
  offending index pair and its kinds — otherwise.
- `autofit/non_linear/search/mle/multi_start_gradient/search.py`: delete the
  construction-time refusal; move the check into `_fit`, immediately after
  `self.bijector.from_model(model=model)` and before `_vmapped` is built, so a
  genuinely bad combination still dies before any likelihood evaluation.
- Do **not** round-trip through the bijector inside the clipper: the `logit`
  epsilon clamps would break bit-identity on unrelated coordinates, saturate
  gradients, and add traced ops.
- No new constructor arguments — `__identifier_fields__` stays untouched, so
  existing stored results are not re-keyed.

## Tests

- `test_autofit/non_linear/test_clipper.py`: rewrite the blanket-refusal test
  into the composition cases (`BijectorNone` bit-identical; a `log` on a
  non-`ell_comps` path composes; `BijectorLogit` on the ball model still raises
  and names the pair; a common scale projects onto `R / s`; a mixed scale
  raises; `BijectorDiagonal(ScalerPriorWidth())` with equal widths is accepted),
  and restate the search-wiring tests from "refused at construction" to "refused
  at model resolution, before the first step". Keep the identifier assertions.
- `test_autofit/non_linear/test_bijector.py`: F5 pin — a per-path map round
  trips **bit-exactly** on its identity coordinates.
- `test_autofit/non_linear/search/mle/test_multi_start_gradient.py`: the
  joint-clipper-plus-bijector combination constructs and `_fit` accepts an
  identity-mapped ball pair; a `logit`-on-`ell_comps` combination raises before
  the first step.

Unit tests stay NumPy-only (JAX is optional); the traced behaviour is covered by
a separate CPU integration script.

## Campaign implication (not done here)

The Phase 8B `logit` arm must be restated as a `BijectorPerPath` with `logit` on
every path *except* `ell_comps.*` in order to use the disk. That is a config
change in `autolens_profiling`, not a library change.
