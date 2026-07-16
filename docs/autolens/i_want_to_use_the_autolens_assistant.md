# I want to use the autolens_assistant to perform Expectation Propagation

Type: docs
Target: PyAutoLens
Repos:
- PyAutoLens
- autolens_assistant
- autolens_workspace
Difficulty: too-large
Autonomy: supervised
Priority: high
Status: formalised

I want to use the autolens_assistant to perform Expectation Propagation (EP) analysis of a Cosmology science case.

The science case is inferring the Hubble constant from time delay lensed quasars, and a example package already
containing EP scripts and runs, simulators and other key things is at:

/mnt/c/Users/Jammy/Science/concr/scritps/cosmology and /mnt/c/Users/Jammy/Science/concr/simulator/cosmology.py

This is actually quite a mature project, but its a git old so probably has some API drift (e.g. old PyAutoLens)
and generally needs to be brushed up.

There are also EP and other examples in autolens_workspace/scripts/guides/modeling/advanced

Can you therefore make a new science project using the autolens_assistant, which uses the main scripts in thee projects
project to perform the EP fit but also allows for the one by one / graphical fits. However, for now, I want to descope
down from the Hubble coonstant for now, and have the only goal be to simulate N strong lens using the power-law + shear
mass model, where the power-law slopes are drawn from a hierarchical distribution. The example scripts should
then be built around recovering the slopes acurate but, more important the mean and scatter of the slope hierarchical
parameter.

The goal are:

1) Show that we can do this for large samples without EP, using JAX gradient samples (SPECIFY).

2) Show that we can do this with EP, ideally showing it recovers the same values and errors.

3) We are going to scale up to large lens samples, so make sure all of this can run on RAL and its HPC via the HPC link.

4) To test all the graphical EP diagnostics and result analysis code, especially tyhe recent EP updates we did last week.

<!-- formalised by the Intake (Conception) Agent on 2026-07-16 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/32708468-5918-4dbc-a763-583805364341/scratchpad/intake_ep_cosmology.md -->
