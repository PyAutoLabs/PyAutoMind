# HowToFit chapter 1: tutorial 4/6 review feedback (backticks, missing images, T6→T7 moves)

Type: docs
Target: HowToFit
Repos:
- HowToFit
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: formalised
Consequence: judge
Witness: the six PNGs referenced by `tutorial_4_why_modeling_is_hard.py` resolve to committed files under `scripts/chapter_1_introduction/images/`; `grep -n 'Resampling Info\|n_divergent' scripts/chapter_1_introduction/tutorial_6_gradients.py` returns nothing; tutorial 7 prints the three Hamiltonian diagnostics from a live `BlackJAXNUTS` result; notebooks and markdown mirrors regenerated (`generate.py` for `notebooks/`, `generate_markdown.py` for `markdown/`).
Review-minutes: 60
Unattended: no
Filed: 2026-09-14
Issued: 2026-09-14

A read-through of HowToFit chapter 1 tutorials 4, 5 and 6 produced the feedback below. The Colab
`ModuleNotFoundError` failures the same read-through hit are a separate PyAutoNerves bug
(`draft/bug/autonerves/colab_setup_missing_dynesty_and_emcee.md`) and are NOT in scope here.

## 1. Tutorial 4 — unbackticked code identifiers

`scripts/chapter_1_introduction/tutorial_4_why_modeling_is_hard.py` lines 169-170 refer to
`log_likelihood_function` and `model_data` as bare words, where the surrounding prose (lines 166,
180, 183-184, 209, 246) backticks both. Add the missing backticks.

## 2. Tutorial 4 — six referenced images are missing from the repo

Lines 461-477 promise a bad/okay/good comparison and embed two `<table>` blocks pointing at:

    scripts/chapter_1_introduction/images/{bad,okay,good}_fit.png
    scripts/chapter_1_introduction/images/{bad,okay,good}_normalized_residual_map.png

