# PyAutoFit `MockResult` fills every parameter with 1.0, which is an invalid `ell_comps`

Type: bug
Target: PyAutoFit
Repos:
- PyAutoFit
Difficulty: small
Autonomy: supervised
Priority: medium
Status: **implemented and pushed** (2026-08-13), awaiting PRs.
        Branch `claude/autofit-mock-ones-parameters-bug-sv303m` in **PyAutoFit**
        (fix + 4 regression tests) and **PyAutoGalaxy** (`MockResult` signature).
        The originally-reported symptom was already gone before this work — it was
        fixed in the workspace repos on 2026-08-10, hours after the Heart run that
        reported it. This ticket fixed the underlying library defect.

## TL;DR — what changed since this prompt was first filed

1. **The 7 failing scripts all pass now.** They were fixed in the workspace repos
   (`autogalaxy_workspace_test` #104 and `autolens_workspace_test` #256, both
   committed 2026-08-10 18:54 -0400) — after Heart run 31356506626 sampled them.
   This ticket was filed against stale evidence.
2. **The library defect those commits worked around is still on `main`**, and is
   the real content of this ticket.
3. **Reproduction is no longer blocked.** The prompt previously said the full
   autogalaxy stack "could not be installed from a cloud session". It can — see
   "How to reproduce" below. Everything in this document was produced that way.
4. Three claims in the original prompt were wrong; they are corrected below so
   nobody re-treads them.

## Root cause (reproduced, not inferred)

`af.m.MockResult.__init__` falls back to building its own summary when the caller
does not pass one:

```python
# autofit/non_linear/mock/mock_result.py
super().__init__(
    samples_summary=samples_summary or MockSamplesSummary(model=model or ModelMapper()),
    ...
)
```

and `MockSamplesSummary.__init__` fills every parameter with a blanket `1.0`:

```python
# autofit/non_linear/mock/mock_samples_summary.py:26
self._kwargs = {path: 1.0 for path in self.model.paths} if self.model else {}
```

That dict backs both `max_log_likelihood_sample` and `median_pdf_sample`. So any
`MockResult` constructed with a real `model` but no `samples_summary` carries an
all-ones instance — and `1.0` is an invalid `ell_comps` for every elliptical
profile.

**The consumer is `Result.instance`, and the crash happens inside `search.fit()` —
not in the aggregator.** Verified traceback (pre-fix `ellipse.py`, libraries at
`main`):

```
ellipse.py:53                    search.fit(model=model, analysis=analysis)
abstract_search.py:739           search_internal, fitness = self._fit(...)
mock_search.py:101               return self._fit_fast(model=model, analysis=analysis)
mock_search.py:95                fitness([prior.mean for prior in model.priors_ordered_by_id])
mock_search.py:82                if self.result.instance is None:      <-- here
result.py:117                    return self.samples_summary.instance
...
geometry_profiles.py:237         validate.validate_ell_comps(ell_comps=ell_comps)
autogalaxy.exc.ModelParameterException: ell_comps must satisfy
  ell_comps[0]**2 + ell_comps[1]**2 < 1; got (1.0, 1.0), magnitude 1.4142135623730951
```

## Corrections to the original prompt — do not re-tread these

- **"The path runs through serialization into the database and back out through
  the aggregator."** Wrong. The exception is raised during `search.fit(...)`,
  before `af.Aggregator.from_database` is ever called. No database round-trip is
  involved.
- **"`MockSearch._fit_fast` evaluates at `[prior.mean ...]`, which is 0.0 for
  `ell_comps` — valid."** The *vector* is indeed valid. The crash is on the next
  line (`mock_search.py:82`, `self.result.instance`), which builds an instance
  from the **summary**, not from the vector.
- **"`MockSamplesSummary.default()` uses an empty `Collection()`, so its `_kwargs`
  is `{}`."** Correct, and that is exactly why the search-side summary was a dead
  end. The reaching path is `MockResult`'s fallback `MockSamplesSummary(model=model)`
  — a *different* construction site that was never checked.
