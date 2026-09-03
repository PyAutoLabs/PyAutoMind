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
