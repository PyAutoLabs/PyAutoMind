# Regression-test the Colab sampler install (code fix shipped in PyAutoNerves#164)

Type: test
Target: PyAutoNerves
Repos:
- PyAutoNerves
Difficulty: trivial
Autonomy: safe
Priority: normal
Status: formalised
Consequence: notify
Witness: a regression test in PyAutoNerves asserting that every entry of `_PROJECTS` resolves to a `packages` list containing `dynesty` and `emcee` alongside `nautilus-sampler` — i.e. that all three samplers PyAutoFit exposes as `af.DynestyStatic`, `af.Emcee` and `af.Nautilus` are installed by the Colab bootstrap.
Review-minutes: 10
Unattended: ready
Filed: 2026-09-14

## The code fix already shipped — this is the missing test

This prompt was filed 2026-09-14 from review feedback on HowToFit chapter 1
tutorials 4/5/6. The **code half was fixed independently the same day** in
PyAutoLabs/PyAutoNerves#164 (merged), which added `emcee>=3.1.6` and
`dynesty==2.1.5` to `_SHARED_EXTRAS` with the specifiers `autofit` declares, plus
a comment recording why a `--no-deps` install has to name its siblings' real
dependencies. See `complete/2026/09/howtofit-tutorials-1-3.md`.

**What did not ship is the regression test.** #164 was verified only against the
existing suite (183 passed), which asserts nothing about the contents of
`_SHARED_EXTRAS` — `test_setup_colab.py` checks only `packages[0] == "autonerves"`.
Nothing currently stops a future edit dropping a sampler again, which is exactly
how this bug arose.

## Remaining work

1. Add the test the Witness above describes: for every `_PROJECTS` entry, the
   resolved `packages` list contains `dynesty`, `emcee` and `nautilus-sampler`.
   Assert on the sampler *names*, not exact pins, so a version bump does not
   break it.
2. Consider whether the three samplers belong in their own `_SAMPLERS` list
   rather than inside `_SHARED_EXTRAS`. A missing sampler is a hard
   `ModuleNotFoundError` at fit time, not a degraded experience, so the grouping
   arguably should say so. This is a judgement call, not a given — the test in
   step 1 is the part that carries the value.

## Still true, and worth keeping in view

The install runs with `--no-deps`, so **any** real `autofit` dependency that a
stock Colab image does not ship must be named in the list explicitly or it never
arrives. `emcee` and `dynesty` were the two that bit; a broader audit of
`autofit`'s `dependencies` against a stock Colab image would say whether others
are waiting (`corner`, `typing-inspect`, `gprof2dot`, `numpydoc`, `xxhash`,
`astunparse`, `array_api_compat`, `optax` are all declared and none is named in
`_SHARED_EXTRAS`). That audit is not required by this prompt but is the obvious
next question.

Colab notebooks `pip install autonerves` fresh on every run, so #164 reaches users
only once a new `autonerves` is released to PyPI.
