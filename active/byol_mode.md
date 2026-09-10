# autofit_assistant: a "Bring Your Own Likelihood (BYOL)" mode analogous to start here

Type: feature
Target: autofit_assistant
Repos:
- autofit_assistant
- PyAutoFit
Themes:
- assistants
- docs
Difficulty: small
Autonomy: safe
Priority: high
Consequence: notify
Witness: `modes/byol.md` exists and `AGENTS.md` mode selection routes the published Bring Your Own Likelihood prompt ("Set up PyAutoFit with my existing science project …") to it; the mode runs the prompt's own contract — overview of the project and likelihood function → compose and explain a model → recommend a search → stop until the go-ahead → run → explain how results are written to disk and how to inspect them — one stage per turn with the ask-anything / teacher-mode footer; every surface that carries the prompt (PyAutoFit README, RTD Quick Start, assistant README) titles the section "Bring Your Own Likelihood (BYOL)" and says the prompt launches BYOL mode.
Filed: 2026-09-10
Issued: 2026-09-10
Parent: complete/2026/09/start-here-mode.md

## Original request (verbatim)

> Now add an analogous mode for these natural language prompts on the README.md and throughout the docs, maknig sure to put BYOL in the title in brackets and calling it byol mode or something so we can ply on BYOB Bring Your Own Likelihood
> Already have a likelihood function for your science problem? Point the assistant at your existing code and it can set it up with PyAutoFit — defining the model, choosing priors with you, configuring a search and organising the results:
>
> Set up PyAutoFit with my existing science project. An example likelihood function can be found at [GitHub link or local directory].
>
> First, give me an overview of my project and likelihood function. Compose an appropriate model, explain it to me, and recommend a non-linear search (for example MCMC, nested sampling or maximum-likelihood estimation).
>
> Do not begin inference until we have discussed the setup and I give you the go-ahead.
>
> Once inference is running, explain how the results are written to disk and show me how to inspect and interpret them with PyAutoFit.
>
> Your existing science code remains the source of the likelihood. With PyAutoFit built around it, you can perform inference through natural language while gaining access to features such as flexible priors and model composition, MCMC and nested sampling, automated result handling, model comparison and scalable workflows.

## Context

The start-here mode (`complete/2026/09/start-here-mode.md`, autofit_assistant#39) catches the
published start-here prompt. The second published prompt — Bring Your Own Likelihood, on
@PyAutoFit/README.md, @PyAutoFit/docs/overview/quick_start.md and @autofit_assistant/README.md
("Your own project", P2) — has no mode of its own; it lands in inferred assistant mode. The
engine already exists: `skills/af_wrap_likelihood.md` (wrap + validate), with
`af_compose_model`, `af_configure_search`, `af_run_search`, `af_load_results`.

## Scope

- @autofit_assistant/modes/byol.md — the mode, mirroring `modes/start_here.md`'s shape: trigger
  (the published BYOL prompt, or "byol" / "bring your own likelihood"), posture (their code is
  the source of the likelihood, never altered; nothing is fitted before the go-ahead), then the
  prompt's own contract as stages, one per turn: (1) overview of the project and the likelihood
  function (read the code, restate what it scores and its calling convention); (2) compose and
  explain a model with priors chosen with the user (`model.info`); (3) wrap into an `Analysis`
  and validate at hand-built instances against their function (`af_wrap_likelihood`), with the
  data-inspection gate; (4) recommend a search with the reason (`af_configure_search`); (5) the
  go-ahead checkpoint; (6) run, then explain how results are written to disk and how to inspect
  and interpret them (`af_run_search`, output-folder tour, `af_load_results`, `af_plot_fit`);
  hand-off to `start-new-project` and the scientific-workflow pages. The ask-anything /
  teacher-mode footer on every stage, as in start here.
- @autofit_assistant/AGENTS.md — register **BYOL** in "Modes" and the selection rule beside
  start here.
- @autofit_assistant/README.md, @PyAutoFit/README.md, @PyAutoFit/docs/overview/quick_start.md —
  retitle the section "Bring Your Own Likelihood (BYOL)", keep the prompt byte-identical, add one
  sentence that the prompt launches **BYOL mode** (link `modes/byol.md`), with the BYOB play
  ("bring your own likelihood — we supply the inference") where the register allows.
- `docs/setup/{claude_code,codex_cli}.md` — mention BYOL beside the start-here line if they
  reference the BYOL prompt.
