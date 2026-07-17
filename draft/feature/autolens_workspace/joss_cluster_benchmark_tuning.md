# Tune cluster-scale JOSS benchmarks toward their 5-minute targets

Type: feature
Target: autolens_workspace
Repos:
- autolens_jax_joss
- autolens_workspace
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: formalised

Follow-up to the jax-joss-benchmarks epic (autolens_workspace#281). First official
A100 rows for the cluster-scale benchmarks landed far above the paper's
five-minute targets:

- `cluster` (A2744, 7 multi-plane sources): 442 min total — **90 min JAX compile**,
  261 min sampling (271k evals), logL -5089.
- `strong_and_weak` (A2744 + shear catalogue): 515 min — 97 min compile, 319 min
  sampling (231k evals).

Levers, in expected order of impact:

1. **Persistent JAX compilation cache** — the jax-compile-time-research task
   (autolens_profiling#71) measured warm-repeat compile ~6x faster on the A100
   with a persistent cache dir; the ~90-min factor-graph fusion compile is the
   same pathology. Wire `JAX_COMPILATION_CACHE_DIR` into the benchmark harness
   and report cold vs warm compile as separate columns.
2. **Point-solver cost** — `pixel_scale_precision=0.001` on a 120x120 1"/px grid
   over 7 sources x 8 planes; profile the refinement depth and relax to what the
   0.5" positional noise actually requires.
3. **Sampler budget** — n_live=150 over 22 params drove 271k evals; check
   convergence diagnostics for early-termination headroom (n_live 100, higher
   n_batch).
4. Consider whether the paper's cluster claim should quote the warm-cache number
   (justified: any real analysis re-fits the same graph many times).

Also revisit the `imaging` benchmark's search row once the Nautilus comparison
lands (cold-start multi-start Adam missed the pixelized basin, logL -3e7 —
the open search question from autolens_workspace_developer#100).
