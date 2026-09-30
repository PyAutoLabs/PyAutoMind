## raw-pdip-forward-polish
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/594
- completed: 2026-09-30
- library-pr: https://github.com/PyAutoLabs/PyAutoArray/pull/595 (merge 7a89e19a0, head 42c52358)
- workspace-pr: https://github.com/PyAutoLabs/autolens_profiling/pull/357 (merge 4652580b2, head ad365df)
- pending-release: PyAutoArray@https://github.com/PyAutoLabs/PyAutoArray/pull/595
- epic: linear-solver-programme (phase 2)
- summary: |
    Phase 2 of epic linear-solver-programme. PyAutoArray#595: the raw-forward PDIP solver
    (`nnls_preconditioning_no_mapper: raw`, #572) now returns the #573/#574 polished iterate
    (<= 10 tight warm-started Jacobi-system PDIP iterations) as its forward value, via
    `_raw_forward_polished()` shared by the custom_vjp primal and forward, so jit / grad / eager
    agree; backward unchanged. `RAW_POLISH_MAX_ITER` added (old name aliased); docstrings and
    config wording updated. New fixture `mge_solver_reference_systems.npz` (8 #571 systems +
    euclid vis_lp, fnnls x_ref) and `test_nnls_raw_forward_amplitude.py` (107 cases; 12 red on
    base bd03e09e — euclid inactive/total flux 0.115, source flux k1/k2/k3/k5 1.6e-3..6.4e-3;
    green after). End-to-end jit-vs-eager relaxed to rtol 1e-9 after the 3.12 Actions leg showed
    5.4e-11 runner-dependent XLA reassociation.
    autolens_profiling#357: `euclid_latent.py` validation re-based to the post-fix jit
    3.320127604; all 6 solver cells re-run against PyAutoArray 7a89e19a0 (provenance recorded;
    artefacts overwrote the v2026.8.17.1 stamp in place, pre-fix at 3ad68af); ledger Phase 2
    section, campaign page + index, README regen.
- results: |
    Corpus 81/81 converged incl. 48/48 SLaM; fixed pdip_raw == phase-1 pdip_raw_polish on 81/81.
    Worst inactive-column flux 0.115 -> 3.31e-4; source-flux misses 53/81 -> 1/81 (euclid proxy
    only); euclid total_source_flux jit-vs-eager +5.76e-2 -> +7.47e-5; euclid pipeline latent
    test 19/19 on library main with no override. autolens_workspace_test: 7 mapper-less/MGE
    scripts pass, no pin moved (mge_group JIT now equals NumPy to 6e-12).
- rule-verdict: |
    Not admissible under the phase-1 pre-registered rule as written — criteria 2-4 fail on
    recorded rule weaknesses: euclid source-column proxy 4.96e-2 vs actual latent 7.5e-5;
    flat-direction system sig 0.219 shared by all accurate candidates; 5/52 KKT ratios at the
    3e-16 floor. Shipped on the direct flux/latent evidence above.
- gates: |
    PyAutoArray pytest 1890 + CI 3 legs green; autolens_profiling ruff / 5 checks / pytest 984 /
    9 smokes + lint green. Both PRs shipped under the Heart RED development override (recorded on
    the issue, the PRs, active.md and autonomy_log); merged by human /prm on green checks. Heart
    RED for release throughout (release validation FAILED stage integrate; later also a
    PyAutoGalaxy CI failure — unrelated).
- next: |
    Phase 3 = draft/research/autoarray/mge_nnls_fix_pyautoarray_571_slam_60.md (GPU/A100 timing
    + parity rows). PyAutoArray#595 awaits a release (pending-release above; cleared only by
    /review_release).

## Original prompt

# Linear-solver programme phase 2: fix the raw-forward PDIP amplitude bias in PyAutoArray

