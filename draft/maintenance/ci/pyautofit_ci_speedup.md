# CI speed: PyAutoFit's 10-minute PR CI is the floor of a shift merge

Type: maintenance
Target: PyAutoFit
Repos:
- PyAutoFit
Difficulty: medium
Autonomy: supervised
Priority: medium
Status: draft
Filed: 2026-11-19
Epic: autonomous-orchestrators
Phase: 10
Consequence: judge
Lane: any
Unattended: never

## Request (verbatim)

Human, 2026-11-19, in chat: "do all the still open". The epic's M3.7 section: "PR CI is the remaining floor (PyAutoFit 10 minutes): a `/ci_speedup` task."

## Why

Since M3.7b a shift's close-out waits in-turn for PR CI and merges on green. Galaxy's PR CI takes about 4 minutes and PyAutoFit's about 10, so PyAutoFit's CI is now the longest wait between PR-open and merge.

## Shape

Run `/ci_speedup` on PyAutoFit: find the slowest parts of its PR CI (unit tests, legs, setup) on the Heart board, then plan the speed-ups through the dev flow. Never weaken a test to make it faster.

## Survey (2026-11-19, read-only `/ci_speedup`, Heart board 2026-11-19T14:34Z, verdict green)

**The gate.** PyAutoFit `Tests` (`.github/workflows/main.yml`): PR median 555 s, max 1058 s over 26 runs (board `gates` lane). Run 44563924855 on `main` (2026-11-19): `unittest (3.12)` 7 m 48 s, `unittest (3.13)` 7 m 54 s, `unittest-nojax` 5 m 15 s, in parallel. Inside the 3.12 leg pytest itself took 398.8 s for 4310 tests (3.13: 390.3 s; nojax: 241.3 s for 3985), so about 85% of the leg is the test run and about 1.5 minutes is setup.

**The slowest tests (board `tests` lane, slowest leg).** The 7 PyAutoFit entries in the top 25 add up to 85 s:

| s | test |
|---|------|
| 30.7 (3.12; 17.1 on 3.13) | `non_linear/search/mle/test_bfgs_resume.py::test_interrupted_fit_resumes_from_checkpoint[LBFGS]` |
| 14.4 | `graphical/functionality/test_moment_projection.py::test__hierarchical_scatter_moments_match_exact_posterior` |
| 11.0 | `non_linear/search/test_conformance_backend.py::test_backend_runs_in_reduced_test_mode[BlackJAXNUTS…]` |
| 8.0 | `non_linear/search/test_conformance_backend.py::test_backend_runs_in_reduced_test_mode[NSS]` |
| 7.6 | `non_linear/test_scaler.py::test__scaling_cannot_move_the_MAP` |
| 7.1 | `non_linear/search/mcmc/test_blackjax_smc.py::test__cold_run_recovers_the_analytic_log_evidence` |
| 6.2 | `graphical/stochastic/test_regression.py::test_stochastic_linear_regression` |

**What the numbers say.** The long tail of 4300 fast tests, not one slow test, is the cost: the top 7 are 85 of about 400 s. Trimming them alone saves at most about 1.5 minutes.

**Candidate levers, largest first (each to be timed before it ships):**
1. **Run the suite in parallel.** Check whether `main.yml` already uses `pytest-xdist`. If not, `-n auto` on the 4-core GitHub runner is the one lever that can take the legs from about 8 to about 3–4 minutes. First check tests that share files or global state (output paths, `conf` singletons) with `-n 4` locally, and fix any that clash rather than marking them serial without cause.
2. **The 30.7 s LBFGS resume test.** It is twice as slow on 3.12 as on 3.13. Name the split (search iterations versus checkpoint I/O versus JAX compile) and shrink the iterations or the fixture, keeping the resume assertion.
3. **The moment-projection and conformance-backend tests** (14.4, 11.0, 8.0 s). Smaller fixtures and fewer samples under test mode, keeping each assertion.
4. **Leg setup (about 1.5 minutes).** Check pip cache hits and whether the nojax leg reinstalls what it does not need.

Never skip, quarantine or weaken a test to make it faster. This survey makes no change; the work goes through `/start_dev` with this section as the plan's evidence.
