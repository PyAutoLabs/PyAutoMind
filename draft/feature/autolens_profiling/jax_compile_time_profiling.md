# Profile and speed up JAX likelihood-function compile times (all use cases)

Type: feature
Target: autolens_profiling
Repos:
- @autolens_profiling
Difficulty: large
Autonomy: supervised
Priority: high
Status: formalised

`autolens_profiling` measures **run time** (per-eval cost, VRAM, wall time) but
not **compile time**. For JAX likelihoods, XLA compilation is now a first-class
cost in its own right — sometimes dominating a whole run — and nothing in the
repo profiles it or defends against regressions in it.

Build the code setup in `autolens_profiling` to **profile JAX likelihood-function
compile times across all use cases** (the existing cell grid: imaging /
interferometer / point_source / datacube × mge / pixelization / delaunay ×
instrument × fp64/mp × CPU/GPU/A100), and then **reduce them**.

## Motivating example (a particularly slow one, measured 2026-07-15)

A pixelized multi-start gradient MAP fit on an **A100 80GB**, float64:

- model: SLaM-pix-1 shape — MGE linear lens light (geometry fixed), free
  Isothermal + ExternalShear, source `RectangularKernelAdaptDensity(shape=(30,30),
  bandwidth=0.1)`, `over_sample_size_pixelization=1`, **no** sparse operator;
  8 free non-linear parameters, 15361 image pixels.
- search: `af.MultiStartAdam(n_starts=16, n_steps=300, batch_size=4)` — the
  batched `value_and_grad` is tiled by `jax.lax.map(..., batch_size=)`
  (PyAutoFit#1373/#1374).
- **XLA spends >30 minutes compiling a single fusion** (`input_reduce_fusion`),
  repeatedly, at several points in the run.
- The *same* fusion took **7m36s** in the simpler FD probe
  (`jax.value_and_grad` of the same likelihood, no `lax.map`), so the
  scan-of-vmap structure appears to make it dramatically worse.
- **Latent variables cost 453 s for a SINGLE sample** (`Time to compute latent
  variables: 453.35 seconds for 1 samples`), compile-dominated — the same
  `input_reduce_fusion` recompiles in the latent path
  (`LATENT_BATCH_MODE='jit'`, per-sample jit).
- Total: a 300-step, 16-start fit took **~35 min wall, almost entirely compile**.

## MEASURED: autotuning is NOT the cause (tested 2026-07-15 — do not re-chase)

The unbatched attempt reported `Autotuning failed for HLO ... All configs failed
during profiling`, which made XLA autotuning the obvious suspect. **It was
tested and ruled out.** Two otherwise-identical A100 runs:

| | autotune ON (330377) | `--xla_gpu_autotune_level=0` (330378) |
|---|---|---|
| wall_s | 2100.1 | 2090.1 |
| max logL | -39887.864 | -39887.864 |
| einstein_radius | 1.4169 | 1.4169 |

**Identical to the decimal — autotuning made no measurable difference.** (The
autotuned job *appeared* slower only because it was additionally paying for a
`print_vram_use` compile, and was observed mid-flight.) The autotune-failure
message is a symptom of the 58 GiB allocation, not the cause of slow compiles.

## Leads worth investigating (not yet tested)
- **Persistent compilation cache** (`jax_compilation_cache_dir`) — the phase-3
  benchmark already used one; make it standard so repeat cells pay compile once.
- **`XLA_FLAGS=--xla_dump_to=`** — dump the HLO for the pathological fusion and
  find what is being fused (the shape was
  `f64[16, 15361, 2, 31, 512]` unbatched = 58 GiB, which also OOM'd).
- fp64 vs mp: f64 doubles buffers and may change autotune behaviour.
- Whether `lax.map`'s scan-of-vmap is inherently worse for XLA here than a
  plain `vmap`, and whether `remat` / a different tiling helps.

## Scope

1. A compile-time **profiling** capability alongside the existing run-time
   profiling (report compile seconds per cell; the artifacts/README dashboard
   pattern already exists), so slow compiles are visible and regressions are
   caught.
2. Then **reduce** compile times using the leads above, with before/after
   numbers per cell.

Note the sibling knob: `analysis.print_vram_use(model, batch_size=...)` itself
triggers a full vmapped compile, so it is not a cheap diagnostic on heavy cells
— its docstring's "20-30 seconds" is an MGE-scale claim.

<!-- intaken 2026-07-15 from the pixelized multi-start A100 runs (autolens_workspace_developer#100). Fable to do the work. -->
