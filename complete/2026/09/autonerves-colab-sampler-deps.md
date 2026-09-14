Adds the regression test that PyAutoNerves#164 shipped without.

The Colab bootstrap installs with `pip install *packages --no-deps`, so a sampler
absent from the list never lands and the notebook cell constructing that search
dies with `ModuleNotFoundError` at fit time. `dynesty` and `emcee` were missing,
breaking Dynesty/Emcee examples across all six `_PROJECTS` entries. #164 fixed the
list but added no test: `TestRegistry` asserted only `packages[0] == "autonerves"`.

`TestRegistry.test_every_project_installs_every_sampler` now asserts that for every
key in `_PROJECTS` the resolved `packages` list contains `dynesty`, `emcee` and
`nautilus-sampler`, matched on requirement name with the version specifier split
off so a future re-pin cannot break it.

- Tests: 184 passed (183 before); 21 in `test_setup_colab.py`. CI green on
  unittest 3.12, 3.13 and unittest-nojax.
- Control test: dropping each of the three samplers makes the assertion fail;
  substituting `dynesty==9.9.9` and a bare unpinned `emcee` keeps it passing.
- `autonerves/setup_colab.py` untouched, byte-identical to main. The `_SAMPLERS`
  regrouping floated in the plan was deliberately not taken as unrequested churn
  on freshly-merged code.
- `--no-deps` audit: dynesty needs numpy+scipy, emcee needs numpy,
  nautilus-sampler needs numpy/scipy/scikit-learn/threadpoolctl — all present in a
  stock Colab image. Nothing further required.

Shipped under a human heart-ack covering "autogalaxy_workspace: Smoke Tests failure
on main; release validation FAILED (stage integrate); workspace validation not
passing (3 failed, cloud#34824535982)", authorising PR-open only; merge was a
separate human act.

**The user-visible bug remains live and is not fixed by this merge.** The released
`autonerves 2026.9.14.1` was tagged from `0e7163b` (2026-09-08) and uploaded
2026-09-14T09:25Z, about nine hours before #164 merged at 18:48 EDT. Colab
`pip install autonerves` fresh every run, so it still receives the sampler-less
list. Only a new autonerves PyPI release clears it.

Follow-up filed: `draft/bug/autonerves/nautilus_sampler_pin_drifts_from_pyautofit.md`
— `setup_colab.py` pins `nautilus-sampler==1.0.4` while PyAutoFit's
`pyproject.toml` declares `1.0.5`.

## Original prompt

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
Issued: 2026-09-14

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
