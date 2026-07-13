# Built-in benchmark package for autolens_assistant (4 standard prompts + run/track harness)

Type: feature
Target: autolens_assistant
Difficulty: too-large
Autonomy: supervised
Priority: normal
Status: formalised

for autolens_assistant, I now want to create in built bench marks, which have the goal of being standard prompts which we run using different AI agents and models to test performance. I want 3 prompts for assistant mode, the first is "easy" difficulty and simply does tasks already available in the workspace should be based on this prompt in README.md: Model the JWST imaging in dataset/imaging/cosmos_web_ring: perform data preparation steps, set up a sensible lens light and mass model with a pixelized source reconstruction, run the fit, and show me the reconstructed source and the fit residuals, the next is medium difficulty, it requires doing things that are not explicitly in the workspace (e.g. model comparison, changing mass profile for DM subhalo) and again is based on a README.md prompt:

Assistant mode.

The strong lens SLACS0946+1006 famously has a dark matter subhalo detection that many argue is unusually concentrated. I'd like to analyse the HST imaging of this lens provided at dataset/imaging/slacs0946+1006/ and reproduce that detection.

Specifically, I want this analysis to perform Bayesian model comparison to (a) confirm a subhalo is preferred over a smooth-mass baseline by fitting a free-position, free-mass SIS perturber across the image plane and comparing the Bayesian evidence to the no-subhalo fit, and (b) test the "super-concentrated" claim by comparing the SIS subhalo against a more shallow NFW mass profile at the recovered position.

Set the pipeline up so the smooth lens light and mass model, the pixelized source reconstruction, and the subhalo results are all inspectable on my computer, and report the Bayesian evidence for each comparison.

Assess whether the analysis will run fast on my laptop / PC GPU, and if not, set this up as a small project on the HPC I have access to.

The third should be hard mode and is a new prompt not on the README.md, with the goal that it requires us to combine 3 different packages on the autolens_workspace: group, multi, imaging and interferometer, here is the prompt:

Assistant mode.

First, I want to simulate imaging and interferometer data of a group-scale strong lens, which is composed of two SIE lens galaxies and a quadruply imaged Cored Sersic background source.

Then, I want to perform modeling of this dataset, simultaneously fitting the imaging and interferometer data. I want the foreground lens model to use multi Gaussian Expansions for the lens light, SIE's for each lens and a multi Gaussian expansion for the background source.

After this fit has been judged successful, do a follow up lens model that uses a pixelized source reconstruction, but retains the MGE lens light and SIE source.

Present me with results confirming the fit was a success.

I also want you to make one benchmark based on the Teacher mode example prompt:

Teacher mode.

I'm new to PyAutoLens and want to learn the basic workflow end-to-end. Can you walk me through it on a simple simulated example: simulate Euclid-like imaging of a simple strong lens (an isothermal mass with a Sersic source), then fit that simulated data and recover the lens model.

Explain what each step is doing and why as we go: composing the lens and source model, running the simulation, choosing the mask, the non-linear search, and how to read the result. So I come away understanding the workflow, not just the commands.

Put this in a benchmark package and have a design whereby I can run these benchmarks, track the conversation and results and store them so they can be pushed to GitHub as well as be run and tracked for different models and run with the same model to compare performance on different days. Think about if there is anything else benchmarking would benefit from and put this all in the clone agent too, e.g. make sure it's aware of it.

<!-- formalised by the Intake (Conception) Agent on 2026-07-10 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/b2cd50d3-5bf7-4aeb-99be-c2de56b54377/scratchpad/intake_benchmarks_raw.md -->
