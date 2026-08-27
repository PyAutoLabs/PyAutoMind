# `@PyAutoFit` Bug: a rejected best point kills the run at results-write and loses samples.csv

Type: bug
Target: autofit
Difficulty: small
Autonomy: supervised
Priority: high
Status: formalised
Issued: 2026-08-27

Original request (verbatim): "Look at the JAX profiling gradinet epic, download results
overnight from A100, and do a major assessment of the results so far are, maybe double
checking some conclusiojns." → audit → "yep do all that" (ranked action 1).

## Problem

Six of seven finished Phase 8B MultiStartProdigy arms on the RAL A100 (autolens_profiling
jobs 341874/341875, 1.8–4.0 h each) completed 3000/3000 steps and then died inside
`analysis.save_results` with

    autofit.exc.SamplesException: The stored parameters returned by max_log_likelihood
    cannot be reconstructed as a model instance because the current model rejected them
    ← autogalaxy.exc.ModelParameterException: ell_comps must satisfy e0**2+e1**2 < 1

The best lane sits outside the ellipticity unit disk (the `ell_comps` prior is an
independent TruncatedGaussian(-1,1) box; `validate_ell_comps` is a no-op on JAX tracers,
so the jitted objective is finite there). The rejection only surfaces on host
materialisation, and then:

1. `@PyAutoFit/autofit/non_linear/result.py:116-121` `Result.instance` goes through
   `SamplesSummary.max_log_likelihood` (`samples/summary.py:58` → `samples/interface.py:122`,
   raising policy). The summary holds ONE sample so it cannot "next_valid"; the recovery
   added by #1486 lives only on `Samples.max_log_likelihood` (`samples/samples.py:378-413`)
   and never applies to the path that runs. (This is the open #1487 suspect.)
2. `@PyAutoFit/autofit/non_linear/search/updater.py:211-224` catches the exception and
   returns early — `save_samples_summary` and `save_samples` are SKIPPED, so the run has
   no `samples.csv`, no `.completed`, and the only surviving artifact is
   `search_internal.dill` (which the crash coincidentally spares from deletion).
3. `@PyAutoLens/autolens/analysis/analysis/dataset.py:186-191` `save_results` catches
   only `AttributeError`, so the exception escapes `start_resume_fit`
   (`abstract_search.py:777`) before `paths.completed()` at `:781`.

## Fix (library-first; this prompt covers PyAutoFit + the PyAutoLens catch)

- `Result.instance`: try the summary; on `SamplesException` fall back to
  `self.samples.max_log_likelihood()` (the recovering path). Log at WARNING.
- `updater._save_samples`: persist `samples` (and a summary marked invalid / without
  instance) BEFORE instance materialisation, so a rejected best point never costs the
  run its data. This also removes the early return that #1487 identifies as the reason
  the weight-threshold prune never runs.
- PyAutoLens `save_results` / `save_results_combined`: also catch
  `af.exc.SamplesException` (belt-and-braces; never let a tracer/plot failure kill a fit).
- Tests: a model whose stored best vector is rejected by `instance_from_vector` →
  `Result.instance` returns the best VALID sample; `samples.csv` is written; no raise.
- Do NOT make `validate_ell_comps` fire on tracers. The physics gap (joint disk
  constraint / reparameterisation) is a separate Phase-3 follow-up prompt.

After merge: `HPCPullPyAuto` on RAL so the ~22 pending 8B arms write normally.
Audit: https://claude.ai/code/artifact/d9f4b0f3-52a1-4830-a9ad-11a225b77507
