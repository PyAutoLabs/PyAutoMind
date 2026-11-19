## positions-threshold-fixture-off-axis
- issue: https://github.com/PyAutoLabs/PyAutoLens/issues/860 (closed, completed)
- completed: 2026-11-14
- library-pr: https://github.com/PyAutoLabs/PyAutoLens/pull/861 (MERGED d9a22748b)
- shipped: a **test-only** change to `test__positions_threshold_from` in
  `test_autolens/analysis/test_result.py`. The lens centre moved from `(0.1, 0.0)` (on the x = 0 axis)
  to `(0.06, 0.08)`, off every grid symmetry line (x = 0, y = 0, y = ±x). The two thresholds were
  re-pinned once: `0.0009898320 → 0.0012770598` and, for `factor=5`, `0.0049491599 → 0.0063852988`.
  The tolerance stays at 1e-4, and the knife-edge comment is replaced.
- witness (re-run by the independent close-out session at head de90200d9): the deflection at the source
  position is (−0.6, −0.8) for the new centre and (−1, 0) for the old one, which has an exact 0.0
  component. ±1e-6 nudges in x and y leave both images identical, at (±0.599609375, ±0.799494806358),
  and move the thresholds by at most 2.51e-8 relative. Control: a 1e-6 x-nudge of the old fixture
  flips the branch and moves the threshold 98%. `test_result.py` passes 23/23. The author reports
  `test_autolens`: 1021 passed, 1 xfailed.
- not in scope: `test__positions_likelihood_from__mass_centre_radial_distance_min` uses the same
  on-axis tracer and keeps its own knife-edge position pins. It can follow up as a separate prompt.
- gate: CI GREEN (ci-verdict, 3 success, 1 skipped non-test leg "Refresh the Heart feed"); Heart
  scoped dev-ship green for PyAutoLens; Heart freeze clear; review (independent close-out) found no
  changed default, error message, weakened test, rename or wrong docs claim.
- session: unattended glance close-out, shift 2026-11-14-pm2 (claude-opus-5-5). The PR carries the
  `pending-release` label; the `active.md` row held no `pending-release:` line, so none was carried at close-out (added 2026-11-19 by the release session).
- affected-repos: PyAutoLens

## Original prompt

# Move the positions_threshold test fixture off the symmetry axis

Type: bug
Target: autolens
Repos:
- PyAutoLens
Themes:
- testing
Difficulty: small
Autonomy: safe
Priority: normal
Status: draft
Consequence: glance
Witness: The `positions_threshold` fixture in `test_autolens/analysis/test_result.py` sits off the lens symmetry axis (on-axis deflection no longer exactly 0.0), the two pins are re-pinned once against it, and a 1e-6 nudge of the fixture changes neither the solved branch nor the pinned thresholds beyond 1e-6 relative.
Review-minutes: 3
Verified: 2026-11-14 2deeab94 (PyAutoLens)
Lane: any
Filed: 2026-09-03

## Symptom

The two `positions_threshold` pins in `test_autolens/analysis/test_result.py`
sit on a solver tie-break: the fixture lies on the lens symmetry axis, so the
on-axis deflection is exactly `0.0` and which branch the position solver takes
is decided by floating-point noise. PyAutoArray#519 made the grid transform an
exact identity at angle 0, the noise vanished, the branch flipped, and the pins
had to be re-pinned (`complete/2026/09/positions-threshold-repin.md`).

Measured knife edge: a **1e-15** x-nudge flips the branch back; a **1e-6** nudge
moves the threshold by **×86**.

## Fix

Nudge the fixture off the symmetry axis so the solved position is unambiguous,
and re-pin once against the off-axis geometry. The pin then measures the
threshold rather than the tie-break, and the next exactness improvement upstream
stops breaking it.
