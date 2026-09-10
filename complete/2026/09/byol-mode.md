# byol-mode — "Bring Your Own Likelihood (BYOL)" mode + PyAutoFit docs headings

- Issue: https://github.com/PyAutoLabs/autofit_assistant/issues/40 (closed)
- PRs: PyAutoLabs/PyAutoFit#1604 (merged 1b7c1c992, docs only) → PyAutoLabs/autofit_assistant#41 (merged a29fdd289)
- Branch: feature/byol-mode on both repos, worktree ~/Code/PyAutoLabs-wt/byol-mode
- pending-release: PyAutoFit@https://github.com/PyAutoLabs/PyAutoFit/pull/1604
- Heart at ship: YELLOW, acknowledged in-session (same five organism-scope reasons as start-here-mode); freeze clear at merge.
- Parent: complete/2026/09/start-here-mode.md (the sibling mode; same shape)

## What shipped

**autofit_assistant#41.** `modes/byol.md` (303 lines): the published "Set up PyAutoFit with my
existing science project" prompt run as six stages, one per turn, taken from the prompt's own
sentences — overview of the code and what it scores (calling convention, log-likelihood vs
chi-squared, free vs fixed, data and cuts) → model with priors chosen with the user → the
`Analysis` wrapper importing their code unchanged, `af_wrap_likelihood`'s three validation
checks and the data-inspection gate → search recommendation with the reason and the JAX triage
question → a go-ahead table where nothing runs until they say go → the fit with the
output-folder tour, plots, aggregator reload and residuals as the check. Ask-anything /
teacher-mode footer on every stage; "you bring the likelihood, the assistant brings the
inference". `AGENTS.md`: fourth mode bullet and the trigger beside start here (BYOL wins when
both fire and code is pointed at). `README.md`: "### Bring Your Own Likelihood (BYOL)" at the
end of "Your own project" (P2, Setup step 3 and Getting Started point at it); prompt text
unchanged and byte-identical to the mode.

**PyAutoFit#1604.** `README.md` and `docs/overview/quick_start.md` sections retitled "Bring Your
Own Likelihood (BYOL)" with one paragraph linking the prompt to the mode;
`docs/overview/natural_language.md` "use my existing likelihood code" pointer names the mode.
Sphinx warnings 30 == baseline; no in-repo anchor referenced the old heading.

## Witness

Met: `modes/byol.md` exists; `AGENTS.md` routes the published BYOL prompt to it; the mode runs
the prompt's contract (overview → model → search → stop until go-ahead → run → results on disk)
one stage per turn with the footer; all three surfaces carrying the prompt are titled "Bring
Your Own Likelihood (BYOL)" and say the prompt launches BYOL mode. Dry run (gitignored
`scripts/scratch/byol_demo/`): stand-in user module over `dataset/sne_cosmology/` (1371 SNe,
`-0.5·χ²` without the noise constant); wrapper equals the user's function at a hand-built
instance (−295.1774), bad instance −1726.64, 0.19 ms/call; `DynestyStatic(nlive=75)` 11.4 s /
3686 evaluations: Ωm 0.344 +0.021/−0.019, H0 73.11 +0.27/−0.30 (README validation 0.344 /
73.14), log Z −302.40; aggregator reload returns the same medians.

## Decisions and findings

- A `### BYOL` sub-heading placed inside P2 swallowed P3–P6 in the rendered README; moved to the
  end of "Your own project" with a P2 pointer.
- No skill gap: `af_wrap_likelihood`'s Ask / Branch / validate / JAX triage / Combine mapped onto
  the prompt's stages without extension.
- The local `test_aggregate_csv.py` failures seen during start-here-mode were the
  .completed-zip sibling-dir shadow bug, fixed on main by PyAutoFit d6fa9cdc8 (#1602) the same
  afternoon; the bug prompt filed for them was retired by that task's close-out. This ship's
  full suite: 2567 passed.

## Original prompt

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
