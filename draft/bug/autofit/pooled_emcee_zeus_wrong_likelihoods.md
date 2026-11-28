# Pooled Emcee and Zeus return wrong likelihoods, and Emcee leaves its worker pool running

Type: bug
Target: PyAutoFit
Repos:
- PyAutoFit
Difficulty: medium
Autonomy: supervised
Priority: medium
Status: formalised
Consequence: judge
Filed: 2026-11-26

## Finding

Reproduced on 2026-11-26 with `af.ex.Gaussian` + `af.ex.Analysis`, `nwalkers=12`, `nsteps=20`, and a fresh output folder for every run:
- Emcee with `number_of_cores=1` gives a log likelihood of about -810 to -860 and exits normally.
- Emcee with `number_of_cores=2` gives `log_likelihood = inf`, and then the process hangs at exit (90s timeout). `multiprocessing.util._exit_function` joins SneakyPool workers (`autofit/non_linear/parallel/sneaky.py`) that are blocked in `queue.get`, so the pool is never closed.
- The released 2026.11.25.1 behaves the same, so this predates R6.
- Zeus with `number_of_cores=2` exits normally but lands far from the 1-core answer (-91 vs -1.5). On CI 3.13 its conformance tests failed with "Number of contractions exceeded maximum limit" under `"auto"`.

PyAutoFit#1802 sets the Emcee and Zeus defaults back to 1 core, so only an explicit core count above 1 reaches this path.

Recovery for a quick repro: a runner script lives in the Opus 5.5 health session's scratchpad (`emcee_diag/run.py`), but it may be gone. It is a short script calling `af.Emcee(nwalkers=12, nsteps=20, number_of_cores=N)` on `af.ex.Gaussian`.

## Ask

Find why SneakyPool fitness values come back wrong (`inf` for Emcee) and why the pool is not closed after the fit; check Zeus's `ctx.pool()` path too. Close the pool deterministically, and add a PyAutoFit test that runs Emcee and Zeus with `number_of_cores=2` to completion, compares the result with 1 core, and checks the process exits. Then decide whether `"auto"` can become their default again.
