## gnfw-convergence-fast
- issue: https://github.com/PyAutoLabs/PyAutoGalaxy/issues/677
- completed: 2026-10-28
- library-pr: https://github.com/PyAutoLabs/PyAutoGalaxy/pull/678
- epic: lenstwin (follow-up to phases 2–3; not a numbered phase)
- summary: `gNFW.convergence_func` no longer calls `quad` once per radius in a Python loop (merge
  d52d5fa). For 1D NumPy inputs with ≥ max(100, n_nodes) finite positive radii the line-of-sight
  integral I(η) is tabulated on a log-spaced η grid (20 nodes/decade, 0.05-decade padding, quad at
  epsrel 1e-10, epsabs 0) and interpolated by a cubic spline in (log η, log I); the closed-form
  prefactor is unchanged. Table nodes and the per-radius path share a stable integrand
  (`_convergence_integral_from`: y = sin t, breakpoints η, 10η, …), so results do not depend on
  input size. 100k points 12.6 s → 0.02 s; default-settings CircularAperture gNFW mass 29.6 s →
  0.04 s; single-radius calls 2.5× faster. New class constants on `AbstractgNFW`; no public API
  change. Zero/negative/non-finite radii, 2D rows and non-NumPy xp keep the original path.
- tests: test_gnfw.py 20 passed (tabulated vs stable reference ≤ 2e-6 for γ ∈ {0,…,2.5}, η
  1e-5..1e3; per-radius vs tabulated; NaN/0/inf unchanged; elliptical grid). Full suite 1431 passed
  / 7 skipped; no existing expected value moved. CI green on acfc61a (3.12, 3.13, nojax, docs).
- traps: the old naive integrand (1 − √(1 − y²)) is wrong by up to 100% for η < 1e-6 with γ ≤ 1
  (cancellation) — values at typical η (1e-3..10) shift ≤ 1.5e-7 toward the reference. `quad`'s
  default epsabs 1.49e-8 stops after one pass at large η where I ~ 1e-7 (≈1e-5 relative error):
  use epsabs=0. Grid tests comparing with point evaluation need over_sample_size=1.
- notes: Requested by the human 2026-10-28 ("speed up gNFW quickly") after lenstwin phases 2–3 hit
  the slow path. Consequence: judge — merged on the human's /prm (freeze clear). Opus worker
  implementation; first version kept the naive integrand on the small-input path, sent back so
  both paths agree. Heart STALE, environment reasons only.

## Original prompt

# Speed up gNFW convergence: tabulate the line-of-sight integral once per call and interpolate, instead of one `quad` per grid point

Type: feature
Target: autogalaxy
Repos:
- PyAutoGalaxy
Themes:
- performance
Difficulty: small
Autonomy: supervised
Priority: high
Status: formalised
Consequence: judge
Witness: `gNFW` / `gNFWSph` `convergence_2d_from` agrees with the current per-point `quad` result to ≤ 2e-6 relative for inner slopes {0, 0.5, 1, 1.5, 1.99, 2.5} over ξ/r_s from 1e-5 to 1e3; existing gNFW tests pass unchanged; a 100k-point convergence evaluation is ≥ 100× faster than before
Review-minutes: 15
Unattended: never
Epic: lenstwin
Filed: 2026-10-28
Issued: 2026-10-28
Issue: https://github.com/PyAutoLabs/PyAutoGalaxy/issues/677

Requested by the human on 2026-10-28 ("speed up gNFW quickly") after lenstwin phases 2–3 found `gNFW.convergence_func` (`@PyAutoGalaxy/autogalaxy/profiles/mass/dark/gnfw.py:90`) costs ~0.1–2 ms per point: it calls `scipy.integrate.quad` once per radius in a Python loop. Aperture-mass integration (`mass_angular_within_circle_via_grid_from`, `ag.MassBudget`, `al.twins.compare` M(<R)) evaluates the convergence on 10⁴–10⁶ sub-pixels, so a gNFW twin needs coarse settings or takes minutes (traps in `complete/2026/10/lenstwin-p2-mass-budget.md` and the phase-3 record).

## Approach (prototyped 2026-10-28)

The integral I(η; γ) = ∫₀¹ (y+η)^(γ−4) (1−√(1−y²)) dy depends only on η = ξ/r_s for a given inner slope. Per call: evaluate it with `quad` on a log-spaced η table spanning the input radii (≈ 20–40 nodes per decade, a few hundred `quad` calls), fit a cubic spline to log I against log η, and evaluate the spline at every input η, then apply the existing closed-form prefactor unchanged. Prototype: 200k points in 0.05 s versus ~20 s, max relative error ~1e-5 at 20 nodes/decade (tighten to meet the Witness). Keep the per-point `quad` path for tiny inputs (e.g. fewer points than table nodes) so small calls are not slower and stay bit-identical. Handle η = 0 / non-finite radii exactly as today. Keep `epsrel` semantics documented.

Do not change `deflections_yx_2d_from` / potential (MGE) or any other profile. NumPy only (the function already uses scipy, so it is not on the JAX path).

## Tests

Accuracy against the old per-point implementation (kept as a private reference or computed in-test with `quad`) across slopes and η decades; small-input path unchanged; existing `test_autogalaxy/profiles/mass/dark/test_gnfw.py` and dependent tests (`test_mass_budget.py`, `test_mge.py`, `test_abstract.py`, coolest interop) pass unchanged; a timing smoke assertion is not required in CI but report the measured speed-up in the PR.
