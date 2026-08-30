# The reconstruction noise map is not the truncated posterior the NNLS solve implies

Type: bug
Target: autoarray
Repos:
- @PyAutoArray
Themes:
- pixelization
Difficulty: medium
Autonomy: human-required
Priority: low
Status: draft
Consequence: judge
Review-minutes: 20
Unattended: never
Filed: 2026-08-28

- Status: split out of reconstruction-noise-map-solver-mismatch at close-out 2026-08-28 — Defects 2/3 and docs shipped (PyAutoArray#472/#473/#493), recorded in complete/2026/08/reconstruction-noise-map-solver-mismatch.md; this is what remains.

## Step 1 (gating) — re-measure the evidence-optimal lambda with the lens mass FREE

Everything below is conditional on this measurement, so do it first and stop if it comes back flat.

The `low` grade rests on one result: at the fitted `lambda* = 10` the shipped (full-matrix) noise map
and the active-set-conditional one differ by only **1.007–1.263 median**, and source flux through the
`S/N >= 5` cut moves 0.0% / −1.3% / 0.0%. But **the lens mass was fixed at truth** in that fit. A free
mass model that cannot absorb residuals may prefer a *lower* lambda — and at lambda ~ 0.1–1 the gap
opens to **1.7–2.8× median, up to 10× per pixel**, with flux shifts of −11% to −49%.

- Rebuild the harness from `autolens_workspace/scripts/imaging/features/pixelization/source_science.py`.
  The original scripts (`scratchpad/fitted_lambda.py`, `real_fit_measure.py`, `sensitivity.py`) were
  session artefacts and no longer exist.
- Sample lambda jointly with a free mass model rather than maximising log evidence on a grid — grid
  maximisation was the previous shortcut and it cannot see posterior mass at lower lambda.
- Report where lambda lands and the shipped/conditional ratio there. Also worth covering: Delaunay
  (only `RectangularBilinearAdaptDensity` was ever measured) and more than one noise realization.

## Step 2 (only if step 1 shows a material effect) — the truncated-Gaussian posterior

`reconstruction_noise_map` reports `sqrt(diag([F + lambda*H]^-1))`, the covariance of the
*unconstrained* Warren & Dye solve, while the default `use_positive_only_solver: true` runs NNLS —
whose posterior is a Gaussian truncated to `s >= 0`.

**Read this before designing anything: the two available maps bracket the truth.**

- full-matrix (shipped) ignores `s >= 0` → **overstates** (upper bound);
- active-set-conditional treats the active set as known → **understates** (lower bound);
- the true truncated posterior lies between.

So swapping to the conditional covariance is **not** the fix at any lambda. The work is to compute
the truncated posterior properly, or to widen the documented bracket. PyAutoArray#472 already
documents the bracket, so doing nothing remains an acceptable outcome.

## Verification

- Step 1's numbers, with error bars — enough realizations to state whether the free-mass lambda
  differs from `lambda* = 10` at all.
- Any implementation must be checked against both bounds on a compact source (`r_eff = 0.05`, where
  the shipped map overstates by ~26% median) and land between them; a result outside the bracket is
  a bug in the estimator, not a finding.
- Pinned pixels (`reconstruction == 0`) have a boundary-spike marginal, not a Gaussian. Whatever the
  noise map reports there must be stated in the docstring, not implied.
- No change to `reconstruction`; this is the noise map only.
