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
