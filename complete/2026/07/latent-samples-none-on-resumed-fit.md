# latent-samples-none-on-resumed-fit

- shipped: 2026-07-25 (the same day the prompt recorded the finding)
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1418 (merged) — "fix: raise SamplesException from latent computation when samples is None (resumed fits)"
- repos:
  - PyAutoFit

## Summary

The prompt was filed from the 2026-07-25 full health sweep and fixed upstream the
same day. Nothing in PyAutoMind recorded it, so the prompt sat in `draft/` for two
weeks looking like open work.

Recorded 2026-08-09 by the draft/ sweep. No work is owed.

## Verified against PyAutoFit main (`3b960609`), 2026-08-09

The prompt's § Task offers two options — (a) reload persisted samples on the
resume path, or (b) raise a clear guarded error. **Option (b) is what landed**,
and its § Acceptance is met exactly: "either computes latent samples or fails with
an intentional, documented message — never an `AttributeError` from inside
`latent_samples_from`."

`autofit/non_linear/analysis/latent.py` now opens `latent_samples_from` with an
explicit `if samples is None:` guard raising `exc.SamplesException`, and the
message names the cause and both remedies — samples output disabled via
`output.yaml`'s `samples: false` or `general.yaml`'s `samples_to_csv: false`, so
`result.samples` comes back `None` on the reload; enable samples output and re-run
from cleared output, or pass a `Samples` object explicitly. It also states why
`samples_summary.json` is not a substitute (latents are per-posterior-sample).

The function's `Raises` docstring carries the same diagnosis the prompt reached
independently — that a completed fit short-circuits to
`NonLinearSearch.result_via_completed_fit`, which reloads from `samples.csv`.

The prompt's open sub-question ("May be test-mode-specific — check whether a real
non-bypass resumed fit also returns samples=None") was answered by the fix taking
the general path: the guard is unconditional, not gated on `PYAUTO_TEST_MODE`.

## Why it was missed

This is the one class of drift the Mind cannot see by itself. Unlike the
PyAutoArray k×s finding, there is **no completion record for #1418 anywhere in
`complete/`** — the fix went in upstream without a Mind entry, so no amount of
cross-referencing draft prompts against the ledger would surface it. Only reading
the prompt's acceptance criteria against the upstream tree finds this shape.

## Original prompt
# compute_latent_samples crashes on a resumed completed fit (samples is None)

Type: bug
Target: autofit
Repos:
- @PyAutoFit
Difficulty: medium
Autonomy: supervised
Priority: low
Status: draft

## Finding (2026-07-25 full health sweep)

Running `autolens_workspace_test` `misc/latent/latent_variables_smoke.py` (and
`latent_nan_robustness.py`) twice in the same output tree fails on the second
run: the search resumes ("Fit Already Completed: skipping non-linear search"),
`result.samples` comes back `None` on the resume path (PYAUTO_TEST_MODE=2
bypass), and

    autofit/non_linear/analysis/latent.py:113  latent_samples_from
    -> samples.model  ->  AttributeError: 'NoneType' object has no attribute 'model'

A fresh run (output cleared) passes. So the latent pipeline works, but the
resume/load path hands `compute_latent_samples` a `None` samples object
instead of the persisted samples (or a clear error).

## Task

Determine whether the resume path should (a) reload persisted samples so
latent computation works on resumed results, or (b) raise a clear, guarded
error from `compute_latent_samples` when samples are unavailable. May be
test-mode-specific — check whether a real (non-bypass) resumed fit also
returns samples=None.

## Acceptance

Second invocation of the latent smoke scripts in an existing output tree
either computes latent samples or fails with an intentional, documented
message — never an AttributeError from inside latent_samples_from.
