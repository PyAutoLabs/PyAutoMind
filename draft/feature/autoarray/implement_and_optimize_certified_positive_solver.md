# Implement and optimize certified positive solver with structure-aware CPU and JAX dispatch

Type: feature
Target: PyAutoArray
Repos:
- PyAutoArray
Difficulty: large
Autonomy: supervised
Priority: normal
Status: formalised
Consequence: judge
Witness: Representative mapper-only and MGE-inclusive fits preserve constrained reconstruction/evidence within declared tolerances, including forced fallback and JAX jit/vmap; benchmark records justify every automatically selected solver against its backend's current baseline.
Review-minutes: 20
Unattended: needs-slicing

## Original request

Ok, first intake an issue which is to implement the cerified solve in the source code, have a final stab at speeding it up and optimizing it, and also doing this for CPU. That is, I guess the method should ask if the system it is solving is a Mapper only (e.g. sparse struture) or has dense MGE like structures, and thus chooses the solver which is most efficient for the task. Is it true that the cerified solver works less well than the original code when MGE is included?

## Scope

Promote the experimental certified active-set positive solver from the profiling harness into @PyAutoArray, with a bounded final optimization pass on CPU and JAX/GPU. One production-library task and one PR; other repositories below are evidence and validation dependencies only.

Choose the efficient supported solver using backend and actual inversion composition: mapper-only versus systems containing linear-light/MGE coefficients. Use existing inversion metadata (linear_obj_list / has(cls)) before the numeric utility, without lens-profile imports into PyAutoArray. Mapper-only does not imply sparse assembled matrices: the cited benchmarks are dense. Preserve existing sparse paths/fallback unless explicitly supported.

Preserve positivity, fixed/edge-zero constraints, API/return behavior, NumPy fingerprint/memo warm starts, and existing backend/differentiation contracts. Certify primal and dual/KKT conditions, including inactive coefficients with invalid negative dual values. Fall back to the existing robust solver on non-certification, exhausted budgets or numerical failure. Fit settings/override and solver observability into existing APIs.

Use conservative bounded budgets: measured HST 7 Delaunay / 11 rectangular are empirical, not universal; Euclid rectangular already reaches 11 in a fiducial case. Ensure correct, efficient jit/vmap operation: lax.cond inside vmap can execute both solvers, so provide an explicit batching strategy and measure its actual cost, including failed cases.

Make a finite profiling-guided optimization pass. For native CPU, compare against production NumPy/SciPy fnnls separately from JAX-CPU versus PDIP. The existing NumPy certified prototype did not reliably beat fnnls: retain fnnls or keep the new CPU route opt-in unless measurements justify automatic selection. Likewise retain the existing MGE-inclusive solver until matched evidence supports changing it. No speedup is promised on every backend.

## Acceptance

Reuse existing fixtures for a finite representative subset: mapper-only rectangular/Delaunay and MGE-inclusive systems, good/poor fits, small/large source sizes (around 500/1500/2500/4000 where useful), available CPU/GPU, fp64 reference. Record solve-only and whole-likelihood times separately, fallback frequency/cost, correctness tolerances and dispatch decisions. Automatically selected routes must preserve constrained reconstruction/evidence and avoid material runtime regression against their production baseline; unproven cases retain the baseline.

Cover positivity/KKT, forced fallback, edge/failure cases and existing derivative contracts. Run appropriate source tests and downstream JAX jit/vmap parity in autogalaxy_workspace_test/autolens_workspace_test; PyAutoArray's own suite is NumPy-only. Document configuration, backend/composition rules, measurements and limitations.

## Evidence and boundaries

Formalizes the production-solver seed in PyAutoMind/ideas.md from autolens_profiling#259. In autolens_profiling:

- results/notes/fixed_lens_light_source_only_2026_09.md
- results/notes/fixed_lens_light_library_path_2026_09.md
- results/notes/fixed_lens_light_hardware_2026_09.md
- results/notes/fixed_lens_light_low_likelihood_draws_2026_09.md
- results/notes/fixed_lens_light_source_pixel_scaling_2026_09.md
- results/notes/fixed_lens_light_verdict_2026_09.md
- results/misc/fixed_light_probe/{delaunay_1500,rectangular_1521}.{md,json}

Joint 60-MGE+Delaunay1500 free_all failed certification after 40 passes (41 factorizations), while free_one certified at 32; PDIP converged in 22 iterations. Joint rectangular1521 variants failed after 40; PDIP took 21. Source-only free_all took 2 Delaunay / 7 rectangular passes. These demonstrate poorer convergence with MGE, not a matched joint-GPU timing comparison.

Reuse the separate active CPU decomposition task PyAutoMind/complete/2026/09/fixed-light-numba-phase1.md (and its phase-2 successor active/fixed_light_numba_phase2_source_only_solver.md) and its draft fixed_light_numba_cpu_programme.md; do not duplicate that campaign or the hst_gpu_non_solver_residue_programme.md.

Fixed-light measurements use pre-solved intensities and exclude preparation; they do not prove that freezing one estimate throughout a search preserves every likelihood. Out of scope: new sparse operators, changes to statistical modeling/positivity, and broad profiling campaigns.

<!-- formalised by the Intake (Conception) Agent on 2026-09-15 from file:tmp/certified_positive_solver_intake.md -->