- The exception type is `ModelParameterException`, not `ValueError`.
- The original "DISPROVEN — do not re-tread" note about
  `parameter_list_with_physical_ell_comps` **stands**: `model.all_paths` and
  `model.unique_prior_paths` (used by `Sample.from_lists`) are both sorted by
  prior id, so the helper's index alignment is correct.

## Second, independent defect: `ag.m.MockResult` narrows its parent's API

```python
# autogalaxy/analysis/mock/mock_result.py
class MockResult(af.m.MockResult):
    def __init__(self, samples=None, instance=None, model=None,
                 analysis=None, search=None,
                 max_log_likelihood_galaxies=None, max_log_likelihood_tracer=None):
```

`samples_summary` is absent from the signature and is not forwarded, so
`ag.m.MockResult(..., samples_summary=...)` raises
`TypeError: MockResult.__init__() got an unexpected keyword argument 'samples_summary'`.
Callers therefore *cannot* avoid the all-ones fallback through `ag.m.MockResult`
at all — which is why the workspace fix had to switch to `af.m.MockResult`.
Confirmed by direct experiment.

## Evidence: two controlled variants isolate the two causes

Both run against library `main` with the pre-fix or post-fix `ellipse.py`:

| Variant | Script parameters | `samples_summary` passed? | Result |
|---|---|---|---|
| Original (pre-fix) | `prior_count * [1.0]`, `* [10.0]` | no | fails at `(1.0, 1.0)` — **the reported symptom** |
| A | `prior_count * [1.0]`, `* [10.0]` | yes | fails at `(10.0, 10.0)` — script's own fill |
| B | physical (`ell_comps` → 0.1) | no | fails at `(1.0, 1.0)` — **library defect alone** |
| Current `main` | physical | yes | passes |

Variant B is the decisive one: with physically-valid fixture values, the library
fallback still produces the exact reported `(1.0, 1.0)`. The library defect is
real and independent of the workspace fixture values.

## The fix (written and validated)

```diff
--- a/autofit/non_linear/mock/mock_samples_summary.py
+++ b/autofit/non_linear/mock/mock_samples_summary.py
@@ -23,7 +23,11 @@ class MockSamplesSummary(SamplesSummary):
         self._max_log_likelihood_instance = max_log_likelihood_instance
         self._prior_means = prior_means
-        self._kwargs = {path: 1.0 for path in self.model.paths} if self.model else {}
+        self._kwargs = (
+            {path: prior.value_for(0.5) for path, prior in self.model.path_priors_tuples}
+            if self.model
+            else {}
+        )
```

This matches the idiom already used by `_make_samples` in `mock_search.py`
(`prior.value_for(0.5)`), so the fix is consistent with the package's own
convention rather than a new one.

### Validation actually run (libraries at `main`, Python 3.11 venv)

| Suite | With fix | Baseline (no fix) | Verdict |
|---|---|---|---|
| PyAutoFit `test_autofit` | 1694 passed, 1 failed | 1694 passed, 1 failed | identical — no regression |
| PyAutoGalaxy `test_autogalaxy` | 1081 passed, 0 failed | — | clean |
| PyAutoLens `test_autolens` | 518 passed, 1 failed | 1 failed | identical — no regression |
| All 7 reported scripts | 7/7 pass | 7/7 pass | clean |
| Variant B (fixture fix reverted) | passes | fails `(1.0, 1.0)` | fix is load-bearing |

The two pre-existing failures are unrelated and reproduce without the patch:
`test_autofit/graphical/functionality/test_messages.py::test_beta` and
`test_autolens/potential_correction/test_iterative_interferometer.py::test__solve_joint_optimization__identity_damping_finite`.

## What was implemented

Branch `claude/autofit-mock-ones-parameters-bug-sv303m` in both repos.

