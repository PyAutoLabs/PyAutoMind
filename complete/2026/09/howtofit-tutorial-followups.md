The two follow-ups reported out of HowToFit#57, plus two bugs found while doing
them.

**Math sweep finished.** #58 converted tutorials 1-3 only. Tutorial 6 (4 display +
28 inline), tutorial 7 (1 display) and the optional Bayesian formalism tutorial
(7 + 40) are now converted too. Conversion was AST-driven over module-level
docstrings, so nothing inside code was touched; `\begin{equation*}` environments
were left alone since MathJax renders those. Tutorial 5's single `\[` is
`suffix=" \\[-2pt]"`, a LaTeX row-break passed as a Python string to
`af.text.Samples.latex()` — code, not prose, and correctly left.

**Tutorial 3's `__Priors__` block was dead *and* wrong.** It set three priors on a
model that all five fits discarded by re-calling `af.Model(Gaussian)`, so it never
applied; the fits silently ran the `config/priors/gaussian.yaml` defaults. Two of
the three were also wrong: `normalization` `Uniform(0, 10)` excludes the true 25.0
and `sigma` `Uniform(0, 10)` puts the true 10.0 on the boundary. Five redundant
re-creations removed, so the block now takes effect.

The values deliberately **restate the config defaults** rather than narrowing
them, and that was decided by measurement, not judgement. `af.LBFGS()` initialises
with `InitializerBall(0.49, 0.51)` — a tight ball on the **centre of each prior**,
not a broad random draw — so under `normalization = Uniform(0, 50)` the centre is
exactly 25.0, the true value, and the first MLE fit, whose failure is the entire
teaching point of the MLE section, succeeded 10/10 at logL 176.1. Measured: config
priors fail 10/10, the narrowed candidate succeeds 10/10, the restated defaults
fail 10/10 and reproduce the baseline local maximum exactly. Had this been
reasoned about rather than measured, the narrowing would have shipped and silently
deleted the lesson.

**MCMC budget.** The prose after the uninitialised Emcee fit asserted it
"succeeded, finding the same high-likelihood model that the MLE search with a good
starting point identified". At `nwalkers=10, nsteps=200` it succeeded 11 times in
20. Both Emcee searches now `nwalkers=20, nsteps=500`: 80/80 in a stress test,
median 9.8s against 3.9s. **Walkers, not steps, were the lever** — 20x300 (6000
evaluations) beat 10x500 (5000). 20x300 reached 20/20 and then failed at N=60,
which is why the leaders were re-confirmed at 80 runs rather than stopping at the
first clean sweep. CI cost is unchanged: `profile_smoke.yaml` sets
`PYAUTO_TEST_MODE: "2"` (skip sampler) with no tutorial 3 override, measured
~1.5s before and after.

**`self.noise_map`.** `Analysis.log_likelihood_function` in tutorials 3, 4 and 5
computed its noise normalization from a module-level `noise_map` global while
every other line used `self.`. It returns the right number inside the tutorial
only because that global exists — and this is the class the tutorials explicitly
tell readers to copy, where it raises `NameError`. It broke the measurement
harness on first run, which is how it surfaced. Now `self.noise_map` in all three,
matching tutorials 6 and 7, which were already correct.

Smoke 18/18 PASS exit 0, CI green on all 7 checks.

A PyAutoFit correctness bug found while calibrating the MCMC budget was fixed
separately in PyAutoFit#1629 (see the `emcee-log-prob-alignment` record).

Shipped as HowToFit#60.

## Original prompt

# HowToFit follow-ups: finish the math sweep and fix tutorial 3's dead Priors block

Type: docs
Target: HowToFit
Repos:
- HowToFit
Themes:
- howtofit
- notebooks
- rendering
- priors
Difficulty: medium
Autonomy: safe
Priority: normal
Status: formalised
Consequence: judge
Review-minutes: 20
Unattended: ready
Filed: 2026-09-14
Issued: 2026-09-14
Parent: active/howtofit_tutorials_1_3_fixes.md

## User request (verbatim)

"do the follow ups"

— the two follow-ups reported out of HowToFit#57 / #58 (see that issue's
"Out of scope" section).

## Follow-up A: finish the math-delimiter sweep

`#58` converted `\[ ... \]` -> `$$ ... $$` and `\( ... \)` -> `$...$` in tutorials
1-3 only, because the reader scoped that task to tutorials 1-3. Neither `\[` nor
`\(` is a default MathJax delimiter in Jupyter, JupyterLab or Colab, so every
remaining occurrence renders as raw LaTeX. Remaining, measured on the `#58`
branch:

| File | `\[` | `\(` |
|---|---|---|
| `tutorial_5_results_and_samples.py` | 1 | 0 |
| `tutorial_6_gradients.py` | 4 | 20 |
| `tutorial_7_the_details.py` | 1 | 0 |
| `tutorial_optional_bayesian_formalism.py` | 7 | 35 |

Tutorial 5 was not in the original follow-up note but carries the same bug.
`chapter_advanced/` is clean.

## Follow-up B: tutorial 3's `__Priors__` block is dead *and* wrong

`scripts/chapter_1_introduction/tutorial_3_non_linear_search.py` sets

```python
model.centre = af.UniformPrior(lower_limit=0.0, upper_limit=100.0)
model.normalization = af.UniformPrior(lower_limit=0.0, upper_limit=10.0)
model.sigma = af.UniformPrior(lower_limit=0.0, upper_limit=10.0)
```

on a model that **every** subsequent fit discards by calling `af.Model(Gaussian)`
again before `search.fit`. The overrides therefore never apply, and the fits
silently run on the `config/priors/gaussian.yaml` defaults:

| Parameter | Truth | Tutorial override | Config default |
|---|---|---|---|
| `centre` | 50.0 | `Uniform(0, 100)` | `Uniform(0, 100)` — identical |
| `normalization` | 25.0 | `Uniform(0, 10)` — **excludes the truth** | `LogUniform(1e-6, 1e6)` |
| `sigma` | 10.0 | `Uniform(0, 10)` — **truth sits on the boundary** | `Uniform(0, 25)` |

So the block teaches a prior override that never applies and would break the fit
if it did. It also contradicts its own prose, which says "we are using
`UniformPriors` in this tutorial due to their simplicity" while every fit
actually runs a `LogUniformPrior` on `normalization`.

## The trap that decides the design

Making the overrides *apply* changes the parameter space every search explores,
and the first, uninitialised MLE fit in this tutorial is **supposed to fail** —
that failure is the pedagogical hinge of the whole MLE section ("it can get stuck
in a local maximum"). Today it fails reliably because `normalization` is
`LogUniform(1e-6, 1e6)`, so a random draw is essentially never near 25. Narrow
that to a `Uniform` band centred on plausible values and a random draw lands near
the truth often enough that the fit may start *succeeding*, which would make the
tutorial flaky in the opposite direction and silently destroy the lesson.

**Decision rule (measured, not assumed):** prefer the version that makes the
overrides real and meaningful, but only if the uninitialised first MLE fit still
fails **10 out of 10 runs**. If it does not, keep the explored parameter space
semantically equal to the config defaults and make the block honest instead.