Type: bug
Target: PyAutoArray
Repos:
- PyAutoArray
- euclid_strong_lens_modeling_pipeline
- autolens_profiling
Difficulty: medium
Autonomy: supervised
Priority: high
Status: formalised
Filed: 2026-09-30
Issued: 2026-09-30
Witness: a PyAutoArray regression test loads the phase-1 corpus npz (copied from autolens_profiling `results/lens/solver/corpus/` as a fixture beside `test_autoarray/inversion/inversion/files/mge_slam_nnls_systems.npz`) and asserts, per system, converged AND amplitude agreement with fnnls (amp_rel_max ≤ 1e-3, source flux_rel ≤ 1e-4) — an amplitude assertion, not logL — red on unfixed main; plus euclid `tests/test_compute_latent_variable.py::test_latent_euclid_variables_traces_under_jax_jit` passes on library main with no config override.
Review-minutes: 3
Consequence: glance
Unattended: needs-slicing

Epic `linear-solver-programme`, phase 2. Contract: `complete/2026/09/linear-solver-accuracy-study.md` (phase-1 record with the original programme prompt folded in; the phase-1 verdict blocker is satisfied — autolens_profiling#355 merged 2026-09-30).

## Symptom

Raw PDIP (PyAutoArray#572, `nnls_preconditioning_no_mapper: raw`, the released mapper-less
default) stops on the objective (gap 4.7e-6 vs fnnls) with amplitudes 4.3 % off fnnls, so
euclid `total_source_flux` traces to 3.511 under `jax.jit` vs 3.320 eager. The euclid latent
test has been red since 2026-09-25. logL cannot see it (Δχ² ~1e-5); amplitude latents shift ~6 %.

## Fix

Candidate: phase 1 verdict (autolens_profiling#355, `complete/2026/09/linear-solver-accuracy-study.md`): **no candidate passes the pre-registered rule** — raw PDIP reports converged on 81/81 (KKT ~3e-14) yet leaves 11.5 % of the reference amplitude on euclid columns inactive in the reference (total_source_flux +5.76 %); jacobi diverges on 29/81. Post-hoc, each of these turns the euclid latent test green: forward polish (+7.5e-5), tol 1e-5 (+5.1e-4), jaxnnls tol with cap > 50 (-3e-8); caps ≤ 16 are unsafe. The binding constraint is the stopping test, not the iteration budget. Choose among these on the post-hoc evidence and gate on inactive-column flux, not logL/KKT.

Implement exactly the candidate the phase-1 pre-registered rule admits (converged 100 %, 48/48
SLaM incl.; worst amp_rel_max ≤ 1e-3; worst source flux_rel ≤ 1e-4; KKT ≤ 10× pdip_jacobi's;
lowest median iterations). The three plausible shapes:

1. A tighter data-scaled tolerance constant in `data_scaled_solver_tol`
   (`autoarray/util/jax_nnls.py`).
2. Return the PyAutoArray#573 polished iterate (≤ 10 warm-started Jacobi iterations) as the
   forward value in `_raw_forward_backward_point` / `_solve_nnls_raw_forward_with`. The
   custom_vjp forward must return the same value the primal (`solve_nnls_primal_raw_forward`)
   returns, or jit/grad and eager diverge — polish both or neither.
3. A KKT / solution-based stop instead of the objective-gap stop.

Also touch the `inversion_util.py` raw branch if the candidate needs it, and update the
`nnls_preconditioning_no_mapper` comment in `general.yaml` to describe the new behaviour.

## Constraint

The 48/48 SLaM source_lp[1] points must stay converged (#571); the existing
`mge_slam_nnls_systems.npz` test must stay green.

## Rejected

- Loosening `JIT_VS_EAGER_REL` in the euclid test.
- A pipeline config stopgap to `jacobi` (reintroduces #571).

## Downstream

- workspace_test mapper-less likelihood pins: re-pin if the forward value moves.
- autolens_profiling: re-run `scripts/lens/solver/accuracy.py` post-fix and append the row to
  `results/notes/linear_solver_accuracy_2026_09.md` (+ campaign page
  `wiki/campaigns/linear_solver_accuracy.md`).

## Ownership and order

PyAutoArray owns the solver; euclid_strong_lens_modeling_pipeline owns the witness test (no edit
expected there); autolens_profiling is the corpus fixture source. Library-first: ship PyAutoArray,
then re-verify the euclid test on library main.
