# Update the multi_plane guide's Richardson-step warning once the adaptive Hessian ships

Type: docs
Target: autolens_workspace
Repos:
- autolens_workspace
Themes:
- notebooks
Difficulty: small
Autonomy: supervised
Priority: normal
Status: formalised
Blocked-by: a PyAutoGalaxy release carrying PR#593 reaching the installed stack (workspace follows the released library, not main)
Filed: 2026-08-29

`scripts/guides/advanced/multi_plane.py` § `__A Warning: The NumPy Hessian Step Is Too Coarse Near A
Compact Deflector__` (added in autolens_workspace#517, ~line 1217) prints the defect **live**: it
evaluates `LensCalc.from_tracer(...).magnification_2d_via_hessian_from` on the PyAutoLens#480
fixture, shows `[-0.00694, -0.00221, 0.00139, 0.00246]` against the autodiff / ray-traced
`[0.04508, 0.01099, -0.08602, -0.01118]`, and says the defect is filed and *not fixed*.

PyAutoGalaxy#591 / PR#593 (merged 2026-08-29) fixed it: `_hessian_via_richardson` now adapts its
step per point (successive-Richardson gate, `rtol=1e-7`, roundoff-floor stop, one loud warning
for genuinely singular points). Once that reaches a released PyAutoGalaxy, the guide's printout
will show agreement (~3e-4 vs the reference) and the prose will be wrong.

## What to change

- Rewrite the section as "what used to fail, and how the adaptive step handles it": keep the
  live evaluation (it now demonstrates the fix), quote the old wrong numbers as history, explain
  the two termination rules and the `UserWarning` contract (only genuinely singular points warn),
  and drop the "not fixed" sentence and the bug-prompt pointer (point at PyAutoGalaxy#593 instead).
- Keep the section short; the oracles above it already carry the comparison.
- Regenerate `notebooks/guides/advanced/multi_plane.ipynb`; run the guide through the runner.

## Why gated

Workspace scripts run against the released libraries in users' installs; the guide must not
describe behaviour its readers cannot yet see. Un-gate when PyAutoHeart's release run for the
version carrying #593 is published (see `complete/2026/08/lenscalc-adaptive-hessian-step.md`
).
