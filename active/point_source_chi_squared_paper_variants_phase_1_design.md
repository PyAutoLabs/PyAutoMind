# Point-source chi-squared variants (arXiv:2406.15280) — Phase 1: design

Parent: `point_source_chi_squared_paper_variants.md` (verbatim request there).
Phase 1 of 5. Judgment-heavy — stays with the lead (Opus) session per
`PyAutoBrain/skills/WORKFLOW.md`; no source edits in this phase.

## Goal

Produce the approved design for centre-free point-source likelihoods:
which variants from Lombardi 2024 (arXiv:2406.15280, Gravity.jl) we
implement, and the exact API. Output = design writeup on the GitHub issue
+ any corrections to the phase 2–5 prompts.

## Grounding (verified 2026-07-27)

- Model classes: `PyAutoGalaxy/autogalaxy/profiles/point_sources.py` has only
  `Point(centre)` and `PointFlux(centre, flux)` — centre is always a free
  (y,x). No centre-free class exists anywhere.
- Centre plumbing is a single funnel:
  `PyAutoLens/autolens/point/fit/abstract.py:144-153`
  `source_plane_coordinate → self.profile.centre`. Every fit uses it.
- Fit classes (`autolens/point/fit/positions/`): `FitPositionsImagePair`
  (Hungarian, numpy-only, not jittable), `FitPositionsImagePairAll`
  (all-to-all LogSumExp mixture, from this paper, JAX-blessed),
  `FitPositionsImagePairRepeat` (nearest-with-repeats + unmatched-model
  policies, JAX-shaped, `AnalysisPoint` default), `FitPositionsSource`
  (source-plane, scalar µ² noise weighting).
- `fit_positions_cls` is the only pluggable hook (`fit/dataset.py:34` default
  `FitPositionsImagePair`; `model/analysis.py:42` default
  `FitPositionsImagePairRepeat` — note the defaults DIFFER).
- FALSE DOCSTRINGS: a "barycenter of ray-traced positions" option is claimed
  but not implemented in `fit/positions/abstract.py:48`,
  `image/abstract.py:49`, `image/pair.py:30`, `image/pair_all.py:26`,
  `image/pair_repeat.py:18`, and the workspace guide
  `autolens_workspace/scripts/cluster/likelihood_function.py:312-318`
  (claims `FitPositionsSource(profile=None)` uses a centroid — it actually
  raises `PointExtractionException`). Phase 2 must make the docstrings true
  or delete them; phase 4 fixes the guide.
- JAX blockers on the source-plane path (relevant to any new source-plane
  variant): `Grid2DIrregular.grid_2d_via_deflection_grid_from`
  (`PyAutoArray/autoarray/structures/grids/irregular_2d.py:170`) takes no
  `xp`; `FitPositionsSource` missing from pytree registration
  (`model/analysis.py:181-218`). `distances_to_coordinate_from` (:204) is
  already `_xp`-threaded.

## Paper taxonomy to design against

- Image-plane (Eqs. 29–38): direct association / best-match / marginalize
  over all pairings (LogSumExp — our `PairAll`). Baseline forms keep the
  source position β as a free non-linear parameter.
- Source-plane linearized (Eqs. ~41–48): linearize the lens equation around
  each observed image; β enters linearly and is solved analytically as a
  precision-weighted (full local Jacobian / inverse-magnification-tensor
  weighted) mean of back-traced positions. This is BOTH the centre-free
  source-plane chi-squared AND the better-errors variant (tensor weighting
  vs our scalar µ²).
- Centre-free image-plane: profile the analytic β* (from weighted
  back-projection) into the image-plane chi-squareds — forward-solve model
  images from β* instead of a sampled `profile.centre`, for the pair-repeat
  and all-to-all schemes.

## Decisions to make (the actual design work)

1. Variant set: (a) source-plane analytic-centre with tensor weighting;
   (b) source-plane analytic-centre with current scalar µ² weighting (for
   continuity/comparison)? (c) centre-free `PairRepeat`; (d) centre-free
   `PairAll`; (e) is a centre-free Hungarian `Pair` worth it given it is
   numpy-only? Recommend which becomes the documented default for cluster
   fits (Lenstool parity uses `FitPositionsSource`).
