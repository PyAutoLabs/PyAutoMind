# PyAutoFit mock scaffolding fills every parameter with 1.0, which is now an invalid `ell_comps`

Type: bug
Target: PyAutoFit
Repos:
- PyAutoFit
- autogalaxy_workspace_test
- autolens_workspace_test
Difficulty: medium
Autonomy: supervised
Priority: high
Status: formalised — NOT started. Root cause is narrowed to PyAutoFit's mock
        helpers but the exact call site is **not** pinned; see "What is not yet
        known". Requires an environment that can run the full autogalaxy stack.

## Symptom

Seven aggregator integration scripts across the two `*_workspace_test` repos fail
with the same exception:

    ValueError: ell_comps must satisfy ell_comps[0]**2 + ell_comps[1]**2 < 1;
    got (1.0, 1.0), whose magnitude is np.float64(1.4142135623730951)

Observed in PyAutoHeart Workspace Smoke run 31356506626 (2026-08-10), legs
`autogalaxy_test / misc` and `autolens_test / misc`.

Failing scripts (all `scripts/misc/aggregator/`):

- `autogalaxy_workspace_test`: `ellipse.py`, `fit_imaging.py`,
  `fit_interferometer.py`, `galaxies.py`
- `autolens_workspace_test`: `tracer.py`, `fit_imaging.py`,
  `fit_interferometer.py`

## Why this is a real bug and not a bad shipped value

The guard is correct and correctly placed. `validate_ell_comps` sits on
`EllProfile`, the single base every elliptical profile inherits (`ag.Ellipse`
included), and enforces `f = sqrt(e_y**2 + e_x**2) < 1` because the axis ratio is
`q = (1 - f) / (1 + f)` — at `f >= 1` the ellipse degenerates to `q <= 0` and has
no geometric meaning. `(1.0, 1.0)` gives `f = 1.414`, `q = -0.17`. Nothing should
ever construct a profile with it.

This is **not** the same failure as the sampler-draw legs (`guides`, etc.), which
were fixed by PyAutoGalaxy#568 making `ModelParameterException` a
`FitException` so searches resample. That fix does not help here: the aggregator
rebuilds instances from stored samples outside any likelihood call, so there is no
resample path to take.

## Evidence

1. **The value is a hardcoded fill, not a sampled value.** It prints as plain
   `(1.0, 1.0)` — Python floats. The genuine sampler-draw failures in the same run
   print as `np.float64(-0.7446446619131553)`. Different provenance.

2. **Two places in PyAutoFit hardcode exactly this shape:**
   - `autofit/non_linear/mock/mock_samples.py` — `MockSamples.default_sample_list`
     builds `kwargs={path: 1.0 for path in self.model.paths}`.
   - `autofit/non_linear/mock/mock_samples_summary.py` — `MockSamplesSummary.__init__`
     sets `self._kwargs = {path: 1.0 for path in self.model.paths}`, which backs
     both `max_log_likelihood_sample` and `median_pdf_sample`.

   A blanket `1.0` is a safe placeholder for most parameters and an invalid value
   for any `ell_comps`. `_make_samples` in `mock_search.py` already does the right
   thing (`prior.value_for(0.5)`), so the fix idiom exists in the same package.

3. **All 7 scripts construct `MockSearch` identically and never pass
   `samples_summary`:**

   ```python
   search = ag.m.MockSearch(
       samples=samples,
       result=af.m.MockResult(model=model, samples=samples,
                              samples_summary=samples.summary()),
   )
   ```

   `MockSearch.__init__` therefore falls back to `MockSamplesSummary.default()`.
   Whether that asymmetry (a real model in `MockResult`, a default summary on the
   search) is the trigger or a red herring is the open question.

## Hypothesis already tested and DISPROVEN — do not re-tread

The obvious suspect is the helper copy-pasted into all 7 scripts:

```python
def parameter_list_with_physical_ell_comps(value):
    parameter_list = model.prior_count * [value]
    for index, path_tuple in enumerate(model.all_paths):
        if "ell_comps" in path_tuple[0]:
            parameter_list[index] = 0.1
    return parameter_list
```

It looks broken — `all_paths` returns a tuple of `Path`s per prior and
`Path = Tuple[str, ...]`, so `path_tuple[0]` is a path tuple and `in` is
exact-element membership, which would not match a leaf named `ell_comps_0`.

**It is not broken.** `ell_comps` has a tuple default, so PyAutoFit builds a
`TuplePrior` attribute named `ell_comps`, and the path is
`('ellipses', '0', 'ell_comps', 'ell_comps_0')` — it contains a bare `'ell_comps'`
element, so the check matches. Reproduced by rebuilding `ellipse.py`'s exact model
(two `Ellipse` models with fixed `major_axis`, plus the nested multipole
collection) against installed autofit and running the real helper:

```
[2] ('ellipses', '0', 'ell_comps', 'ell_comps_0')   -> 0.1
[3] ('ellipses', '0', 'ell_comps', 'ell_comps_1')   -> 0.1
ellipses[0].ell_comps = (0.1, 0.1)
```

Index alignment is also fine: `all_paths` and `instance_from_vector`
(`prior_tuples_ordered_by_id`) both order by prior id. **Changing this helper is a
no-op — do not "fix" it.**

## What is not yet known

Which call site actually feeds the all-ones instance to the aggregator. Two
candidates were checked and neither fits cleanly:

- `MockSamplesSummary.default()` uses an empty `Collection()`, so its `_kwargs`
  is `{}`, not a dict of 1.0s.
- `MockSearch._fit_fast` evaluates at `[prior.mean for prior in
  model.priors_ordered_by_id]`, which is `0.0` for `ell_comps` — valid.

So the path runs through serialization into the database and back out through the
aggregator, which is where it needs to be traced.

## Suggested approach

1. Run one failing script (`autogalaxy_workspace_test/scripts/misc/aggregator/ellipse.py`)
   against the full stack with a breakpoint or traceback on the guard, and record
   the actual construction stack. **This needs a real autogalaxy environment** —
   it could not be done from a cloud session (autoarray/jax/numba would not
   install there).
2. Fix at the PyAutoFit mock layer: replace the blanket `{path: 1.0 ...}` with
   prior-median values (`{path: prior.value_for(0.5) for path, prior in
   model.path_priors_tuples}`), matching `_make_samples`.
3. Mind the blast radius: `MockSamples`, `MockSamplesSummary` and `MockSearch`
   have roughly 55 call sites inside PyAutoFit alone, plus the PyAutoGalaxy and
   PyAutoLens suites. Run all three suites, not just PyAutoFit's.
4. Consider whether `MockSearch` should inherit the `samples_summary` from a
   passed-in `result` rather than silently defaulting.

## Notes

- Do not relax or move the `ell_comps` guard. It is correct.
- Do not chase the `workspace-validation-report` artifact from a cloud session
  (blocked at the egress proxy). Per-job logs via the Actions API carry the same
  failures.
- Sibling work already shipped: the one genuinely unphysical shipped literal,
  `ell_comps=(0.5, 0.9)` in HowToGalaxy `tutorial_3_fitting`, was corrected
  separately. An AST scan of 454 `ell_comps` literals across
  autogalaxy_workspace, autolens_workspace, HowToGalaxy, HowToLens and both
  `*_workspace_test` repos found no other violating literal, so this ticket is
  the whole remaining `ell_comps` surface.
- PyAutoHeart#27 is a different family (release-profile timeouts and a JAX
  exception, 2026-07-06); it is not related.
