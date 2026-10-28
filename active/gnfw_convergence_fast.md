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
