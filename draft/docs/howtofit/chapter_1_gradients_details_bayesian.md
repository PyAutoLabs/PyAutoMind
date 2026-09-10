# HowToFit chapter 1: gradients, the details, and Bayesian formalism tutorials

Type: docs
Target: HowToFit
Repos:
- HowToFit
Themes:
- howtofit
- jax
- tutorials
- notebooks
Difficulty: large
Autonomy: supervised
Priority: normal
Status: formalised
Consequence: judge
Witness: three new chapter-1 scripts run green under `python .github/scripts/run_smoke.py`; regenerated notebooks, `llms-full.txt` and `workspace_index.json` pass `navigator_check.yml`; the chapter README / `start_here.py` / `llms.txt` list the new tutorials.
Review-minutes: 45
Unattended: needs-slicing
Filed: 2026-09-10

Original request (verbatim):

> I want to improve HowToFIt, first reread it all to get a sense of the style, level of detail and information content.
> Then write the following extra tutorials and aspect:
>
> Chapter 1, tutorial 6, "gradients" write this based on the following __Contents__ (but should could be multiple sections).
>
> - Gradients: Extend the phenomenoligcal description of a parameter space from tutorial 3 to include a gradient,
> the ideal that the walker or search knows for each sample which direction the likelihood around it increases it.
> Give an example of a gradient calculaiton on the 1D Gaussians using finite differencing.
> - JAX and autodiff: Now explain auto differention, motivate it by explaining that for many likliehood functions its
> too complicated to analytically compute a gradient, autodiff does it computatiojnally "under the hood". JAX-ify
> the 1D Gaussian likelihood function and illustrate it.
> - JAX search: Show a few examples of JAX gradient searches, I guess like tutorial 3 we should follow the MLE, MCMC, nested
> sampling approach explaining in each how gradients changes their approach. I guess oen section for each search type.
> - SHow how gradients can help with result analysis in a way which naturally follows a concept in tutorial 5
>   (poserior predictive test?).
>
> Chapter 1, tutorial 7, "the_details":
>
> - Discuss how you need to think carefully about your model parameteriation and avoid one where two parameters could
> "flip" and produce the same example, give example with 1D gAussian and example of using an assertion or other criteria
> to remove it.
> - Another example, you need to avoid parameterrs which lead to plataues in likelihood space, for example when the intensity
> or normalization of a gaussian is 0 all solutions become the same. Some searches may struggle with this, give example
> of fixing it.
> - This is a good point to show inference using different searches and rexplain how different searches will face
> the above issues differently, a walker based approach (MCMC) will get stuck in the mirror solutions of the first exampe
> or be unable to walk out of platues. On the other hand, a nested sampler will pretty much sample those regions, and
> pick one peak (if its single mode only), then the live points will move on past the plateau and perform will be
> good. Important lesson, comparing different searches can help us work out better how to improve inference.
> - Clipping: Models may have solutions which are unphysical outside certain bounds or for certain values, and just
> because your priors on individual parameters keep parameters physical sopmetimes its *parameter combinations* which
> can lead to this. This could, in turn, mean that models are rejected (e.g. return a NaN) or have plateaus again
> messing up searches. Give example but also explain how PyAutoFit has the resample_figure_of_merit which behaviour
> changes depending on the search.
> - Explain the value NaN and gradient NaN values that users can now see in their search.sumary files, as these are
> symbptoms of the above kind of issues. This allows us to explain that just cause a likelihood has a good value
> doesnt mean we can assume its gradient is ok.
> - Unit cube vs phyusical, come back o this point from tutorial 1 to explain how it is actually very important when
> we think about how as search sees and therefore explores parameter space
> - In summary, there are so many details we need to think of when we go about inference. OFten, non the above matter
> and we can get a good inference analysis and pipeline going without worry about these details. However, worrying about
> them will often mean inference runs faster, converges on the right solution more often, and there are worst case scdenarions where
> by not worrying about the above you may infer the wrong solution.
>
> Chapter 1, tutorial option, "bayesian formalism."
>
> - Bayesian Formalism: Now explain that everything they've learned in the previous chapter is Baeysian inference
> and run through how the contnts of tutorials 1 throuh 5 link to formal Bayesiqn equations. Make it clear that
> the point of HowToFit is to make it so you can learn inference without knowing formal maths, but it helps to know
> how to the two fit together.

## Context established at filing (2026-09-10)

- Chapter 1 currently ends with a prose-only `tutorial_6_scientific_workflow.py`; the
  new tutorials 6 and 7 displace it, so it is renumbered to tutorial 8 and the
  Bayesian formalism tutorial becomes `tutorial_optional_bayesian_formalism.py`
  (chapter 3 already uses the `tutorial_optional_*` naming).
- Chapter 1 never mentions JAX, gradients, the unit cube or posterior predictive
  checks; all are new vocabulary for the chapter.
- Installed PyAutoFit: `Analysis(use_jax=True)` swaps `self._xp` to `jax.numpy`;
  `MultiStartAdam` (autodiff MLE), `BlackJAXNUTS` (HMC MCMC) are the gradient
  searches; `LBFGS` is finite-difference; Nautilus/Dynesty use JAX only for
  vmap/jit. `search.summary` carries `Value-NaN Lane-Steps` / `Gradient-NaN
  Lane-Steps` for the multi-start gradient searches only. `add_assertion` is a
  traced `xp.where` penalty on the JAX path (PyAutoFit#1583, installed).
  `resample_figure_of_merit` is hard-coded per search (`-inf` MLE/MCMC, `-1e99`
  nested/SMC), not a config key.
