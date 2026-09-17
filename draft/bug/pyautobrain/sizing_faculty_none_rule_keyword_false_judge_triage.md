# Sizing faculty: a `none` rule, keyword hits on prose that only describes a surface, and a `triage` rule

Type: bug
Target: pyautobrain
Repos:
- PyAutoBrain
Themes:
- mind-workflow
Difficulty: small
Autonomy: safe
Priority: normal
Status: draft
Consequence: glance
Witness: `estimate_consequence` on a prompt whose `Witness:` value starts with `none` returns `judge` with a reason naming the none (unit test); the 14 prompts named below derive the tier their declared override carries today without the override, or the keyword change is recorded as declined per prompt with its reason; a `draft/triage/` prompt derives `judge` with a reason naming triage (unit test); a whole-backlog regrade before and after is recorded in the PR, and no prompt's derived tier moves from a cheaper tier to `judge` except the six `Witness: none —` ones and the two triage ones.
Review-minutes: 3
Unattended: ready
Filed: 2026-09-17

Three defects in `agents/faculties/sizing/_sizing.py`, all found by the witness
campaign (PyAutoMind#398, record `complete/2026/09/witness-campaign.md`) while
grading 137 prompts through it. Derived `notify` (organ-internal repo) is
overridden to `glance` here on purpose: a rule change in this module regrades
every prompt on the dashboard, so the before/after regrade deserves a look. This prompt is itself the
finding in miniature: the faculty derives `judge` for it on "public api,
defaults to, raises " because the words appear below, quoted as the keywords
they are.

## 1. No `none` rule

`estimate_consequence` rule 3 is `if not witness: return "judge"`. The campaign's
`Witness: none — <reason>` form (the prompt's own "Done when" allows it) is a
non-empty string, so it is read as a witness and the prompt derives `glance` or
`notify`. Six prompts carry it today: `multiwavelength_inversion`,
`ep_analytic_updates`, `ep_lbfgs_jax`, `board_without_gh` (now archived),
`brain_board_follow_ups`, `model_figures_6b2_slam_stages`. Their declared
`judge` holds by precedence, so `dashboard.md` and the batch planner are right;
the derived reading, `sizing --json`, and any regrade that counts "witnessed"
are wrong. Fix: `declared_header` maps a value starting with `none` (case-
insensitive, optional `—`/`-` after it) to no witness, and rule 3's reason says
`Witness: none declared — <the reason>` so the disagreement report stays useful.

## 2. `JUDGE_SURFACE_KEYWORDS` hits on prose that describes a surface

The module's own "Known limit" paragraph predicts this; the campaign measured
it: **14 of 137 prompts** needed a declared-`glance` override because a keyword
appeared in prose *describing* the thing being fixed, not a surface the task
changes. `raises ` alone accounts for ten — every one a bug prompt whose title
or symptom section says "raises `IndexError`" about the crash it fixes:
`mapping_overlay_follow_ups` (autoarray), `assertion_repr_recurses_forever`,
`emcee_crashes` (since folded), `model_function_cannot_resolve_config_priors`,
`pyautofit_prior_model_summary_header`, `stale_enable_pytrees`,
`mcmc_thin_zero_and_check_size_short_chain` (autofit),
`drawer_pix_initializer_exception_flake` (euclid),
`point_source_json_datasets_record_no_regime` (pyautolens),
`mesh_geometry_areas_transformed` (autoarray). The other four: `witt_wynne_solver_library_home`
and `wiki_currency_check_version_gate` on "public api" (one names its deliverable's
API, the other names what a check hashes), `point_solver_profiling_cells` on
"defaults to" (a trap note about `plane_redshift`), `unregistered_worktrees` on
"reported by" (in its own witness). Inline code is already masked, which is why
"raises `IndexError`" trips but "`raises RayTracingException`" does not — the
same sentence grades differently depending on where the backticks fall.

Decide, do not guess, between: (a) dropping `raises ` from the list and relying
on the `error contract` phrase the list already carries; (b) matching `raises `
only when it is not followed by a masked code token (a described exception)
and not in the title line; (c) keeping the list and documenting the override as
the intended path (then this section is a no-op and the 14 overrides stand).
Whichever it is, the before/after regrade in the witness is the evidence.

## 3. No `triage` rule

`draft/triage/` prompts have no work-type rule anywhere in the faculty: they
derive `ready` and grade like any other prompt (two graded `glance` during the
campaign and were re-homed as bugs by hand). A prompt whose classification is
still open should derive `judge` with a reason naming triage, the same shape as
the `release`/`human_review` rule 1, and `estimate_unattended` should not call
it `ready`. Also seen: an unknown `Unattended:` value (`needs-decision`) is not
a grade the faculty knows and falls through to derived `ready`; either reject
it in `declared_header` or document the vocabulary.

<!-- filed 2026-09-17 at the witness campaign close-out (PyAutoMind#398), by hand: the intake agent's own header bugs (draft/bug/pyautobrain/intake_agent_silently_drops_unknown_type_values.md) are still open -->
