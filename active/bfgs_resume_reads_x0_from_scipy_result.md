# `@PyAutoFit` BFGS/LBFGS resume reads `["x0"]` from the saved scipy result and cannot resume an interrupted run

Issued: 2026-10-25
Type: bug
Target: autofit
Repos:
- PyAutoFit
Difficulty: low
Autonomy: safe
Priority: normal
Status: active
Consequence: glance
Witness: an Emcee-style interrupt/resume test for BFGS and LBFGS (run with a small `maxiter`, kill after the first checkpoint, re-run the same `search.fit`) completes without `KeyError` and reaches the same optimum as an uninterrupted run; a resume with `total_iterations >= maxiter` leaves `search_internal` populated so `Samples` build.
Filed: 2026-10-14

Found by the A5 library worker (PyAutoFit#1689–#1692) and verified identical on main df6d218f1, so it is not an A5 regression and was deliberately left unchanged there. `autofit/non_linear/search/optimize/bfgs/search.py` resumes by reading `["x0"]` from its dill-saved scipy `OptimizeResult`, which has no such key, so every resume of an interrupted BFGS/LBFGS run raises `KeyError: 'x0'`. Separately, when the saved `total_iterations` already meets `maxiter`, the resume path skips the optimiser and never sets `search_internal`, so samples cannot be built. Fix on top of the A5 `run(ctx)` version of the search (after #1692 merges); keep Zeus/BFGS's own dill save/resume (A5 decision 2) rather than introducing `resume_state`.
