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