**PyAutoFit** (`2581ecf`):
1. New shared helper `prior_median_kwargs(model)` in `mock_samples.py`.
2. `MockSamplesSummary.__init__` and `MockSamples.default_sample_list` both use
   it instead of `{path: 1.0 ...}`. `_make_samples` in `mock_search.py` now
   delegates to it too — the idiom it already used, in one place rather than three.
3. New `test_autofit/non_linear/samples/test_mock_placeholders.py` — 4 tests using
   a guard class that mirrors the `ell_comps` constraint, so the regression is
   covered inside PyAutoFit with no autogalaxy dependency. Verified to fail 3/4
   without the fix.

**PyAutoGalaxy** (`96baf25`): `MockResult.__init__` accepts `samples_summary` and
forwards it to `super()`. `al.m.MockResult` *is* `ag.m.MockResult` (re-exported,
not a second subclass), so PyAutoLens is covered by the same change.

### Post-implementation validation

| Suite | Result | Baseline | Verdict |
|---|---|---|---|
| PyAutoFit | 1698 passed, 1 failed | 1694 passed, 1 failed | +4 new tests, no regression |
| PyAutoGalaxy | 1081 passed, 0 failed | 1081 passed, 0 failed | clean |
| PyAutoLens | 518 passed, 1 failed | 518 passed, 1 failed | no regression |
| All 7 reported scripts | 7/7 pass | 7/7 pass | clean |
| Variant B | passes | fails `(1.0, 1.0)` | fix is load-bearing |

The latent call site `test_autogalaxy/analysis/analysis/test_analysis.py:40` is
green under the full PyAutoGalaxy suite above.

## Remaining scope

Optional tidiness only (original suggestion 4): have `MockSearch` inherit
`samples_summary` from a passed-in `result` instead of silently defaulting to
`MockSamplesSummary.default()`. With the fix above this is no longer a
correctness issue. Not done — it touches ~55 `MockSearch` call sites and belongs
in its own behaviour-preserving change.

**Difficulty is `small`, not `too-large`.** The original sizing assumed a 3-repo
library+workspace coordination. The workspace half is already shipped; what is
left is a self-contained PyAutoFit change (plus an optional small PyAutoGalaxy
one), with all three library suites already shown green against it.

## How to reproduce (this works from a cloud session)

```bash
python3.12 -m venv venv && ./venv/bin/pip install autolens   # pulls the full stack
./venv/bin/pip uninstall -y autofit autogalaxy autoarray autonerves autolens
# then put the source checkouts on PYTHONPATH:
export PYTHONPATH=<PyAutoFit>:<PyAutoGalaxy>:<PyAutoArray>:<PyAutoNerves>:<PyAutoLens>
export PYAUTO_SKIP_WORKSPACE_VERSION_CHECK=1
cd autogalaxy_workspace_test/scripts/misc/aggregator && python ellipse.py
```

Install the released stack first to get the dependency closure, then shadow the
four libraries with source checkouts via `PYTHONPATH` — an editable install of the
checkouts is refused on Python 3.11 because `autonerves` now requires `>=3.12`,
and the `PYTHONPATH` route sidesteps that gate. To reproduce the original failure,
check out `autogalaxy_workspace_test` at `40beb30^`.

## Notes

- Do not relax or move the `ell_comps` guard. It is correct.
- The workspace-side fixes (#104, #256) are legitimate and should stay: these are
  integration fixtures, and physically-valid fixture values are the right thing
  regardless of the library defect. They are not masking — after the library fix,
  variant B shows the scripts pass on their own merit either way.
- PyAutoHeart#27 is a different family (release-profile timeouts and a JAX
  exception, 2026-07-06); it is not related.
- Sibling work already shipped: the one genuinely unphysical shipped literal,
  `ell_comps=(0.5, 0.9)` in HowToGalaxy `tutorial_3_fitting`, was corrected
  separately. An AST scan of 454 `ell_comps` literals across the workspace repos
  found no other violating literal.
