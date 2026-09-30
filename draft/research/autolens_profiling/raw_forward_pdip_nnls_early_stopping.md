# Raw-forward PDIP NNLS early stopping: a dedicated autolens_profiling study, then the PyAutoArray fix

Type: research
Target: autolens_profiling
Repos:
- autolens_profiling
- PyAutoArray
- euclid_strong_lens_modeling_pipeline
Themes:
- nnls
- jax
- profiling
- correctness
Difficulty: too-large
Autonomy: supervised
Priority: high
Status: formalised
Filed: 2026-09-30
Consequence: glance
Witness: on PyAutoArray main with no config override, `tests/test_compute_latent_variable.py::test_latent_euclid_variables_traces_under_jax_jit` in euclid_strong_lens_modeling_pipeline passes (jit total_source_flux within rel 1e-3 of eager 3.31988), the 48 #571 SLaM source_lp[1] points still converge, and lens/autolens_profiling/wiki carries a campaign page + index row recording the benchmark and the chosen solver.
Review-minutes: 3
Unattended: needs-slicing

Human intent, verbatim (2026-09-30): "i agree that euclid A needs a plan, I would be tempted to make this a dedicated part of autolens_profiling with a wiki and whatnot".

A released-default solver silently biases amplitude-derived latents by ~6 % while the
likelihood barely moves. This prompt makes the diagnosis a **dedicated autolens_profiling
study** (its own campaign page in the profiling wiki), and the PyAutoArray fix follows from
the study's verdict. Planning happens in a later `start_dev` session; this prompt sets it up.

## Symptom

- `euclid_strong_lens_modeling_pipeline` main has been red since run 36153011006 (2026-09-25,
  merge a89a468). The pipeline tree is identical to the last green commit 485eb9a, so the cause
  is upstream.
- Failing test: `tests/test_compute_latent_variable.py::test_latent_euclid_variables_traces_under_jax_jit`
  (line 847). The latent `total_source_flux` traces to **3.51109 under `jax.jit`** vs
  **3.31988 eager NumPy** (rel tol 1e-3).
- It also blocks euclid PR #107 (hook propagation).

## Cause (read-only investigation, 2026-09-30)

- PyAutoArray #572 (merge 3de624b5, 2026-09-24, "raw-forward PDIP for mapper-less
  positive-only JAX solves", issue #571) made `nnls_preconditioning_no_mapper: raw` the default
  for mapper-less (MGE-only) JAX inversions.
- Bisect: passes with PyAutoArray at 7fa8d271 (pre-#572); fails at origin/main; passes at main
  with `nnls_preconditioning_no_mapper: jacobi`.
- Captured euclid system: n = 60 MGE columns, curvature condition number 5.6e11, max|q| 8.5e6.
  - **raw PDIP**: reports "converged" in 24 iterations; objective gap vs fnnls 4.7e-6;
    amplitude gap **4.3 %**; its own KKT residual 2.4e-5 against a data-scaled tolerance of
    ~1.1e-9. It stops on the objective, not on the solution.
  - **jacobi PDIP**: 19 iterations; objective gap 4.7e-10; amplitude gap 1.8e-4.
- Meaning: Δχ² ~1e-5, so logL-only checks cannot see it, but amplitude-derived latents shift
  ~6 %. This affects **production JAX vis_lp latents** such as `total_source_flux`, not only the
  test.

## Constraint

#571's reason for switching to raw must stay fixed: jacobi PDIP diverged on 14/48 SLaM
source_lp[1] near-truth points. Any candidate that reintroduces that divergence is rejected.
Related capture: `scripts/imaging/hazards/mge_nnls_capture.py` in autolens_profiling (the 48
near-truth vectors) and the sibling prompt
`draft/research/autoarray/mge_nnls_fix_pyautoarray_571_slam_60.md` (timing/parity of #571; this
study is about solution accuracy — coordinate, do not duplicate).

## Candidate fixes to evaluate

1. Tighten the raw tolerance, or change the convergence criterion to be KKT / solution-based
   rather than objective-based.
2. Jacobi-space polish iterations warm-started from the raw solution.
3. Other preconditioning (to be proposed in planning).

Code: `autoarray/util/jax_nnls.py` (`solve_nnls_primal_raw_forward`, `data_scaled_solver_tol`),
`inversion_util.py` (the `preconditioning == "raw"` branch).

## Rejected (do not revisit without new evidence)

- Loosening `JIT_VS_EAGER_REL` in the euclid test: hides a real 6 % error.
- A pipeline config stopgap setting `jacobi`: reintroduces #571.

## Deliverables

1. **Benchmark set** of mapper-less systems in autolens_profiling: the 48 #571 SLaM
   source_lp[1] points, the captured euclid system, plus a spread of conditioning.
2. **Measurements per candidate solver**: solution accuracy against fnnls (amplitude relative
   error, derived latents such as total_source_flux, KKT residual — not only logL / objective),
   convergence / divergence rate, iteration count and cost (CPU and GPU, single and vmap), fp64.
3. **Ledger + wiki**: a `results/notes/` ledger and a new campaign page in
   `lens/autolens_profiling/wiki/campaigns/` built from `_template.md` with the ten header labels,
   plus a row in `wiki/index.md` (check that repo's AGENTS.md and `wiki/README.md`;
   `scripts/misc/tooling/check_wiki.py --check` must pass). Write a pre-registered decision rule
   before the deciding run.
4. **PyAutoArray fix** driven by the verdict (a follow-on phase or prompt, library-first), then
   re-verify the euclid pipeline on library main. PyAutoArray owns the solver;
   euclid_strong_lens_modeling_pipeline owns the witness test.

## Success

- The euclid test passes on PyAutoArray main with no config override.
- #571's 48 cases still converge.
- The wiki records the findings, the rule and the chosen solver.

<!-- formalised by the Intake (Conception) Agent on 2026-09-30 from file:../raw_forward_pdip_early_stop.md -->
