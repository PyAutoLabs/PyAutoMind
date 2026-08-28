# Themes

The controlled vocabulary for a prompt's optional `Themes:` header — *what the
work is about*, as opposed to `Target:`, which is only *where the code lives*.
Themes are the key the dashboard's auto-bundler groups on, so they are
deliberately few, deliberately topical, and deliberately cross-repo: "three
things about MGE" is a session, "three things that live in autoarray" is a
directory listing.

Usage, in a prompt's light header (see `REFERENCE.md`, "Prompt file format"):

```markdown
Themes:
- mge
- jax-gradient
```

The **first** bullet is the primary theme and is the grouping key; the rest are
affinity keywords that decide which prompts pack together inside that group.
One to three keywords is the intended shape. A keyword that is not in the list
below still renders — loudly, with a ⚠️ on the dashboard and a Hygiene count —
so a typo is visible rather than silently becoming a free-text tag.

This file is the source of truth and is meant to be edited by hand: adding a
keyword here is the whole of adding a theme, and PyAutoBrain reads it rather
than holding its own copy.

## Vocabulary

- `mge`: Multi-Gaussian Expansion light and mass profiles, and fitting with them.
- `point-source`: Point-source lens modelling — image-plane solvers, positions, flux ratios.
- `pixelization`: Pixelized source reconstruction — meshes, regularization, inversions.
- `interferometer`: Visibility-space datasets — NUFFT transforms, interferometer fits.
- `cluster`: Cluster- and group-scale lensing with many deflectors.
- `multi-band`: Multi-wavelength or multi-dataset fitting across bands and instruments.
- `jax-compile`: JAX tracing and jit compilation — compile time, retracing, the jit pipeline.
- `jax-gradient`: JAX autodiff — gradient correctness, custom rules, gradient-based search.
- `samplers`: Non-linear search machinery — nested sampling, MCMC, optimizers, search tiers.
- `numba-cpu`: The numba CPU likelihood path — kernels, caching, CPU performance.
- `graphical-ep`: Graphical models and expectation propagation — hierarchical fits.
- `profiling`: Performance measurement campaigns — likelihood profiling, benchmarks, timings.
- `hpc-gpu`: HPC and GPU execution — cluster submission, device placement, remote runs.
- `visualization`: Figures and plotters — what the organism draws, and how it reads.
- `ci-smoke`: CI workflows and workspace smoke tests — the automated green/red surface.
- `release`: Release execution — versions, tags, PyPI publication, readiness gates.
- `dashboard`: The Mind dashboard and its sibling one-tap boards.
- `mind-workflow`: The task lifecycle itself — prompts, registries, skills, the dev workflow.
- `assistants`: The domain science-assistant workspaces and their wikis.
- `docs-hub`: Public documentation surfaces — RTD, the docs hub, the chat-surface routes.
- `notebooks`: Notebook generation and the workspace script-to-notebook pipeline.
- `cti`: Charge Transfer Inefficiency calibration and modelling.
- `reduce`: Data reduction of raw imaging into modelling-ready datasets.
- `hygiene`: Code-quality upkeep — dead code, slow tests, stale docs, dependency drift.
