# EP campaign — phase map for the 2026 Q3 graphical/EP push

Type: research
Target: graphical_ep
Themes:
- graphical-ep
Difficulty: too-large
Autonomy: human-required
Priority: high
Status: campaign map — phases route through /start_dev one at a time; this file is never issued itself and nothing here is bulk-issued
Consequence: judge
Review-minutes: 25
Unattended: needs-slicing
Epic: graphical-ep
Filed: 2026-08-19 (backfilled from git)

Filed 2026-08-19 from James's multi-phase EP brief (raw text preserved in the
intake session). This is the umbrella view; each phase's real content lives in
its own prompt file. Update the table as phases ship.

## End goals (acceptance for the campaign as a whole)

1. An analytic Gaussian model that statistically demonstrates the graphical
   and EP source code is correct (means *and* errors against closed form).
2. slope_hierarchy cosmology: accurate graphical + EP results, EP scaling to
   100+ datasets, fast, interpretable/inspectable output for a scientist,
   running on RAL A100s.
3. IC50: graphical + EP scaling to 10 000+ datasets, with EP-vs-graphical
   parity demonstrated at small N.

## Phases

| # | Phase | Prompt | State (2026-08-19) |
|---|-------|--------|--------------------|
| 1 | Analytic Gaussian benchmark (the keystone — start here) | `active/analytic_gaussian_benchmark.md` (was `research/graphical_ep/analytic_gaussian_benchmark.md`) | **issued 2026-09-02** — autofit_workspace_test#91; re-homed to `autofit_workspace_test/scripts/graphical/` (EP CI infrastructure, core parity script curated into the smoke gate); workspace-only, PyAutoFit defects file as their own bug prompts |
| 2 | Scatter-collapse cure or caveat | `bug/autofit/ep_scale_collapse_basin_cure_or_caveat.md` | filed earlier; 2026-08-19 levers added (thorough hierarchical-factor sampler, TruncatedGaussian zero-boundary test); leg 1 guard shipped (#1465) |
| 3 | Graphical (non-EP) JAX scaling | → PyAutoCortex `phases/slope_hierarchy/n25_scale_up.md` (phase 1 of project `slope_hierarchy`; carries the measurement addendum) and `graphical_scoping.md` sub-tasks | **moved to the Cortex 2026-09-01** (was `research/graphical_ep/slope_hierarchy_n25_scale_up.md`); Cortex state `planned` |
| 4 | IC50 EP end-to-end + scale ladder | → PyAutoCortex `phases/ic50_workspace/ep_scale_up.md` (phase 1 of project `ic50_workspace`; dev companion stays in the Mind as `feature/autofit/ep_lbfgs_jax.md`) | **moved to the Cortex 2026-09-01** (was `research/graphical_ep/ic50_ep_scale_up.md`); Cortex state `planned` |
| 5 | Diagnostics sufficiency checkpoint | no prompt yet — deliberate | judge after phases 2 & 4 produce real runs; the 2026-07 diagnostics wave (#1330/#1335) shipped and caught #1383; graphical_scoping sub-tasks 5–6 (summary JSON, dashboard) are the likely follow-ups |
| 6 | Profiling: autofit_profiling repo + two epics | `research/autofit/autofit_profiling_bootstrap.md` | filed; repo creation human-gated |

Adjacent live work this campaign leans on but does not own: priors/messages
phase 4 (`bug/priors/` tracker — design #1500, findings #1498/#1501) and the
slope_hierarchy methods write-up
(`research/graphical_ep/slope_hierarchy_methods_writeup.md`).

## Sequencing

Phase 1 first (cheap, unblocks 2, referees everything). Phase 2 resumes from
its banked evidence once 1 gives the analytic upper limit. Phase 3 runs in
parallel (different machine profile — RAL). Phase 4 after 1–2 establish
trust. Phase 6 epic 1 (general profiling) can start any time; epic 2 (EP
profiling) last, once end-to-end runs exist to profile.

## Deferred — check-in gates, not scoped work

- **JAX/gradient/Hessian EP internals** — against changing EP internals while
  end-to-end models are the goal; adopt only if a genuinely simple change
  dramatically simplifies/speeds things. (`feature/autofit/ep_lbfgs_jax.md`
  covers the *factor-fit sampler*, which is allowed; this gate is about the
  EP update maths itself.)
- **Sampler-result reuse across EP passes** — complicated for efficiency-only
  gains; revisit via profiling epic 2 evidence (ep_scoping sub-task 6).
- **Parallel factor updates on HPC** — revisit when scaled runs approach
  multi-day wall times (ep_scoping sub-task 5 holds the sketch).
- **Multi-dataset factors (EP/graphical middle ground)** — revisit once
  scaling has hit whichever wall (memory or wall-time) shows up first.
