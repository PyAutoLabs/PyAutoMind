# start-here-mode — autofit_assistant "start here" mode + PyAutoFit docs link

- Issue: https://github.com/PyAutoLabs/autofit_assistant/issues/38 (closed)
- PRs: PyAutoLabs/PyAutoFit#1603 (merged 008eaa472, docs only) → PyAutoLabs/autofit_assistant#39 (merged 057a13b9d)
- Branch: feature/start-here-mode on both repos, worktree ~/Code/PyAutoLabs-wt/start-here-mode
- pending-release: PyAutoFit@https://github.com/PyAutoLabs/PyAutoFit/pull/1603
- Heart at ship: YELLOW, acknowledged in-session (organism-scope reasons: autolens workspace validation, MGE profiling drift, no release rehearsal); freeze clear at merge.

## What shipped

**autofit_assistant#39.** `modes/start_here.md` (458 lines): turn-0 intro (what PyAutoFit
is, `dataset/gaussian_x1/` truth values, the Gaussian equation, data plot, one depth question,
then the step-1 prompt and stop); Part 1 — the six RTD Natural Language Inference sections one
step per turn, each explain → the page's prompt verbatim → run through the existing skill and
show the real output → try a variation → check-in; Part 2 — the same six steps on the user's
own science (paper or plain description → model → likelihood with the data-inspection gate →
search → explicit go-ahead → fit and results → `start-new-project` offered → extensions) with
`af_adapt_to_domain` as the engine; a fixed "ask anything / say teacher mode" footer on every
step of both parts, questions never advancing the step. `AGENTS.md` registers the mode and the
selection rule (start-here prompt outranks opening-request inference; `.maintainer` outranks
all). `README.md` restructured: Getting Started → Setting up → The tour, step by step → Your
own project → Teacher mode and HowToFit → License, every prompt blockquote unchanged, the
`model.info` block in lockstep with the RTD page. `docs/setup/{claude_code,codex_cli}.md`: the
tour takes questions at every step. `scripts/start_here/` — nine workspace-style scripts (the
dry run): peak-normalised `gaussian.py` + `analysis.py`, steps 1–6, Nautilus variant.

