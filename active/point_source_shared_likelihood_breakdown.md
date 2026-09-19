# Point source shared likelihood breakdown

Type: feature
Target: autolens_profiling
Repos:
- autolens_profiling
Themes:
- point-source
- profiling
Difficulty: large
Autonomy: supervised
Priority: high
Status: formalised
Consequence: judge
Review-minutes: 20
Unattended: ready
Filed: 2026-09-19

## Objective and ownership

Build the shared point-source likelihood breakdown in @autolens_profiling before
CPU or GPU speed-up work. This is task 1 of a three-task plan. Tasks 2 and 3 are:

- `draft/research/autolens_profiling/pointsolver_image_plane_chi_squared_cpu_speed.md`
- `draft/research/autolens_profiling/point_source_image_plane_gpu_breakdown.md`

This task owns instrumentation and the unoptimized reference baseline, not solver
optimization. Both campaigns consume this instrument; neither builds another copy.
Use start-dev -> start-workspace -> ship-workspace for this bounded workspace PR.
If production-library instrumentation changes prove necessary, scope and approve
that dependency explicitly rather than bundling an optimization into this task.

## User request (verbatim)

break into 3, with the first build the shared likelihood breakdown first, which I guess is CPU or GPU agnostic but maybe not, then PR them into main

## Device boundary

The algorithmic stages, configurations, CLI and result schema are shared. Timing
is device-specific: select the JAX backend at process startup, synchronize outputs,
and record actual hardware, precision and execution settings for every row. Never
combine CPU and GPU measurements as one baseline. Keep backend-specific timing or
trace adapters explicit and reusable rather than forking the solver decomposition.

CPU fp64 is the required reference run for this task. Provide the documented A100
invocation and preserve exact baseline revisions/configuration for reproduction.
Run an available GPU smoke if feasible and report its outcome; if no GPU is
available, state GPU execution is unvalidated. Full A100 validation, mixed-precision
comparisons, kernel traces, memory and batch sweeps belong to task 3. GPU absence
does not block shipping this shared harness or beginning task 2; task 3 must
validate it on A100 before drawing optimization conclusions.

## Breakdown surface

Own and ship `scripts/point_source/likelihood_breakdown/image_plane.py`, or a
clearly documented solved sibling, matching the existing profiling harness.
Include the exact `image_plane_solved` fit class/configuration used by the CPU
assessment and a separately identified plain image-plane control. Reuse existing
simulators and cluster configurations; pass each source's plane_redshift explicitly.

Open the solver loop: initial lattice/vertex-index construction, each refinement
step's ray tracing, containment, selection, neighborhood, deduplication and
up-sampling, followed by magnification filtering, analytic source-centre work
where applicable and pairing/chi-squared. Report step shapes/capacity and actual
vertex counts so padding, geometry and deflection work can be distinguished.
Use prefix-walk timing where valid with fused controls and optional trace hooks; preserve
production semantics rather than replacing the solver with a simplified benchmark.

## Measurement contract

- Use @autolens_profiling for timing and versioned JSON + PNG evidence, with
  README/dashboard regeneration. Correctness evidence belongs in library tests
  and the downstream regression workspace, not timing-only assertions of validity.
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

The iteration and stopping rules above apply to the downstream campaigns; this
task stops at validated instrumentation and its baseline, without optimizing code.

## Acceptance and handoff

- Commit CPU fp64 JSON + PNG under `results/breakdown/point_source/` for the
  fiducial solved and separately labelled plain control, with repeated warmed
  timings, compile/first-call timings, fused controls and numerical agreement.
  Exercise the existing representative cluster configuration without expanding
  the separate cluster runtime catalogue.
- Verify each prefix computes the intended intermediates; retain meaningful
  outputs so dead-code elimination cannot erase the timed stage. Report fusion
  residuals honestly. GPU kernel attribution remains task 3's trace work.
- Preserve the existing production solver behavior, source-plane selection,
  padding and likelihood pins. Validate eager/JIT/vmap agreement and a smooth
  gradient control where supported, reporting unsupported cases explicitly.
- Integrate the existing smoke convention and result/README generation. Run
  repository-required lint, formatting, smoke and dashboard idempotence checks.
- Document reproducible commands, result schema, profiling/library commit IDs,
  environment and known limitations in a shared breakdown note. Preserve the
  original baseline revision even if CPU changes land before the A100 slot.
- Link the merged instrumentation PR and CPU baseline from both dependent
  prompts. Those links open the CPU implementation gate; GPU optimization also
  requires its own untouched A100 reference run on the preserved baseline.

## Scope boundary and provenance

The September 19 survey found no point-source breakdown on fetched profiling
main; the existing cluster breakdown times the solver as one block. Original
September 17 assessments remain verbatim in the two campaign prompts.
`draft/research/autolens_profiling/point_solver_profiling_cells.md` separately owns
quasar/flux and cluster runtime catalogue expansion. Reuse its landed work where
available; do not duplicate it or make it a prerequisite for this instrument.

<!-- formalised by the Intake (Conception) Agent on 2026-09-19 from file:tmp/point_source_shared_likelihood_breakdown.md -->
