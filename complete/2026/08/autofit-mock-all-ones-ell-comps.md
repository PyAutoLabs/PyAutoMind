# autofit-mock-all-ones-ell-comps

- shipped: 2026-08-13
- repos:
  - PyAutoFit
  - PyAutoGalaxy
- PRs:
  - PyAutoFit#1471 `aea9a40` — fill mock sample placeholders from prior medians
  - PyAutoGalaxy#569 `ee0f471` — let `MockResult` accept and forward `samples_summary`
  - PyAutoMind#184 `3cd074e` — correct the prompt's root-cause theory

## Summary

PyAutoFit's mock scaffolding filled every parameter with a blanket `1.0`, which
is an invalid `ell_comps` for any elliptical profile (magnitude must be below 1;
`(1.0, 1.0)` is 1.414). Replaced with each prior's median via a shared
`prior_median_kwargs(model)` helper, and widened `ag.m.MockResult` so callers can
actually supply their own summary.

The reported symptom — 7 aggregator integration scripts failing across
`autogalaxy_workspace_test` and `autolens_workspace_test` — was **already gone**
before this task started. It had been fixed workspace-side on 2026-08-10 18:54
(`autogalaxy_workspace_test` #104, `autolens_workspace_test` #256), hours after
Heart run 31356506626 sampled it. The ticket was filed against stale evidence.
What shipped here is the library defect those commits worked around.

## Root cause

`af.m.MockResult.__init__` falls back to building its own summary when the caller
passes a `model` but no `samples_summary`:

```python
samples_summary=samples_summary or MockSamplesSummary(model=model or ModelMapper())
```

and `MockSamplesSummary.__init__` filled it with `{path: 1.0 for path in self.model.paths}`.
That dict backs both `max_log_likelihood_sample` and `median_pdf_sample`, so
reading `Result.instance` on such a result raised.

The crash fires inside `search.fit(...)`, at `mock_search.py:82`
(`if self.result.instance is None`) — **not** in the aggregator, and with no
database round-trip involved.

## Traps — read these before re-treading

Three claims in the original prompt were wrong. They are recorded because each
one is a plausible-looking dead end someone will re-derive:

- **"The path runs through serialization into the database and back out through
  the aggregator."** No. The exception precedes `af.Aggregator.from_database`.
- **"`_fit_fast` evaluates at `[prior.mean ...]`, which is 0.0 for `ell_comps` —
  valid."** The *vector* is valid. The crash is on the next line, building an
  instance from the **summary**.
- **"`MockSamplesSummary.default()` uses an empty `Collection()`, so `_kwargs` is
  `{}`."** True, and that is why the search-side summary is a dead end — but the
  reaching path is `MockResult`'s fallback `MockSamplesSummary(model=model)`, a
  different construction site.

The original prompt's **"DISPROVEN — do not re-tread"** note about
`parameter_list_with_physical_ell_comps` **stands**: `model.all_paths` and
`model.unique_prior_paths` (used by `Sample.from_lists`) are both sorted by prior
id, so the helper's index alignment is correct. Do not "fix" it.

Also: the exception type is `ModelParameterException`, not `ValueError`.

## Second defect found along the way

`ag.m.MockResult` subclassed `af.m.MockResult` but omitted `samples_summary` from
its signature, so `ag.m.MockResult(..., samples_summary=...)` raised `TypeError`.
Callers could not avoid the bad fallback through it at all — which is why the
workspace fix had to switch to `af.m.MockResult`. `al.m.MockResult` **is** this
same class (re-exported by PyAutoLens, not a second subclass), so one change
covered both.

## How it was isolated

Two controlled variants against library `main`, which separate the two
independent causes:

| Variant | Script parameters | `samples_summary` passed? | Result |
|---|---|---|---|
| Original (pre-fix) | `prior_count * [1.0]`, `* [10.0]` | no | fails `(1.0, 1.0)` — the reported symptom |
| A | `prior_count * [1.0]`, `* [10.0]` | yes | fails `(10.0, 10.0)` — script's own fill |
| B | physical (`ell_comps` → 0.1) | no | fails `(1.0, 1.0)` — **library defect alone** |
| Current `main` | physical | yes | passes |

Variant B is the decisive one: with physically-valid fixture values the library
fallback still produces the exact reported value, proving the defect is real and
independent of the workspace fixtures.

## Validation

| Suite | With fix | Baseline | Verdict |
|---|---|---|---|
| PyAutoFit `test_autofit` | 1698 passed, 1 failed | 1694 passed, 1 failed | +4 new tests, no regression |
| PyAutoGalaxy `test_autogalaxy` | 1081 passed, 0 failed | same | clean |
| PyAutoLens `test_autolens` | 518 passed, 1 failed | same | no regression |
| All 7 reported scripts | 7/7 pass | 7/7 pass | clean |

Both residual failures are pre-existing and unrelated, and reproduce without the
change: `graphical/functionality/test_messages.py::test_beta` and
`potential_correction/test_iterative_interferometer.py::test__solve_joint_optimization__identity_damping_finite`.

CI ran the unittest matrix on Python 3.12 and 3.13; both green.

## Regression cover

`test_autofit/non_linear/samples/test_mock_placeholders.py` — 4 tests built on a
guard class mirroring the `ell_comps` constraint, so the regression is covered
inside PyAutoFit with no `autogalaxy` dependency. Verified to fail 3/4 against
unpatched code.

## Reproducing the full stack from a cloud session

The original prompt claimed the autogalaxy stack "could not be installed" in a
cloud session and that reproduction needed a local environment. **It can be**, and
this whole task was done that way:

```bash
python3.12 -m venv venv && ./venv/bin/pip install autolens   # pulls the dependency closure
./venv/bin/pip uninstall -y autofit autogalaxy autoarray autonerves autolens
export PYTHONPATH=<PyAutoFit>:<PyAutoGalaxy>:<PyAutoArray>:<PyAutoNerves>:<PyAutoLens>
export PYAUTO_SKIP_WORKSPACE_VERSION_CHECK=1
cd autogalaxy_workspace_test/scripts/misc/aggregator && python ellipse.py
```

Install the released stack first for its dependency closure, then shadow the
libraries with source checkouts via `PYTHONPATH`. The `PYTHONPATH` route (rather
than `pip install -e`) matters: an editable install is refused on Python 3.11
because `autonerves` now requires `>=3.12`. To reproduce the original failure,
check out `autogalaxy_workspace_test` at `40beb30^`.

## Sizing note

Filed as `medium`; the Bug Agent scored it **too-large (17)** on a 3-repo
library+workspace coordination. Both were wrong once the workspace half turned
out to be already shipped — the actual change was **small**: one helper, three
call sites, one signature.

## Not done

Optional tidiness: having `MockSearch` inherit `samples_summary` from a passed-in
`result` rather than silently defaulting to `MockSamplesSummary.default()`. No
longer a correctness issue after this fix, and it touches ~55 `MockSearch` call
sites, so it belongs in its own behaviour-preserving change.

## Original prompt

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
