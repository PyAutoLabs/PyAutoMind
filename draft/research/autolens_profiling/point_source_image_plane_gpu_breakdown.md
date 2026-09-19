# Point-source A100 speed-up campaign: profile and optimize with the shared breakdown

Type: research
Target: autolens_profiling
Repos:
- autolens_profiling
- PyAutoArray
- PyAutoLens
Themes:
- point-source
- profiling
- jax-gpu
Difficulty: large
Autonomy: supervised
Priority: high
Status: formalised
Consequence: judge
Review-minutes: 30
Unattended: ready
Filed: 2026-09-17
Updated: 2026-09-19

## Campaign contract (2026-09-19)

This execution plan supersedes the earlier deliverable/gate wording retained below.
This is one of two optimization campaigns in a three-task plan. The independent
shared breakdown task is their common prerequisite.
It is a phased campaign: at start-dev, issue only the next bounded phase (one task /
one PR per member), retaining this prompt as the campaign intent until all phases
are resolved. Do not attempt a cross-library, multi-PR campaign as a single task.
Use start-dev and the applicable library/workspace worktree and ship procedures;
obtain implementation-plan approval before source edits. No profiling or library
implementation was performed during this consolidation.

### Measurement and acceptance contract

- Use @autolens_profiling for timing and versioned JSON + PNG evidence, with
  README/dashboard regeneration. Correctness evidence belongs in library tests
  and @autolens_workspace_test, not a timing-only assertion of scientific validity.
- Record exact library/profiling commits, JAX/jaxlib versions, device, precision,
  XLA flags, thread settings, model/data seed, source planes, solver grid/scale,
  precision, neighborhood degree, capacity, warm-up, repetitions and cache state.
  Historical numbers are leads, not comparable current baselines.
- Separate tracing/lowering, compilation, first execution and warmed runtime.
  Synchronize device outputs with block_until_ready; pass varying parameter
  inputs through the production likelihood so constant folding cannot fake work.
  Report repeated/interleaved A/B medians and dispersion on identical hardware,
  both ms/likelihood and batch throughput, plus memory where relevant.
- Retain a fused end-to-end production likelihood control. Prefix timing
  differences can change fusion and contain noise: report residuals/negative
  differences honestly and corroborate with a device trace rather than claiming
  independently timed steps sum to the fused runtime.
- Compare likelihood, image counts/positions, NaN padding/masks, magnification
  filtering and source-redshift handling. Cover perturbed models, doubles/quads,
  near-caustic/critical configurations and cluster multi-source/multiplane cases.
  Preserve custom_jvp, eager/JIT/vmap parity and gradient correctness; distinguish
  nondifferentiable image-topology transitions from failures in smooth regions.
- Each iteration: baseline -> one hypothesis -> bounded prototype -> correctness
  gate -> repeated full-likelihood A/B -> accept/reject -> reprofile and rank the
  remaining bottleneck. State minimum detectable improvement from observed noise;
  keep a change only for a repeatable material gain without correctness or
  unacceptable compile/memory regressions. Record negative results too.
- Stop when remaining cost is explained and no worthwhile measured lever remains,
  or a concrete external blocker prevents the next experiment. Do not promise the
  historical speedup, optimize indefinitely, or weaken correctness to hit a target.

### Split request (verbatim)

break into 3, with the first build the shared likelihood breakdown first, which I guess is CPU or GPU agnostic but maybe not, then PR them into main

### Original consolidation request (verbatim)

We did two reviews or assessments of the point source likelihood function recently one for CPU which was JAX and numba sparse (it concluded numba spaerse not worth it) and one for GPU. We may of made some prompts but I want you to assess all that the review put forward and ultimately end with two mind task or prompts, which could be epics, which will profile them with autolens_profiling and iteratively work on the speed up. One was focused in particular on writing an autolens_profiling likelihood_breakdown script, which it may of wrote or just planned, this would likely be the task before we go into specific CPU or GPU speed up

