# Cluster-scale gradient-search benchmark (Prodigy vs Nautilus, point-source)

Filed: 2026-07-31 (backfilled from git)
Themes:
- samplers
- cluster
- point-source

> **ABSORBED 2026-07-31 (same day)** into
> `draft/feature/autolens/point_source_defaults_campaign.md` (phase B, cluster tier, on
> RAL A100s). Do not run standalone — kept for the context literals below.

Human-requested follow-up (2026-07-31, #657 wrap-up): once the galaxy-scale point_source
benchmark cells wrap, extend the Nautilus-vs-MultiStartProdigy comparison to a
CLUSTER-scale point-source model in autolens_profiling — the regime the solved variants
target (many sources, big dimensionality win: -2 params/source with PointSolved).

## Scope (autolens_profiling)

- New sweep cells: `nautilus` + `multi_start_prodigy` on a cluster point-source dataset
  (multi-plane tracer, multiple sources; reuse/extend the profiling simulators — the
  workspace `cluster/simulator.py` family CSV conventions are the model source).
- Model: dPIE/Isothermal members + host halo as in the workspace cluster examples;
  sources as `al.ps.PointSolved` + `FitPositionsSourceSolved` (recommended search config)
  with an image-plane-solved arm if runtime permits.
- KNOWN CONSTRAINT: free cosmology cannot cross the solver custom_jvp boundary
  (Tracer aux; see ideas.md follow-up) — pin cosmology, or benchmark source-plane solved
  only (no solver in chain) until the flattening follow-up lands.
- Compare: best logL vs truth-instance logL, per-parameter recovery, wall time,
  evals/steps; same truth-anchored methodology as the 2026-07-31 galaxy-scale runs
  (results/searches/... JSONs).

## Context literals (2026-07-31 galaxy-scale runs, results/searches/)

- image_plane truth logL +7.20: nautilus +9.56 (739.7s) converged; prodigy 64x300 -79.9
  (852.8s) missed the 5mas basin (PairAll -inf underflow plateaus suspected; 256-start
  rerun pending at filing time).
- source_plane truth logL -33788: BOTH found better-than-truth wrong models (nautilus
  -313, prodigy -110 at 8.7x less wall) — scalar-mu^2 free-centre source-plane bias
  displayed; gradients work, likelihood flavour is the problem.
