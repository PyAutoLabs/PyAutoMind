## certified-positive-solver
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/566
- completed: 2026-09-23
- library-pr: https://github.com/PyAutoLabs/PyAutoArray/pull/567 (merged `11b93476b`)
- workspace-pr: https://github.com/PyAutoLabs/autolens_profiling/pull/299 (merged `043518479`)
- pending-release: PyAutoArray@https://github.com/PyAutoLabs/PyAutoArray/pull/567
- summary: |
    Phase A shipped the certified active-set positive solver into PyAutoArray:
    `autoarray/util/jax_active_set.py`; `solver`/`stats` kwargs on
    `reconstruction_positive_only_from`; Settings/config keys
    `positive_only_solver` (default pdip), `certified_pass_budget` (16),
    `certified_fallback`, `certified_tau_rel`;
    `AbstractInversion.positive_only_solver_used`. Dispatch only JAX +
    mapper-only; NumPy untouched. Exact implicit gradient via stop_gradient
    search + autodiffed final solve. autolens_profiling#299 migrated both
    harness injections to the new kwargs (the #566-dependent test skips on a
    pre-#566 library; 795/794 pass vs new/old).
- evidence: 1616 tests (+32); SciPy nnls 2e-16; PDIP 8e-12; fallback
  bit-exact; gradient FD 3e-9; downstream JAX parity identical (Delaunay
  2.3e-14, dispatch proven); GPU tests 24 pass; RTX 734.9 → 566.1 ms via the
  library setting (harness monkeypatch was 618.2). Review CLEAN at 233cfc0d
  (one minor finding fixed: no-jax import guard test moved to its own file).
- merge: both PRs merged 2026-09-23 on the human's typed `/prm` on green
  checks, library first, under the human's Heart-RED development override
  ("i authorize,"); Heart freeze not frozen; Heart remained RED for release
  purposes. Merged ≠ released.
- traps:
  - `lax.while_loop` is not reverse-differentiable — hence the gradient design.
  - `lax.cond` fallback runs both branches under vmap (phase B concern).
  - The profiling CI checks out PyAutoArray MAIN, so a library-dependent
    harness test must skip pre-release.
- follow-ups:
  - Phase B `draft/research/autolens_profiling/certified_solver_production_default.md`
    (default flip + batched policy; blocked on the release that ships #567).
  - Optional `custom_jvp` to reuse the loop's final Cholesky factor (one extra
    factorization per solve today).
  - Pre-existing `multi_dataset/jax_likelihood/delaunay.py` failure filed as
    `draft/bug/autolens_workspace_test/multi_dataset_jax_likelihood_delaunay_wrong_likelihood.md`.
  - fixed_light_trace cell's pin label still says "library PDIP" for route b
    even when the library runs certified (cosmetic, phase B).

## Original prompt

# Implement and optimize certified positive solver with structure-aware CPU and JAX dispatch

Type: feature
Target: PyAutoArray
Repos:
- PyAutoArray
Difficulty: large
Autonomy: supervised
Priority: normal
Status: issued — PyAutoArray#566 (phase A, 2026-09-23, Fable start_dev, routed to start_library); phase B filed as draft/research/autolens_profiling/certified_solver_production_default.md
Epic: certified-positive-solver
Phase: A
Consequence: judge
Witness: Representative mapper-only and MGE-inclusive fits preserve constrained reconstruction/evidence within declared tolerances, including forced fallback and JAX jit/vmap; benchmark records justify every automatically selected solver against its backend's current baseline.
Review-minutes: 20
Unattended: needs-slicing
Filed: 2026-09-15
Issued: 2026-09-23

## Scoped 2026-09-23 (Fable start_dev) — phase A is THIS issue, phase B is filed separately

Phase A (PyAutoArray only, opt-in): a JAX certified active-set positive solver in a new
`autoarray/util/jax_active_set.py` (budgeted `lax.while_loop` that stops at certification; primal +
dual KKT certification; permanent fixed set; `lax.cond` PDIP fallback on an exhausted budget); the
active set is searched under `stop_gradient` and the final masked Cholesky solve is autodiffed, so
the gradient is the exact implicit active-set derivative (tested against finite differences and
PDIP's `custom_vjp`). Wired behind `Settings` / `general.yaml` keys `positive_only_solver`
(`pdip` default | `certified`), `certified_pass_budget` (16), `certified_fallback` (`pdip` | `none`),
`certified_tau_rel` (1e-9); selected only on the JAX backend for mapper-only inversions
(`has(Mapper) and not has(AbstractLinearObjFuncList)`) — MGE-inclusive systems never certified
(fixed_light_probe: 40 passes, cond 4e10) and keep PDIP; the NumPy path is untouched (the NumPy
certified scheme measured 3-7 % slower than fnnls, factor-reuse lost to the memo).

Phase B (autolens_profiling, maybe PyAutoFit): measure the production composition
`jax.jit(jax.vmap(fn))` with PDIP (the never-measured baseline) against the shipped certified solver
with fallback `pdip` and `none`, decide the production default and the batched policy (the
`lax.cond` fallback runs both branches under vmap: 44.6 vs 31.1 ms/lane at B=16 in residue phase 2).
Only phase B may flip the default.

Evidence added since filing: residue phases 1-3 (autolens_profiling#268/#273/#295) — the certified
solve at budget 7 is 10.2 ms of a 31.6 ms A100 call; whole-call 31.7 vs 50.8 ms PDIP; the harness
kernel is `active_set_steps.active_set_masked_jax` (static `lax.scan`, no gradient rule) and
`library_solver_injection.certified_reconstruction_from` (Jacobi scaling + `lax.cond` fallback).

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

Reuse the completed CPU decomposition records PyAutoMind/complete/2026/09/fixed-light-numba-phase1.md and complete/2026/09/fixed-light-numba-solver.md, with the final campaign verdict in complete/2026/09/fixed-lens-light-numba-cpu.md; do not duplicate that evidence or the separate hst_gpu_non_solver_residue_programme.md.

Fixed-light measurements use pre-solved intensities and exclude preparation; they do not prove that freezing one estimate throughout a search preserves every likelihood. Out of scope: new sparse operators, changes to statistical modeling/positivity, and broad profiling campaigns.

<!-- formalised by the Intake (Conception) Agent on 2026-09-15 from file:tmp/certified_positive_solver_intake.md -->
