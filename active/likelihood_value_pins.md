# autocti_workspace_test: pin numerical log-likelihood values for the CTI likelihood functions

Type: test
Target: autocti_workspace_test
Repos:
- autocti_workspace_test
- PyAutoCTI
Themes:
- cti
- testing
Difficulty: small
Autonomy: supervised
Priority: high
Lane: local-dev
Status: formalised
Consequence: glance
Witness: `scripts/dataset_1d/likelihood/pins.py` and `scripts/imaging_ci/likelihood/pins.py` each evaluate `analysis.log_likelihood_function(instance)` on a deterministic simulated dataset at the truth model and at one offset model and `np.testing.assert_allclose` both scalars against literals committed in the script (rtol 1e-8); both scripts are in `smoke_tests.txt` and the per-PR `Smoke Tests` run is green with them
Review-minutes: 5
Unattended: ready
Epic: cti-upkeep
Phase: 0
Filed: 2026-11-04
Issued: 2026-11-04

## Why

The lens and galaxy test workspaces pin absolute log-likelihood literals for every
likelihood function (`scripts/<dataset>/jax_likelihood/*.py`:
`np.testing.assert_allclose(result, 626.2235846074373, ...)`, re-pinned with a
dated comment when a value legitimately moves, e.g. the 2026-09-08 over-sample
ladder). That is what catches a silent numerical change in a library PR
(PyAutoArray#524's six-tuple return, the [4,2,1]→[4,2,2] sweep).
`autocti_workspace_test` has nothing equivalent: `scripts/dataset_1d/model_fit.py`
and `scripts/imaging_ci/model_fit.py` only `print(result.log_likelihood)` after a
Nautilus fit, and the pre-resurrection
`imaging_ci/profiling/likelihood/*.py` scripts print
`analysis.log_likelihood_function(instance)` without asserting. So the CTI
likelihood (arctic clocking → FPR/EPER extraction → chi-squared) can change
value with no test noticing — exactly the gap the arcticpy bump in
`cti-upkeep` phase 2 (Euclid DR2 well-filling model) will walk into. The human
asked (2026-11-04) for these pins early in the epic, before any library or
arcticpy change lands.

## Task

1. Add `scripts/dataset_1d/likelihood/pins.py` and
   `scripts/imaging_ci/likelihood/pins.py` (no JAX leg — clocking is C++;
   NumPy path only, so no `jax_likelihood/` folder name).
2. Each script simulates a small deterministic dataset in-script (mirror the
   `model_fit.py` simulate blocks: `read_noise=None`,
   `add_poisson_noise_to_data=False`, an explicit constant noise map so chi² is
   defined; if read noise is wanted, seed NumPy explicitly first — the
   simulators take no `noise_seed`), builds the `AnalysisDataset1D` /
   `AnalysisImagingCI` with the same `Clocker1D` / `Clocker2D` the simulate
   used, and evaluates `log_likelihood_function` at (a) the truth instance and
   (b) one offset instance (e.g. trap density ×1.2, release timescale ×0.8) so
   the pinned chi² is non-trivial. Cover parallel-only, serial-only and
   parallel+serial for imaging_ci; one and two trap species for dataset_1d.
   Keep each script under ~10 s.
3. Pin every scalar as a literal with `np.testing.assert_allclose(..., rtol=1e-8)`
   and the lens-style provenance comment (`# pinned 2026-11-xx: autocti
   main@<sha>, arcticpy 2.6`). Print the values too, so a re-pin has the new
   numbers in the CI log.
4. Add both scripts to `smoke_tests.txt`; declare the env the way the
   workspace's other scripts do (`ENV:` block if the harness reads one).
5. Document the re-pin rule in `autocti_workspace_test/AGENTS.md`: a pin moves
   only with a dated comment naming the PR and the cause; the arcticpy version
   is part of the pin's provenance because phase 2 is expected to move every
   literal.

## Validation

- Both scripts run green locally with `PYTHONPATH` including PyAutoCTI
  (append, never replace — see memory on the CTI PYTHONPATH trap) and in CI
  through Heart's reusable `Smoke Tests`.
- Control test: perturb the offset instance by 1 % and confirm the assertion
  fails — a pin that cannot fail is decoration.
- `model_fit.py` scripts untouched; `legacy/` untouched.
