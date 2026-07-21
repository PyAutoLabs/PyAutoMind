# Research profiling experiment in the autolens_profiling repo

Type: research
Target: workspaces
Repos:
- autolens_profiling
Difficulty: hard
Autonomy: safe
Priority: normal
Status: formalised

Research profiling experiment in the autolens_profiling repo. We currently have autolens_profiling examples that run JAX gradient max-likelihood optimizers on a single lens galaxy with a single MGE source. Extend this to a much higher-dimensional, harder model: 4 lens galaxies + 4 source galaxies. Write a simulator.py that generates the dataset from known input truth, then run the existing JAX gradient optimizers (max-likelihood samplers) alongside Nautilus and record whether any of them scale to this dimensionality and recover the input truth. If none of the optimizers succeed, investigate more careful initialization strategies. This is an exploratory benchmark, not a library change.

<!-- formalised by the Intake (Conception) Agent on 2026-07-21 from user-intake -->
