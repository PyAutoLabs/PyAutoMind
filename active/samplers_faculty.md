# Samplers faculty for PyAutoBrain plus a prototype-profile-promote skill

Type: feature
Target: PyAutoBrain
Repos:
- PyAutoBrain
- PyAutoMemory
- PyAutoFit
- autofit_workspace_developer
- autofit_workspace_test
- autolens_profiling
Difficulty: too-large
Autonomy: supervised
Priority: normal
Status: formalised

Samplers faculty for PyAutoBrain plus a prototype-profile-promote skill.

The recurring "prototype -> profile -> promote" sampler work should have a
dedicated reasoning agent in the Brain.

Background / history (already established, April-June 2026):
- autofit_workspace_developer/searches_minimal — minimal scripts plugging
  external sampler APIs directly into af.Model/Analysis without the full
  NonLinearSearch machinery (dynesty, emcee, lbfgs, nautilus + JAX, NSS
  simple/jit/grad, BlackJAX NUTS), with shared _metrics.py MLTracker
  diagnostics (evals-to-ML, time-to-ML) and output/comparison.txt benchmark
  tables (wall time, evals, time/eval, ESS, log Z, n_live).
- autofit_workspace_developer/searches — archive of samplers removed from
  PyAutoFit (UltraNest, PySwarms).
- autofit_workspace_test/scripts/searches — integration scripts for the real
  PyAutoFit searches (Dynesty, Emcee, Nautilus, Zeus, LBFGS, BlackJAXNUTS,
  *_jax jitted-likelihood variants).
- Profiling campaigns for autofit/autolens use cases, including the A100 runs
  in autolens_profiling (NSS 7.5x faster per eval on MGE; OOM on
  pixelization/delaunay via vmap fan-out; chunked-vmap fix).

Deliverables:
1. agents/faculties/samplers/ in PyAutoBrain — a read-only faculty (opines,
   never dispatches) that feature/bug/intake conductors consult when a task
   touches non-linear search work. It must reason about: which sampler suits
   which likelihood; JAX and gradient availability (jit/vmap/grad constraints,
   chunked-vmap for inversion-heavy likelihoods); how samples from one search
   can initialize another and which samplers *require* good initialization
   (e.g. HMC/NUTS from a nested-sampling posterior); cost/diagnostic metrics
   (evals-to-ML, ESS, log Z agreement). AGENTS.md + deterministic entrypoint
   per the Brain faculty template.
2. The faculty stays thin and points at: the PyAutoFit search API
   (autofit/non_linear/search), the three script tiers above, and
   PyAutoMemory/methods_wiki for the science.
3. Grow PyAutoMemory/methods_wiki — pages for HMC/gradient-based sampling,
   initialization chaining, and a sampler-comparison page recording the
   benchmark campaign results and where the raw numbers live. (methods_wiki is
   personal; the faculty is internal so linking there is fine — but no
   PyAutoMemory references may leak into public repos.)
4. A skill that drives the prototype -> profile -> promote pipeline through
   the existing start_dev workflow: new sampler lands first as a
   searches_minimal script with MLTracker diagnostics, then profiling
   comparison, then (if warranted) full PyAutoFit implementation + workspace
   _test integration scripts.

Not in scope: a new conductor (the conductor set stays small; dev legs route
through feature/bug -> start_dev), and no library code changes in PyAutoFit
itself.

<!-- formalised by the Intake (Conception) Agent on 2026-07-08 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/1e711fdf-f152-4a35-9ea7-adb4e14849f3/scratchpad/samplers_faculty_intake.md -->
