## joint-clipper-compose-with-bijector (a ball survives a COMMON linear rescale — R becomes R/s, so the blanket refusal was stronger than the geometry)
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1539
- completed: 2026-08-28
- library-pr: PyAutoFit#1540 (merged 54aa0875b42c8c8107fe980c483a69a61ee91deb -> main)
- summary: `ClipperPriorBoxJoint` no longer refuses every `scaler`/`bijector`; each declared ball pair is resolved against the map and only genuinely non-linear pairs are refused. Unblocks the Phase 8B `ell_comps` box-corner pathology (autolens_profiling#185: half of all scored rows excluded for `|e| >= 1`).
- design: Option B, approved before implementation.

### The geometry, which is the whole argument
A ball is a statement about physical coordinates, but it survives a **common** linear rescale of both its members: `theta_i**2 + theta_j**2 <= R**2` is exactly `phi_i**2 + phi_j**2 <= (R/s)**2`. A disk of radius `R` therefore *is* a disk of radius `R/s` in the stepped coordinates, and the radial shrink — a pure multiply — projects onto it correctly. Only a genuinely non-linear pair has no closed form: a `log`/`logit` kind, or two identity coordinates with **different** scales, which gives an ellipse whose nearest-point projection is the root of a quartic rather than a radial shrink.

### What shipped
- `autofit/non_linear/bijector.py` — new `AbstractBijector.identity_scales`: `List[Optional[float]]`, the per-coordinate linear scale where the kind is `identity`, `None` where it is not, guarded by `_check_resolved()`. `None` rather than `1.0` for `log`/`logit` is deliberate — a log coordinate is not a coordinate scaled by one, and reporting it as such would let a caller compose with it silently and wrongly.
- `autofit/non_linear/clipper.py` — new `ClipperPriorBoxJoint.pairs_in_stepped_coordinates(pairs, scale, bijector)` resolves each declared ball pair against the map, returning `(i, j, radius / s)` for a pair sharing one common positive linear scale and raising the existing `ValueError` — now naming the offending index pair and its kinds — otherwise. `project` calls it in place of the old blanket raise. A "Composition with a scaler/bijector" docstring section carries the `R -> R/s` argument.
- `autofit/non_linear/search/mle/multi_start_gradient/search.py` — the construction-time refusal is deleted; the check runs once in `_fit`, immediately after `self.bijector.from_model(model=model)` and before `_vmapped` is built. Whether the two compose is a question about the **model** — which pairs carry a ball, and how the map treats each — and no model exists at construction; making it here is still before any likelihood evaluation, so a bad combination does not die a minute into a multi-hour fit. `bfgs/search.py` is untouched: LBFGS still refuses the joint clipper wholesale, because scipy has no ball.
- **Deliberately NOT round-tripped through the bijector.** That would be correct for every kind, but it would drag the `logit` epsilon clamps across coordinates the ball has nothing to do with — breaking the bit-identity the interior-point path promises, saturating gradients at the clamped edges, and adding traced ops to every step. Dividing the radius costs nothing and is exact.

### API changes — additive only; no existing signature, default or result changes
- New: `autofit.AbstractBijector.identity_scales` (property; requires `from_model` first) and `ClipperPriorBoxJoint.pairs_in_stepped_coordinates(pairs, scale=None, bijector=None)`.
- Relaxed: `af.MultiStartAdam(clipper=af.ClipperPriorBoxJoint(), bijector=...)` (and `scaler=...`) no longer raises at construction. Combinations that previously raised there now either work (identity-mapped ball pair under one common scale) or raise the same `ValueError` class at model resolution inside `_fit`, before the first likelihood evaluation. A previously-raising combination cannot start silently doing something different — the map is resolved and either accepted or refused, never applied approximately.
- Unchanged: `ClipperPriorBox.__identifier_fields__` stays `("margin", "strict_epsilon")` — the composition takes no new constructor argument, so no stored result is re-keyed. Pinned by a test.
- Downstream: nothing in PyAutoGalaxy or PyAutoLens calls the changed methods; both continue to declare geometry via `__model_ball_constraints__` and are unaffected.

### Validation
- `test_autofit/` full (worktree PyAutoFit first on PYTHONPATH): **2301 passed, 3 skipped** in 80s — base `f466dce1a` was 2288 passed / 3 skipped, so +13 new tests. `test_autofit/non_linear` 717 passed, 2 skipped. `test_autogalaxy/profiles` 716 passed; `test_autolens/analysis` 62 passed (canonical checkouts against the worktree autofit).
- New tests, NumPy-only as the suite requires: `TestJointBallComposesWithAMap` (BijectorNone bit-identical; a `log` on a non-ball path composes and still projects the corner onto the disk; `BijectorLogit` on the ball pair raises naming `(0, 1)`; a common `scale=[2,2,1]` projects onto 0.999/2; `scale=[2,3,1]` raises; `BijectorDiagonal(ScalerPriorWidth())` with equal pair widths is accepted; a model declaring no ball is unaffected) · `TestJointBallSearchWiring` restated from "refused at construction" to accepted-at-construction/refused-at-model-resolution, plus the identifier pin · `test_bijector.py::test__round_tripping_a_per_path_map_is_bit_exact_where_it_is_identity` — the **F5 pin**, identity coordinates round-trip with `==` and the `log` one to rel 1e-12; this is what the radius-division shortcut rests on, and it is also the sound in-process F5 owed by autolens_profiling#185.
- Traced JAX/CPU integration, run outside the unit suite: `MultiStartAdam(clipper=ClipperPriorBoxJoint(), bijector=BijectorPerPath({"einstein_radius": "log"}))` on a toy model whose optimum sits at `|e| = 2.0` (outside the disk, so the gradient pushes outwards every step and only the clipper can hold a lane) — model resolution `[(0, 1, 0.999)]`, final `|e| = 0.999` on all 8 lanes, 0 grad-NaN, 0 value-NaN, and **874 clipped lane-steps**. Those 874 matter: without them the `|e| <= 0.999` assertion would be vacuous. The counterfactual was checked too — the same fit with `BijectorLogit()` raises before the first step, naming the pair and its `(logit, logit)` kinds.
- `black` 25.1.0: changed regions clean. Base files were not black-clean and the resulting unrelated re-wrap churn was reverted, so the diff is change-only.
- heart-ack: shipped + merged under the human-authorised RED override, sole red reason verbatim "release validation FAILED (stage integrate)". The two YELLOW reasons (workspace validation `rectangular_mge*`, session-start-hook manifest drift) are unrelated to this change.

### Campaign follow-up (deliberately out of scope, no prompt filed)
To actually use the disk, the Phase 8B `logit` arm must be restated as a `BijectorPerPath` carrying `logit` on every path **except** `ell_comps.*`. That is a config change in `autolens_profiling`, not a library change, and it belongs with the final 39-arm verdict re-run rather than here.

## Original prompt

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