**PyAutoFit#1603.** `docs/overview/quick_start.md` and `natural_language.md` say the
start-here prompt launches the guided mode; the page's `model.info` block regenerated from a
real compose step (ids 0–2, the page's priors); the dangling `[Find 1D example …]` placeholder
removed. Sphinx warnings 30 == baseline.

## Witness

Met: `modes/start_here.md` exists; `AGENTS.md` routes the published start-here prompt to it;
the mode walks all six Contents sections in order, hands over each page prompt verbatim (11
blockquotes grep byte-identical in `natural_language.md`), shows the result and invites a
variation; README and both RTD pages link the prompt to the mode. Dry run: step 4 recovers
50.00 ± 0.28 / 24.89 +0.67−0.58 / 9.82 +0.28−0.26 (truth 50/25/10) in 16 s; step 5 reloads
without re-fitting; Nautilus three-Gaussian lnZ −60.23 vs −49.41 (Occam prefers x1); Part 2 on
`dataset/sne_cosmology/` recovers Ωm 0.343, H0 73.13 in 14 s.

## Decisions and findings

- `af.ex.Gaussian` is area-normalised; the bundled data and the RTD equation are peak-normalised
  (χ² 73 vs 2566 at truth). The tour defines its own `Gaussian`; the mode says so in one line.
- Three Gaussians + ascending-centre assertion starves Dynesty (0.21 % efficiency, dlogz 339 after
  30 min); the mode warns before launching, offers Nautilus (147 s) as the same-interface swap,
  quotes evidence only from finished runs.
- Local WSL gate: 5 pre-existing `test_aggregate_csv.py` failures on untouched main, CI green →
  filed `draft/bug/autofit/aggregate_csv_tests_fail_locally_pass_in_ci.md`.
- Skill gap: nothing owns loading the user's data + selection cuts → filed
  `draft/feature/autofit_assistant/data_loading_and_selection_cuts_skill.md`.
- Open on the RTD page: "Define the likelihood" still describes a random-draw fit image and shows
  none (the existing `toy_model_fit.png` is a best fit, not a random draw).
- Another session pushed PyAutoFit docs to main concurrently (statistical_methods rewrite,
  nl-prompt containers); the docs branch was rebased before ship.

## Original prompt

# autofit_assistant: a "start here" mode that walks a new user through the six natural-language tasks

Type: feature
Target: autofit_assistant
Repos:
- autofit_assistant
- PyAutoFit
Themes:
- assistants
- docs
Difficulty: medium
Autonomy: safe
Priority: high
Consequence: notify
Witness: `modes/start_here.md` exists and `AGENTS.md` mode selection routes the README / RTD "start here" prompt (`Begin the "start here" guide for a new user.`) to it; the mode walks all six Contents sections of the RTD Natural Language Inference page in order (Compose the Model, Define the Likelihood, Searches, Model Fit and Results, Saving and Loading, Scientific Workflows), each step hands the user the page's own prompt to type, shows the result (e.g. `model.info`) and invites a variation before moving on; README.md and `PyAutoFit/docs/overview/natural_language.md` say the start-here prompt launches this guided mode.
Filed: 2026-09-10
Issued: 2026-09-10

## Original request (verbatim)

> I then want us to add to the autofit_assistant a "start_here" mode which literally does all the above setups,
> guiding the new user through them. E.g. if the user writes start here, the assistant explains the 1D gaussian and
> tells them to input the prompt on the 3 Gaussian model showing them model.info, and then ecnourages them to describe
> the mdoel differently (e.g. make it two Guassians). It should do this for all 6 of the tasks described above.
>
> This is the prompt which users see on the PYAutoFit README.md and ohter pages, which this mode
> should be linked to and initiate. IT should give them a proper intro and stpe by step, following
> the natural language guide on the RTD.
>
> I want to perform scientific inference with PyAutoFit (https://github.com/PyAutoLabs/PyAutoFit) and the
> autofit_assistant (https://github.com/PyAutoLabs/autofit_assistant).
>
> Begin the "start here" guide for a new user.

## Context

"The above setups" / "the 6 tasks" are the six **Contents** sections of
@PyAutoFit/docs/overview/natural_language.md (mirrored in
@autofit_assistant/README.md "Using PyAutoFit Assistant"): model → likelihood →
search → fit/results → save/load → scientific workflows. The RTD page already
carries a ready-to-type prompt for each; the mode reuses those prompts verbatim
rather than inventing new ones.

The "start here" prompt is already published (PyAutoFit README, RTD Quick
Start, assistant README top) but nothing in the assistant catches it: the
assistant has only `modes/teacher.md` and `modes/assistant.md`, selected in
@autofit_assistant/AGENTS.md "Modes".

## Scope

- @autofit_assistant/modes/start_here.md — a third mode, a guided tour: a proper
  intro (what PyAutoFit is, what the bundled `dataset/gaussian_x1/` is, the 1D
  Gaussian equation and its three parameters), then the six steps in RTD order.
  Each step: explain the concept in a few sentences, hand the user the RTD
  page's prompt for that step to type themselves, run it when they do (showing
  the concrete output — `model.info` for step 1, the fit-vs-data image for step
  2, the search list for step 3, the parameter table + plot for step 4, the
  output folder tour for step 5), then invite a variation ("now describe the
  model differently — e.g. two Gaussians", a different prior, a different
  search) before moving on. Step 6 covers the page's three scientific-workflow
  extensions (three Gaussians + evidence comparison, sampler comparison,
  investigate a saved result) and hands off to Bring Your Own Likelihood /
  domain adaptation, Teacher mode and the Scientific Workflow page.
- @autofit_assistant/AGENTS.md — register the mode in "Modes" and the selection
  rule: the start-here prompt (or "start here" / "start_here") selects it; it
  is a guided-onboarding posture that composes with the existing safety
  invariants and skills (`af_compose_model`, `af_run_search`, ...); it steps
  down into assistant/teacher mode when the tour ends.
- @autofit_assistant/README.md — say under the starting prompt that it launches
  the guided "start here" mode and what the six steps are; keep the prompt text
  identical to PyAutoFit's.
- @PyAutoFit/docs/overview/natural_language.md and
  @PyAutoFit/docs/overview/quick_start.md — one sentence linking the start-here
  prompt to the assistant's guided mode (the README/RTD mirror commits show
  these three surfaces are kept in lockstep).

## Notes

- Interpretation: "the prompt on the 3 Gaussian model showing them model.info"
  is read as the step-1 compose prompt (the three-parameter Gaussian whose
  `model.info` the page prints); the three-*component* Gaussian is step 6's
  first extension. Confirm during planning.
- Do not duplicate the RTD prose into the mode file; the mode carries the tour
  logic and points at the page's prompts. Prompts quoted in the mode must match
  the RTD page word for word so the three surfaces stay in lockstep.

## Follow-up requests (verbatim, same session)

> Follow up details: The assistant should then, if it does not already, do a step-by-step guide for a new user to set up inference on
> their own project. IT shiould begin with paper ingestion or just a description of the science they are doing,
> then model composition, definining a likelihood function, picking a search and so on. The point is users should
> ultimately be able to use just natural language to describe everything and then get it going. The autofit_assistant
> GitHub README.md page is prob gonna need a lot of updating to be more in line with the goal here, which is
> reallly to have users run these tasks and then "get it".

> The notion of teacher mode and users asking questions to clarify things should be evident throughout.

Scope additions: Part 2 of the mode replays the six steps on the user's own science
(paper or plain description → model → likelihood → search → fit → results → organise),
composing `af_adapt_to_domain`, `af_ingest_paper`, `af_wrap_likelihood`,
`af_compose_model`, `af_configure_search`, `af_run_search`, `start-new-project`; every
step carries a fixed "ask anything / say teacher mode" footer; README restructured around
the tour (Getting Started → Setup → The tour step by step → Your own project → Teacher
mode & HowToFit → License), prompt text unchanged.
