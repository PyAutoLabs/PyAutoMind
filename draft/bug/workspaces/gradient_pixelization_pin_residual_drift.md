# jax_profiling/gradient/imaging/pixelization.py: 3.2% of its pin move is unattributed

Type: bug
Target: workspaces
Repos:
- @autolens_workspace_developer
- @PyAutoArray
Themes:
- pixelization
- profiling
- jax-gradient
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: draft
Consequence: judge
Review-minutes: 20
Unattended: ready
Filed: 2026-08-26

## What happened

Regenerating the adaptive-rectangular pins after PyAutoArray#490 (mirrored
bilinear row weights + round-off-dependent cell assignment in the shared
adaptive rectangular mapper) turned up one fiducial whose pin does **not**
reproduce even before that fix.

`@autolens_workspace_developer/jax_profiling/gradient/imaging/pixelization.py`
(HST, 28x28 `RectangularBilinearAdaptDensity`, Sersic + Isothermal lens,
`Constant` regularization) asserted `EXPECTED_LOG_EVIDENCE_HST =
-66270.78281169113`, pinned 2026-04-24 (`cfa5378`). Measured 2026-08-26 on
library `main`s, both legs on one host differing only in the #490 commit:

```
72fb01d1^ (pre-fix)   -84633.30874141103    18362  (27.7%) below the pin
72fb01d1  (fixed)     -64156.79838547805     2114   (3.2%) above the pin
```

#490 accounts for +20476 of that. The residual **3.2% is older drift and is
not attributed**. The pin was re-pointed to the measured post-#490 value in the
same change (with the provenance recorded in the file); this prompt owns
explaining the 3.2%.

## Why it is worth a look rather than a shrug

- The input side is ruled out. `jax_profiling/dataset/imaging/hst` is a pure
  rename at `f8a5cef` (`R100`, identical blobs), and the script's model, mask,
  over-sampling and mesh shape are byte-identical to the pinning commit — only
  the path strings changed. The move is entirely library-side.
- It is **not** the mesh-name trap. `RectangularRTUAdaptDensity` at the same
  fiducial gives `-86488.3491981348` pre-fix, further from the pin, not closer,
  so the 2026-08-21 relabel to `Bilinear` (`08d5d86`) was right.
- The sibling `jax_profiling/jit/imaging/pixelization.py` (MGE lens, 35x35, same
  mesh family, same dataset directory) still reproduces its own 2026-05-11 pin
  **bit-for-bit** pre-#490 — measured in the same session. So whatever moved the
  gradient fiducial left the shared adaptive-mesh path alone, and points at
  something specific to Sersic + Isothermal + `Constant` reg, or at a change
  between 2026-04-24 and 2026-05-11.

## Scope

1. Bisect the eager `figure_of_merit` for this fiducial from 2026-04-24 to now.
   Build the old checkouts and measure — do not attribute from commit messages
   (the trap recorded in `complete/2026/08/pixelization-eager-jit-divergence.md`).
   A `git worktree add <scratch> <sha>^ --detach` plus a PYTHONPATH substitution
   of the one repo is minutes per step, and decisive.
2. Decide what the answer means: a deliberate improvement nobody re-pinned, or a
   silent regression in the Sersic / Isothermal / `Constant` path that a stale
   pin has been hiding since April.
3. If it is a regression, that is the bug — fix it and re-measure the pin again.
   If it is deliberate, record the attribution in the file's provenance comment
   next to the #490 rows already there.

## Notes

- Related but distinct: `draft/bug/workspaces/jax_likelihood_pins_stale_by_1e4.md`
  covers `autolens_workspace_test`'s marginal (~1.2e-4) pin drift. This one is
  3.2% on a developer-workspace fiducial.
- The #490 regeneration itself is done and attributable — every other pin
  touched in that pass reproduced its pre-fix value first
  (`autolens_profiling` imaging cells to 1.3e-6, the developer jit cell
  bit-for-bit, its RTU variant to 3.6e-10).
