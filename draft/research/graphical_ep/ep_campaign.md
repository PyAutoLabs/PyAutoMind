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
| 1 | Analytic Gaussian benchmark (the keystone — start here) | `active/analytic_gaussian_benchmark.md` | **implemented 2026-09-02, PR pending** — autofit_workspace_test#91, branch `feature/analytic-gaussian-benchmark` (`scripts/graphical/analytic_*.py`). Verdict: closed form, minimal EP and the graphical joint fit agree everywhere; **every failing cell is autofit's EP column, including the exactly Gaussian leg A**. Six PyAutoFit mechanisms root-caused and filed (see Findings below); the autofit-parity scripts are parked NEEDS_FIX until they land, the closed-form reference + minimal EP are curated into the smoke gate |
| 2 | Scatter-collapse cure or caveat | `bug/autofit/ep_scale_collapse_basin_cure_or_caveat.md` | filed earlier; leg 1 guard shipped (#1465); **mechanism found by phase 1 (2026-09-02)**: the Laplace projection never contains the factor curvature and a failed line search still projects (`bug/autofit/ep_laplace_covariance_and_failed_update_projection.md`), truncation limits are dropped by natural-parameter ops (`bug/autofit/ep_message_support_and_transform_lost_in_projection.md`); the minimal EP shows a mode-based projection of σ is intrinsically collapse-prone (tilted density ∝ 1/σ at x_i = mu) — the *caveat* half is now writable, the *cure* is moment matching or a log-σ parameterisation. Analytic upper limit banked: seed-0 `sigma_q95 = 12.18` (truncated(10,5,0,100), N=5) |
| 3 | Graphical (non-EP) JAX scaling | → PyAutoCortex `phases/slope_hierarchy/n25_scale_up.md` (phase 1 of project `slope_hierarchy`; carries the measurement addendum) and `graphical_scoping.md` sub-tasks | **moved to the Cortex 2026-09-01** (was `research/graphical_ep/slope_hierarchy_n25_scale_up.md`); Cortex state `planned` |
| 4 | IC50 EP end-to-end + scale ladder | → PyAutoCortex `phases/ic50_workspace/ep_scale_up.md` (phase 1 of project `ic50_workspace`; dev companion stays in the Mind as `feature/autofit/ep_lbfgs_jax.md`) | **moved to the Cortex 2026-09-01** (was `research/graphical_ep/ic50_ep_scale_up.md`); Cortex state `planned` |
| 5 | Diagnostics sufficiency checkpoint | no prompt yet — deliberate | judge after phases 2 & 4 produce real runs; the 2026-07 diagnostics wave (#1330/#1335) shipped and caught #1383; graphical_scoping sub-tasks 5–6 (summary JSON, dashboard) are the likely follow-ups |
| 6 | Profiling: autofit_profiling repo + two epics | `research/autofit/autofit_profiling_bootstrap.md` | filed; repo creation human-gated |

Adjacent live work this campaign leans on but does not own: priors/messages
phase 4 (`bug/priors/` tracker — design #1500, findings #1498/#1501) and the
slope_hierarchy methods write-up
(`research/graphical_ep/slope_hierarchy_methods_writeup.md`).

## Findings (phase 1, 2026-09-02)

The benchmark's referee verdict, from autofit_workspace_test#91 (evidence in
its two phase comments) and the read-only root-cause pass, recorded on
PyAutoFit#1405. Each mechanism is a Mind prompt under `draft/bug/autofit/`:

| # | Mechanism | Prompt | Size |
|---|-----------|--------|------|
| D1 | The first prior of a process (id 0) compares equal to the `FactorValue` sentinel, so every multi-variable factor gradient is corrupted; leg A `mu` stays at its start (50.00 ± 20.6 vs 50.86 ± 4.11) | `ep_prior_id_zero_collides_with_factor_value.md` | small, safe — **do first** |
| D2+D3 | Laplace "covariance" = mean-field precision + one non-accumulating random diagonal secant (no factor curvature; result depends on prior ids through sampling order); a failed line search still projects the start point and overwrites the message | `ep_laplace_covariance_and_failed_update_projection.md` | medium — the phase-2 mechanism |
| D4+D5 | Truncation limits dropped by `from_natural_parameters`/`__pow__` (leg B σ message returns limits (−inf, inf)); `TransformedMessage.from_mode` skips the Jacobian for scalar variables (log-σ leg never moves) | `ep_message_support_and_transform_lost_in_projection.md` | medium |
| D6 | `errors_at_sigma(as_instance=True)` crashes on a prior-valued global model | `samples_errors_at_sigma_instance_prior_valued_model.md` | small, safe |

Calibration facts to reuse: EP with a Gaussian site on σ is biased on this
model by construction (seeds 0–4 scatter row a ≤ 0.077, b ≤ 0.145 for the
minimal EP) — that is the analytic ceiling any autofit fix should be judged
against, not zero. Phase 5's diagnostics checkpoint gains a concrete item:
zero SUCCESS updates on a factor is a STALE result that no library warning
currently reports.

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
