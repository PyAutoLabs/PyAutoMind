## samplers-faculty
- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/54 (closed)
- completed: 2026-07-08
- prs: https://github.com/PyAutoLabs/PyAutoMemory/pull/16 (merged), https://github.com/PyAutoLabs/PyAutoBrain/pull/55 (merged)
- notes: |
    New Brain faculty (the fourth): agents/faculties/samplers/ — the "motor
    faculty" (samplers as gaits). AGENTS.md judgment tables (sampler<->
    likelihood match, gradient/JAX constraints incl. chunked-vmap for
    inversion-heavy likelihoods, initialization providers vs consumers,
    four promotion criteria) + deterministic read-only SamplerSurface
    entrypoint (samplers.sh/_samplers.py, stdlib-only): inventories the
    three script tiers (searches_minimal / searches archive /
    workspace_test scripts/searches), the PyAutoFit search catalogue
    (package-per-sampler layout: non_linear/search/<group>/<pkg>/), the
    minimal-tier benchmark table, and tier gaps. Live gap findings at ship:
    nest/nss, mle/drawer, mle/pyswarms, nest/ultranest have no
    workspace_test integration script — the nss one is a real candidate task.
    skills/sampler_pipeline/ drives prototype -> profile -> promote through
    start_dev (MLTracker contract, honest-benchmarking rules, promote-or-
    archive). Science backing in PyAutoMemory methods_wiki: 4 new concept
    pages (hamiltonian-monte-carlo, gpu-nested-sampling filled existing
    index red-links; initialization-chaining; sampler-benchmarks campaign
    record). install.sh auto-discovered the skill (symlink live).
    Calibration: supervised --auto, parked once at ship sign-off,
    approved-unchanged, merged-unchanged. Gotcha: a concurrent session was
    pushing to the Mind checkout mid-run — staged Mind writes by explicit
    filename instead of prompt_sync_push (git add -A) throughout.
    Follow-ups merged same day after user review: PyAutoBrain#56 — skill
    reframed as a development skill with reference.md playbook (repo-URL
    ingestion contract w/ six-dimension API classification validated
    against nessai + jaxns, bring-your-own-likelihood Stage 1b via the
    two-function af.Model/Analysis adapter or Fitness._vmap, --auto
    two-task mapping). Target UX: /sampler_pipeline <github-url> --auto.
    Conductor question settled: stays faculty+skill (consult-graph: feature
    agent must be able to consult it); flip trigger = trials become a
    frequent human verb AND promote scoring hardens into a scriptable
    SamplerDecision core.

## Original prompt

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