## GPU campaign: depends on the shared breakdown, then measured A100 optimization

### Evidence audit (2026-09-19)

Fetched @autolens_profiling `origin/main` has the four point-source runtime
scripts but no `scripts/point_source/likelihood_breakdown/` or corresponding
point-source breakdown results. Its cluster breakdown times `solver.solve` as
one block. The September 17 GPU prompt is a proposed investigation, not an A100
bottleneck verdict. Existing historical A100 science/defaults evidence is not a
substitute for this dedicated breakdown. No new A100 performance claim is made.

The CPU sibling preserves reported scratch gains, not landed profiling artifacts.
Its redundant vertex sort is distinct from necessary triangle deduplication;
GPU benefit must be measured rather than extrapolated from CPU ratios.

### Prerequisite — separate shared breakdown task

Task 1 shipped in [autolens_profiling#293](https://github.com/PyAutoLabs/autolens_profiling/pull/293)
and is recorded in `complete/2026/09/point-source-shared-breakdown.md`.
Use its merged instrument, CPU reference results under
`results/breakdown/point_source/` and reproducible baseline revisions; do not
rebuild the harness here.
The harness shares stages/schema across devices, but A100 execution and timing
must be validated here. A CPU run is not proof of GPU correctness or performance.

First validate the harness on A100 and acquire fp64 and separately labelled
mixed-precision reference rows on the preserved unoptimized library commits.
This remains possible if CPU improvements have already landed. Check numerical
agreement against the CPU reference and production likelihood, recording
precision-specific tolerances. Begin GPU optimization only after that baseline.
The CPU campaign does not depend on this campaign finishing or obtaining a GPU slot.
Coordinate changes to the shared solver with the CPU campaign to avoid conflicts.

### Phase 1 — A100 bottleneck map

- Use the profiling repo's actual `hpc/README.md` and sync configuration. This
  repo's `hpc/sync` has no push: update RAL code with git and library checkouts
  through HPCPullPyAuto, verify revisions, submit through its supported driver,
  and ingest pulled results from LOCAL_PULL_ROOT. Do not copy a generic
  science-project push-submit recipe into this task.
- Obtain a fused device timeline following the maintained trace precedent;
  attribute kernels to source operations and distinguish launch/host overhead,
  sorting/gathers, deflections, synchronization and device computation.
- Test vmap batches 1/4/16 then larger only within measured memory headroom;
  include the historical batch-3 control if useful. Use distinct parameter
  inputs; report latency, throughput, peak memory and batch setup costs.
- Separate fp64/mixed-precision, compilation/cold start/warm execution, simple
  and representative cluster single-/multi-source/multiplane configurations.
- Time primal likelihood and the custom_jvp gradient path separately, including
  batched gradients. Confirm finite-difference agreement at smooth parameter
  points before treating gradient throughput as usable.

### Phase 2 — bounded optimization iterations

1. Re-evaluate the CPU redundant-sort removal on A100, sharing the same library
   fix if valid; coordinate ownership rather than implement a competing patch.
2. If traces support launch-bound execution, prioritize vmap and benchmark the
   batch break-even/memory limit. A faster per-item batch is not lower latency
   for a serial caller; publish both and identify which caller can exploit it.
3. If sorts/gathers dominate, target the measured operation and consider the
   static-lattice precompute jointly with CPU; preserve containment and padding.
4. If unrolled refinement drives compile cost, evaluate a JAX loop representation
   only after checking step-shape changes and autodiff constraints. Compare
   compile amortization and steady state; don't assume scan/loop is faster.
5. If the implicit-gradient leg dominates, profile its Jacobian/linear algebra
   before changing it; preserve the implicit derivative contract.
6. If deflections dominate, route a bounded profile-specific library phase
   informed by `scripts/lens/deflections/`; retain CPU regression measurements.

For each lever publish accepted/rejected/deferred reasoning and re-profile after
accepted changes. Initial launch-latency, sort dominance, unrolled-compile and
Jacobian-cost claims remain hypotheses until phase 1 measures them.

### Completion evidence

Reuse the shared harness and its CPU reference; ship A100 baseline/final artifact pairs,
trace-derived bottleneck map, batching/precision/compile/gradient tables, and
`results/notes/point_source_gpu_breakdown_2026_09.md` with phase PRs and commands.
Finish warranted optimization iterations, not just filing another list of
follow-ups. Explicitly record rejected levers and residual bottlenecks. If A100
access is unavailable, the separate shared task and CPU campaign can proceed
but this campaign remains pending; never label CPU timing as A100 evidence.

## Preserved September 17 assessment and provenance

The following is historical context; the campaign contract above governs new work.

# Point-source image-plane chi-squared on the A100: likelihood breakdown, bottleneck map, speed-up levers

User request (verbatim, 2026-09-17): "In autolens_profiling, we have done lots of work
speeding up imaging and interferometer on CCD. Now, I want us to speed up the point_source
image plane chi-squared, with this issue focusing on JAX GPU Speed up, mostly using the A100s
on RAL to perform the profiling. Follow the same strurture as imaging and interferomerter,
produce the likelihood breakdown (which likely will ned to be made for the steps of the point
solver? I'm not sure if we ever made one) and focus on bottlenecks and so on."

Survey (2026-09-17):

- `point_source/` has a `likelihood_runtime/` tier (image_plane, image_plane_solved,
  source_plane, source_plane_solved) but **no `likelihood_breakdown/` tier** and **no A100
  row** — the only numbers are local CPU (image_plane_solved: 39 ms/JIT call, 28 ms under
  vmap, v2026.7.23.1). `cluster/likelihood_breakdown/image_plane.py` is the closest
  precedent but times `solver.solve` as one block; nobody has ever opened the solver loop.
- The JAX solve is `AbstractSolver.steps()`: `n_steps = ceil(log2(scale/precision))` (=8 for
  the 0.2"/0.001" cell) unrolled iterations of ray-trace → `containing_indices` (padded to
  `MAX_CONTAINING_SIZE=15`) → `for_indexes` → `neighborhood()`^degree → `up_sample()`, each
  of the last three calling `remove_duplicates` = `jnp.sort` + `jnp.unique(size=…)`, then
  `_filter_low_magnification`, then the all-pairs permutation log-sum-exp chi-squared,
  wrapped in the padded `custom_jvp` solve (`implicit_diff.py`).
- Hypotheses to test on the A100: (a) the call is launch-latency / host-sync bound (tens of
  tiny sort/unique/gather kernels per step, ~8 steps) rather than FLOP bound, so vmap over
  likelihood evaluations is the first-order lever; (b) sort-based `unique` dominates device
  time; (c) 8× unrolled steps inflate compile time; (d) the implicit-diff gradient leg
  (vmap'd Jacobian) is a separate cost centre for gradient searches.

Deliverable: a `point_source/likelihood_breakdown/image_plane.py` cell that opens the solver
loop (per-step rows + chi-squared row, prefix-walk by successive differences per the imaging
harness), A100 fp64 + mp rows and a local-CPU row in `results/breakdown/point_source/`, a
fused-program device-timeline trace leg (fixed_light_trace.py precedent) attributing GPU
kernels to library source lines, vmap-batch scaling on the A100, a compile-time row, a
gradient leg, README dashboard regen, and a `results/notes/point_source_gpu_breakdown_2026_09.md`
verdict ranking the levers with measured evidence. Library levers (PyAutoArray triangles /
PyAutoLens solver) are filed from the verdict as follow-up prompts, library-first.

Related: `draft/research/autolens_profiling/point_solver_profiling_cells.md` (cluster arc
phase 2 — more point-source cells, not a GPU campaign; do not merge scopes).