`scripts/chapter_1_introduction/images/` does not exist in the repo and none of the six files are
tracked, so all six render broken. The prose that follows leans on them directly ("This ideal
scenario is illustrated in the `good_fit.png` image above", "This is what happened for the okay and
bad fits above").

Decision taken at review: **generate and commit the images.** Run the tutorial's own 15-parameter
`Collection` fit repeatedly until it lands a clearly bad, a marginal/okay and a good solution, and
save each one's model fit and normalized-residual figure using the tutorial's own plotting code so
the figures match what a reader produces. The okay case must actually show normalized residuals
above 3.0 sigma, since the prose asserts exactly that. Present the candidate figures for sign-off
before committing.

## 3. Tutorial 6 — `search.summary` / Resampling Info block belongs in tutorial 7

`tutorial_6_gradients.py` lines 636-660 read `search.summary` off disk and explain the
`Value-NaN Lane-Steps` and `Gradient-NaN Lane-Steps` counters, then close by saying "Tutorial 7
explains where they come from and what to do about them." Tutorial 7 already has a full
`__NaN Diagnostics__` section (`tutorial_7_the_details.py` line 957) covering the same file and the
same two counters. The block is premature and duplicated: **delete it from tutorial 6**, including
the `search.summary` read and the paragraph above it, and confirm tutorial 7's section needs no
addition to stand alone.

## 4. Tutorial 6 — the ball analogy is unnecessary

Lines 688-699 introduce Hamiltonian Monte Carlo via an extended analogy: the likelihood surface
turned upside down, a ball given "a random flick", accelerating down slopes, coasting up the other
side, and NUTS deciding "how long to let the ball roll". Replace this with the plain statement that
`BlackJAXNUTS` is MCMC where the walker knows which way to step, keeping only as much of the
trajectory picture as the No-U-Turn name actually requires to make sense. Line 902 in the wrap-up
repeats the ball image ("rolls a ball across the landscape") and must be brought into line.

## 5. Tutorial 6 — Hamiltonian diagnostics belong in tutorial 7

Lines 723-742 explain `n_divergent`, `ess_min` and `mean_acceptance` and print them from
`samples.samples_info`. This is too much detail for tutorial 6.

Decision taken at review: **move both the prose and the prints to tutorial 7, adding a
`BlackJAXNUTS` fit there so the numbers come from a live result.** Tutorial 7 currently runs
`DynestyStatic`, `Emcee` and `MultiStartAdam` only; its `__Comparing Searches__` section (line 616)
is the natural home, with the diagnostics as their own subsection near `__NaN Diagnostics__`.
Update tutorial 7's `__Contents__` list (lines 36-46) accordingly, and keep the added fit cheap
enough not to blow out an already long tutorial's runtime.

## 6. Tutorial 6 — wrap-up opening sentence reads badly

Line 887: "This tutorial took the one sentence tutorial 3 used to describe how an MLE search moves
and unpacked it:". Rewrite so it reads naturally.

## Housekeeping

Tutorials 6 and 7 have no `markdown/chapter_1_introduction/` mirror (only tutorials 1-5 and 8 do),
so regenerating markdown affects tutorial 4 only; notebooks must be regenerated for 4, 6 and 7.
Use `generate.py` for `notebooks/` and `generate_markdown.py` for `markdown/` — `generate.py`
alone does not rebuild the markdown mirrors.

## Original request (verbatim)

> HowToFit:
>
> Tutorial 4:
>
> log_likelihioood_function missing `` for code in Analysis markdown section, same for model_data
>
> [Colab ModuleNotFoundError: No module named 'dynesty' — filed separately as the PyAutoNerves bug]
>
> images below this are missing? When I ran the model fit above, that's exactly what happened. It produced a range of fits: some bad, some okay, and some good, as shown in the images below:
>
> Tutorial 5:
>
> [Colab ModuleNotFoundError: No module named 'emcee' — filed separately as the PyAutoNerves bug]
>
> Tutorial 6:
>
> This and thr bit above it about search.summary can wait until tutorial 7:
>
> The block at the bottom, headed Resampling Info, contains two entries only a gradient search can report:
>
> Value-NaN Lane-Steps: the number of times a lane stepped somewhere the log likelihood could not be computed at all, most often because it stepped outside the priors.
>
> Gradient-NaN Lane-Steps: the number of times the log likelihood was computable but its gradient was not. This is the sneakier of the two, because such a lane does not crash or die, it simply stops moving while continuing to look perfectly healthy.
>
> Both counters are usually small and harmless, but they are the vocabulary you need to diagnose a gradient fit that has gone quietly wrong. Tutorial 7 explains where they come from and what to do about them.
>
> [Colab ModuleNotFoundError: No module named 'emcee' — filed separately as the PyAutoNerves bug]
>
> This ball analogy seems unecessary, I get some NUTS description might use it but just say its MCMC but the walker now knows which way to step
>
> random flick and let it roll: it accelerates down slopes, coasts up the other side and travels a long way while staying in regions the landscape favours. That trajectory is computed from the gradient at each moment, which is what autodiff hands us for free. Where the ball stops becomes the next sample, and because it travelled a long, informed distance rather than a small random hop, consecutive samples are far less similar.
>
> "NUTS" stands for the No U-Turn Sampler, which solves the awkward choice here: how long to let the ball roll. Roll too briefly and you wasted the gradient; roll too long and the ball curves back on itself. NUTS stops the trajectory when it starts doubling back. Being a gradient method, it needs the JAX analysis.
>
> This is too much info, move to tutoiral 7:
>
> Hamiltonian sampling comes with its own diagnostics, stored in the samples_info dictionary. Three are worth knowing:
>
> n_divergent: the number of trajectories which "diverged", meaning the ball flew off to infinity instead of following the landscape. A handful is tolerable; many means the steps are too large and the samples cannot be trusted.
>
> ess_min: the "effective sample size" of the worst constrained parameter. Consecutive samples are correlated, so 300 samples are worth fewer than 300 independent draws, and this says how many they are worth.
>
> mean_acceptance: the fraction of proposed trajectories accepted, which for NUTS should sit high, around the 0.8 the warm up phase tunes towards. A low value means the sampler is struggling.
>
> This is a really weird sentense in the wrap up:
>
> This tutorial took the one sentence tutorial 3 used to describe how an MLE search moves and unpacked it:

Type: docs
Target: HowToFit
Difficulty: medium
Priority: normal

<!-- formalised from user review feedback, 2026-09-14 -->
