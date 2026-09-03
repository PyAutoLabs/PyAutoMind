# Re-pin the knife-edge positions_threshold tests after PyAutoArray#519's exact grid transform

Type: bug
Target: autolens
Repos:
- @PyAutoLens
Themes:
- point-source
- testing
Difficulty: small
Autonomy: supervised
Priority: high
Status: active
Filed: 2026-09-03
Issued: 2026-09-03

## Symptom

`PyAutoLens` `main` is RED (`pyauto-heart readiness --json` reason `PyAutoLens: CI failure`).
Two tests in `test_autolens/analysis/test_result.py` fail against the current library `main`s:

- `test__positions_threshold_from` — `positions_threshold_from()` returns
  `0.0019534291030939357`, pinned at `0.0019501455607163743`; `positions_threshold_from(factor=5.0)`
  returns `0.009767145515469679`, pinned at `0.009750727803581872`.
- `test__positions_likelihood_from__mass_centre_radial_distance_min` — `positions[1]` returns
  `(1.0009765625, 0.0005638186222554754)`, pinned at `(1.00097656e00, -5.63818622e-04)`; the x
  component has flipped sign and its magnitude is bit-identical. `positions[0]` is unchanged at
  `(-1.0009765625, 0.0005638186222554754)`.

## Bisect attribution

Bisected across the day's PyAutoArray/PyAutoGalaxy merges with detached scratch worktrees, holding
`PyAutoLens` fixed:

| PyAutoArray | PyAutoGalaxy | result | `positions_threshold_from()` |
|---|---|---|---|
| `main` | `main` | FAIL | `0.0019534291030939357` |
| `62feb7eb^` | `main` | PASS | `0.0019501455607163743` |
| `main` | `50599c2c` | FAIL | — |
| `main` | `2c729217` | FAIL | — |
| `main` | `8d152b15` | FAIL | — |
| `62feb7eb^` | `8d152b15` | PASS | — |

PyAutoArray#519's rotation-matrix rewrite of `transform_grid_2d_to_reference_frame` (commit
`f45b30b0`) is the **sole mover**. The three PyAutoGalaxy merges are bit-neutral.

## Accuracy verdict

The fixture is exactly mirror-symmetric: the `Isothermal` lens centre is `(0.1, 0.0)`, the
`SersicSph` source is at `(0.0, 0.0)`, `ell_comps=(0.0, 0.0)` — both lie on `x = 0`. The new
transform is an **exact identity at angle 0** (measured error `0.0`; the old polar
`cos/sin`-of-`arctan2` form carried `8.9e-16`). Consequently the on-axis deflection `alpha_x` is now
exactly `0.0` where it was `6.1e-17`. The point solver therefore hits an exact tie and its
tie-break selects the other branch, sending both images to the same side of the axis.

The new values are the **more accurate** branch — they come from an exact transform and an exact
on-axis zero. Nothing in the library is wrong; the pinned quantity is a knife-edge, not a physical
constant.

## Knife-edge numbers

- pre-#519 transform error at angle 0: `8.9e-16`; post-#519: `0.0` (exact identity).
- on-axis `alpha_x`: pre `6.1e-17`, post `0.0`.
- nudging the lens centre in x by `1e-15` flips `positions_threshold_from()` straight back to the
  old value `0.0019501455607163743`.
- nudging by `1e-6` moves the threshold by a factor of **86**.
- the `positions[1].x` flip is a sign change only: `5.638186222554754e-04` is bit-identical either
  way, and is itself a grid-step artefact.

## Fix

Test-only re-pin. Update the four literals in `test_autolens/analysis/test_result.py`
(`0.0019501455` → `0.0019534291`, `0.0097507278035` → `0.0097671455155`, `positions[1]` x sign) at
the existing `1.0e-4` tolerances, and add a comment above each pin recording that the fixture is
exactly mirror-symmetric, that the branch is decided by sub-ULP tie-breaking, that PyAutoArray#519's
exact identity transform selected the other branch, and that a `1e-15` centre nudge flips it back.
**No library change.**

## Follow-up suggestion

File separately: move the fixture off the symmetry axis (a small x offset on the lens centre, or a
non-zero `ell_comps`) so the pin measures a stable physical quantity rather than a solver
tie-break. As it stands the test will keep re-breaking on any floating-point-level change anywhere
in the transform/deflection chain.
