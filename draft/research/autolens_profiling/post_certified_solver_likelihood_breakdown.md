# Assess remaining likelihood bottlenecks after certified solver integration on CPU and GPUs

Type: research
Target: autolens_profiling
Repos:
- autolens_profiling
Difficulty: large
Autonomy: supervised
Priority: normal
Status: formalised
Consequence: judge
Witness: All nine backend/mesh combinations have measured whole-call and exclusive breakdown records that reconcile within 5% or quantify instrumentation uncertainty; a ranked optimization assessment states measured contribution, correctness constraints and whole-call speedup ceiling for each candidate.
Review-minutes: 20
Unattended: needs-slicing
Blocked-by: PyAutoMind/draft/feature/autoarray/implement_and_optimize_certified_positive_solver.md

## Original request

Now intake a follow up issue which is that once the ceritifed solver is implemented, to look at the likelihood⠂breakdown and work out if optimization of the other⠐parts which are now the bottlenecks is
  possible. This should be⠄done for numba CPU⢀and JAX GPU (A100 and RTX), for rectangular, delaunay and delaunay NN.

## Objective and dependency

After the production certified solver and its dispatch are implemented and validated in the installed stack, use @autolens_profiling to measure where the likelihood spends time and assess feasible optimization of the remaining bottlenecks. This is one bounded assessment task; library implementation is a separate follow-up. Do not substitute the earlier solver monkeypatch or assume that certified solving is selected or fastest on native CPU.

Dependency: PyAutoMind/draft/feature/autoarray/implement_and_optimize_certified_positive_solver.md. Record the merged library revision and actual production-selected solver/configuration for every measurement.

## Required measurements

Cover all nine combinations: Numba CPU, JAX GPU A100, JAX GPU RTX, each with rectangular, Delaunay and DelaunayNN. Confirm each path is available; missing hardware/path is an explicit unfinished measurement gap, never an extrapolated result.

Use matched fixed-lens-light source-only fits, one controlled representative dataset/configuration, fp64 reference, and roughly 1500 source pixels (record actual built and solved counts, particularly rectangular edge removal). Record CPU/BLAS/Numba threads, GPU model, preprocessing provenance and library/configuration revisions. Separate setup/compilation from warmed steady-state execution and report timing variability.

Measure whole-likelihood time and a same-process exclusive decomposition, including the solver so the proposed bottleneck shift is verified. Attribute mesh/mapper construction, ray tracing, PSF/blurring, mapping/data-vector and curvature/regularization assembly, determinants/evidence, and repeated builds, copies, host/device transfers or callbacks where observed. Avoid overlapping terms; reconcile to whole-call time within 5% or quantify unexplained time, synchronization and instrumentation overhead. Kernel times subtracted across different runs are not a definitive breakdown; check that instrumentation has not materially changed GPU fusion/execution.

Reuse the ongoing CPU work's dense/sparse preprocessing provenance and fixed-light subtraction re-bake/parity checks where applicable. Preserve positivity, edge constraints, reconstruction/evidence and backend parity. Fixing light uses precomputed solved intensities; state its preparation cost separately.

## Deliverable and boundaries

Publish machine-readable measurements and a concise per-hardware/per-mesh verdict ranking opportunities by measured contribution, expected whole-call speedup ceiling, implementation cost and correctness tradeoffs. Distinguish demonstrated improvements from plausible hypotheses. Bounded profiling-harness experiments may test feasibility; any proposed source-library change becomes a separately scoped implementation task. Wider source-size, dataset, precision or batching sweeps require evidence-driven follow-ups. No speedup is promised.

Reconcile overlap at planning time with these existing Mind records, reusing useful results/instrumentation without duplicating or silently replacing ongoing work:

- draft/research/autolens_profiling/hst_gpu_non_solver_residue_programme.md: broader HST/A100 optimization campaign, predating production integration.
- draft/research/autolens_profiling/fixed_light_numba_cpu_programme.md: broader CPU campaign.
- complete/2026/09/fixed-light-numba-phase1.md (harness shipped, legs unrun) and complete/2026/09/fixed-light-numba-solver.md: the CPU measurement/decomposition.

Use autolens_profiling/results/notes/fixed_lens_light_{library_path,hardware,source_pixel_scaling,verdict}_2026_09.md as historical context, not fresh production baselines. Formalizes the non-solver bottleneck seed from autolens_profiling#259 in PyAutoMind/ideas.md.

<!-- formalised by the Intake (Conception) Agent on 2026-09-15 from file:tmp/post_certified_likelihood_breakdown_intake.md -->