2. API: removing the (y,x) priors REQUIRES a parameter-free `al.ps` model
   class (priors derive from `__init__`) — `fit_positions_cls` alone cannot
   do it. Decide: one new class (e.g. `al.ps.PointSolved`, name TBD) +
   orthogonal centre-resolution on the fit side, vs new fit subclasses per
   scheme (the guide's existing class-attribute pattern, cf.
   `unmatched_model_policy`), vs both. Decide the semantics of
   `source_plane_coordinate` when the centre is solved (keep the single
   funnel; no silent None-guards — absence of a centre must be explicit).
3. Name-pairing: dataset `name` → profile pairing must keep working for the
   new class (`fit/abstract.py:84-90`).
4. JAX plan: the analytic β* (weighted mean) is fixed-shape and xp-friendly;
   decide whether phase 2 also fixes the two `FitPositionsSource` jit
   blockers above (recommended — new source-plane variants sit on the same
   primitives). Any `PyAutoArray` change makes this a 3-repo task
   (autoarray + autogalaxy + autolens); the FeatureDecision's
   "repos: autolens" is understated — record the override.
5. Error-fidelity check design: how phase 2 unit tests demonstrate (numpy
   only, no JAX in unit tests) that solved-centre likelihoods match the
   free-centre likelihood profiled over centre, and that tensor weighting
   reproduces image-plane errors better than scalar µ² on a known asymmetric
   configuration.
6. Fluxes — IN SCOPE, alternative to the current implementation. Paper
   (Eq. 39 + §6.1): magnitude-space Gaussian with lensing modulus
   `LMᵢ = 2.5 log10|Aᵢ⁻¹|`; intrinsic magnitude M enters linearly →
   analytically marginalized/profiled (conjugate prior), removing M as a
   free parameter. PyAutoLens is magnification-first flux-space:
   `FitFluxes.model_data = |µᵢ| × profile.flux` (`fit/fluxes.py:110-124`)
   with `flux` a free param on `PointFlux`. Decide the port: flux-space
   analytic profiling (linear least squares,
   `F* = Σ µᵢ f̂ᵢ/σᵢ² / Σ µᵢ²/σᵢ²` — natural fit to our flux-space noise
   maps and outputs) vs paper-exact magnitude space; and what the model
   class looks like (flux-free `PointFlux` sibling composing with the
   solved-centre class). NOTE: there is no `fit_flux_cls` hook —
   `FitFluxes`/`FitTimeDelays` are hard-wired in `fit/dataset.py:114,130`;
   the design must add pluggable hooks (mirroring `fit_positions_cls`) or
   an equivalent mechanism.
7. Time delays — IN SCOPE, alternative to current. Paper (Eqs. 24-25):
   `tᵢ = T + Tᵢ` with reference time T entering linearly → analytic
   marginalization, same structure as M. Current `FitTimeDelays` takes
   residuals relative to the MINIMUM delay (`fit/times_delays.py:109-110`)
   — an ad-hoc T elimination. Design the precision-weighted analytic T
   alternative and compare error behaviour vs min-subtraction.
8. Missing-image penalty — scope against what exists. The paper's
   mechanism is purely combinatorial: marginalizing over pairings with
   normalization `1/|Σ|` (with repetition `|Σ| = P^I`; without repetition
   `|Σ| = P!/(P−I)!`) penalizes many-predicted/few-observed configurations;
   no explicit detection-probability term. `FitPositionsImagePairAll`
   ALREADY implements `-log(n_permutations)` (`pair_all.py:151-154`, cited
   to this paper). Verify it matches `P^I` exactly; decide whether to add
   the without-repetition variant; decide whether the paper-principled
   penalty should be offered as an `unmatched_model_policy` alternative to
   `PairRepeat`'s ad-hoc `no_image_residual = 1e4` floor and
   noise-normalized "penalize" policy (`pair_repeat.py:93-95, 215-219`).
9. JAX-gradient groundwork for phase 5 (design only, no implementation):
   confirm which variants get analytic/custom-JVP treatment vs plain
   autodiff — see the phase 5 prompt for the paper's gradient formulas.

## Consults

- `autolens_assistant/wiki/core/concepts/point_source.md` (read; background
  current as of 2026-07-09) and `skills/al_point_source.md`.
- PyAutoMemory `methods` wiki (likelihood/jax) per FeatureDecision.
- Paper full text: https://arxiv.org/html/2406.15280 §§2, 5 (and 6.1 for the
  deferred marginalization option).

## Exit criteria

Design posted to the issue; user approves variant set + API; phase 2–4
prompts updated to match. No code changes.
