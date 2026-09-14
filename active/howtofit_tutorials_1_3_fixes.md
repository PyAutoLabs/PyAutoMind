# HowToFit tutorials 1-3: data figure, math rendering, MLE start point

Type: docs
Target: HowToFit
Repos:
- HowToFit
- PyAutoNerves
Themes:
- howtofit
- notebooks
- rendering
- colab
Difficulty: medium
Autonomy: safe
Priority: normal
Status: formalised
Consequence: judge
Review-minutes: 20
Unattended: ready
Filed: 2026-09-14
Issued: 2026-09-14

## User request (verbatim)

Fixes to HowToFit tutorials 1 through 3, auto all the way to PR without asking me HowToFit:

Tutorial 1

show image of 1D Gaussian data (from the RTD example) with brief explanatory text after:
"Where:

x: The x-axis coordinate where the Gaussian is evaluated.

N: The overall normalization of the Gaussian.

\sigma: The size of the Gaussian (Full Width Half Maximum,  FWHM , is  22ln2−−−−√σ )."

An af.Model did not have `` around it to look like code, fix that and make sure its ok through HowTo.

Replace:

same issue here albeit it is less technical:
The figure is identical to the previous one too, and that is the point worth taking from this example. The two ways of writing the composition look different on the page, but they build the same structure, and structure is all the map draws. Whenever you change how a model is written, draw it: if the map does not move then nothing about the model moved either, and any difference between the two fits has to be hiding in the legend rather than in the model.

With:

The figure is identical to the previous example, because both ways of writing the model produce the same model structure.

This is a useful check when composing models in different ways: if the figure looks the same, the underlying structure of the model is the same too. Any differences between the fits must therefore come from details such as the parameter priors or fixed values, rather than how the model is composed.

Can you end tutorial 1 here:

Extensibility

It should now be clear why we use Model and Collection objects to construct our model.

These objects facilitate the straightforward extension of our models to include multiple components and parameters. For instance, we can add more Gaussian and Exponential components to the Collection, or define new Python classes to represent entirely new model components with additional parameters.

These objects serve numerous other essential purposes that we will explore in subsequent tutorials.

With an actual example which uses the API, Gaussian and Exponential to compose an 18 parameter model of x2 Gaussian
and x4 Expoentnial, displaying its model.info and image but nothing else.

Also look for typos

Tutorial 2:

Make sure stuff like this displays correctly in jupyter:

[ \text{normalized_residual} = \frac{\text{residual_map}}{\text{noise_map}} = \frac{\text{data} - \text{model_data}}{\text{noise_map}} ]

Also look for typos

Tutorial 3:

Again certain equations especially in the parameter space bit are not math formatted.

The MLE fit went wrong for me can you make the starting point closer so it always work, but not so close its
unfair.

    result = search.fit(model=model, analysis=analysis)

    ModuleNotFoundError: No module named 'emcee'
    (traceback through autofit/non_linear/search/mcmc/emcee/search.py line 135, Colab,
     /usr/local/lib/python3.13/dist-packages/autofit)

## Audit (session findings, 2026-09-14)

**Tutorial 1** (`scripts/chapter_1_introduction/tutorial_1_models.py`)

- No data figure exists. The RTD original is
  `PyAutoFit/docs/overview/python_api.md` lines 48-68: the `data.png` errorbar
  figure, then the `g(x, I, \sigma)` equation, then the `Where:` list. The
  tutorial has the equation + `Where:` list (lines 101-112) but no figure.
  The dataset is `dataset/example_1d/gaussian_x1` (centre 50.0,
  normalization 25.0, sigma 10.0); tutorials 2 and 3 already load it with an
  auto-simulation `subprocess` guard that tutorial 1 can copy verbatim.
- Line 261 `af.Model` is bare prose; line 212 `a Model object` and line 204
  `the Gaussian class` are the same class of miss. A sweep of every
  module-level docstring in `scripts/` finds only two `af.`-prefixed misses
  (t1:261 and `log_likelihood_function` at
  `tutorial_4_why_modeling_is_hard.py:169`), plus a handful of bare class
  names in chapter 1.
- Typos: the Gaussian equation writes `g(x, I, \sigma)` but the parameter is
  named `N` below it (same for the Exponential's `g(x, I, \lambda)`);
  line 118 calls the parameters `(x, N, \sigma)` when the class names them
  `centre, normalization, sigma`; line 367 `ratw` -> `rate`; line 368 `has
  fast` -> `how fast`; line 376 the `Exponential.model_data_from` docstring
  says "Returns a 1D Gaussian"; line 461 prints `sigma (Exponential)` for
  `instance.exponential.rate`; line 93 points a HowToFit clone at
  `autofit_workspace`; line 110/111 carry a stray double blank line.

**Tutorial 2** (`tutorial_2_fitting_data.py`) — display math at lines 297,
323, 344, 365-367 and 387 uses `\[ ... \]`, which Jupyter/Colab's markdown
renderer does not typeset (only `$...$` / `$$...$$` are default delimiters).
Confirmed unrendered in `notebooks/.../tutorial_2_fitting_data.ipynb` cell 22.

**Tutorial 3** (`tutorial_3_non_linear_search.py`) — the Parameter Space
section (lines 52-88) uses both `\[ ... \]` display math and `\( ... \)`
inline math; neither renders. The MLE `InitializerParamStartPoints` at lines
508-514 starts at `centre=55.0, normalization=20.0, sigma=8.0` against a truth
of `50.0 / 25.0 / 10.0` — far enough that LBFGS does not reliably converge.

**Root cause of the `emcee` traceback** — not a HowToFit bug. `emcee>=3.1.6`
and `dynesty==2.1.5` are real `dependencies` of autofit
(`PyAutoFit/pyproject.toml` lines 42 and 44), but the Colab bootstrap
`PyAutoNerves/autonerves/setup_colab.py` installs the stack with `--no-deps`
(line ~270) and neither package is listed in `_SHARED_EXTRAS`. Every Colab
run of tutorial 3 therefore dies at the `af.Emcee` fit, and would die again at
`af.DynestyStatic`. Fix belongs in `_SHARED_EXTRAS`; it reaches users on the
next `autonerves` release.

## Scope

Math-delimiter conversion is scoped to tutorials 1-3 as requested. Tutorials 6,
7 and `tutorial_optional_bayesian_formalism.py` carry the same unrendered
`\[ \]` / `\( \)` blocks and need a follow-up sweep.
