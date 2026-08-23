# TEST_MODE bypass crashes on ordered-parameter assertion ties

Type: bug
Target: PyAutoFit
Repos:
- @PyAutoFit
Difficulty: small
Autonomy: supervised
Priority: normal
Status: formalised — STILL REPRODUCES; see the 2026-08-09 note before grading this against main
Filed: 2026-07-17 (backfilled from git)

## 2026-08-09 — do NOT mistake the adjacent FitException catch for this fix

Checked by the draft/ sweep against PyAutoFit main (`3b960609`). The bypass path
in `abstract_search.py` **now catches `exc.FitException`** and continues with the
`-1e99` sentinel, logging "TEST MODE 2: likelihood verification raised
FitException … treating as a resample-rejected instance". That reads exactly like
this prompt's suggested fix. **It is not.** The bug below still reproduces.

The catch wraps only the likelihood call. The model instantiation is on the line
*before* the `try`:

```python
if call_likelihood:
    instance = model.instance_from_vector(vector=parameter_vector)   # <-- outside
    try:
        log_likelihood = float(analysis.log_likelihood_function(instance))
    except exc.FitException as e:
        ...
```

and `instance_from_vector` → `instance_for_arguments` → `check_assertions`
(`autofit/mapper/prior_model/abstract.py:193`) is precisely what raises
`exc.FitException("N assertions failed!")` when an ordering assertion ties at the
prior medians. `ignore_assertions` defaults to `False` and the bypass does not
pass it. So the assertion exception escapes the guard entirely and still
hard-fails the run.

The upside: the fix is now a one-liner rather than the "catch and retry with a
perturbation" design sketched below. Two options, both cheap and both
deterministic:

- move the `instance_from_vector` call inside the existing `try` — the sentinel
  path already does the right thing for a rejected instance; or
- pass `ignore_assertions=True` at the bypass instantiation, on the grounds that
  a verification eval at the medians is not a sampled point and assertions exist
  to steer sampling.

The second is probably the better semantics (a tied median is not a pathological
model), but it changes what the verification eval attests to — pick deliberately.
Prefer either over adding perturbation logic.

`Difficulty:` stays small. The § Blocks note below still holds.

---

Found during the CTI resurrection epic (Phase 4, 2026-07-17). `PYAUTO_TEST_MODE=2/3`
bypass evaluates the model at the **prior medians**. A model whose components have
identical priors plus an ordering assertion (the standard idiom for breaking
exchange degeneracy, e.g. PyAutoCTI trap models with
`model.add_assertion(trap_0.release_timescale < trap_1.release_timescale)`)
ties exactly at the medians, so the bypass evaluation raises
`autofit.exc.FitException: GreaterThanLessThanAssertion` and the script crashes.

Real samplers resample assertion-failing points gracefully — this is purely a
bypass-path artifact, and it makes every ordered-trap CTI workspace script
un-smokeable at TEST_MODE=2 (reproduced with a bare
`model.instance_from_prior_medians()`; TEST_MODE=1 passes).

Suggested fix: at the bypass evaluation, catch `FitException` from assertions
and retry with a small deterministic perturbation of the unit-cube point (or a
seeded random draw), mirroring what a real sampler does. Keep it deterministic
so smoke runs stay reproducible.

Blocks: autocti_workspace smoke coverage of `modeling/start_here.py`-class
scripts (CTI epic Phase 5); the workspace documents the artifact in its
AGENTS.md meanwhile.
