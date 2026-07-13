## shareable-science-projects
- issue: https://github.com/PyAutoLabs/autolens_assistant/issues/45 (closed)
- pr: https://github.com/PyAutoLabs/autolens_assistant/pull/46 (merged 2ceedf4, squash)
- completed: 2026-07-10
- summary: docs emphasis pass, head of the autolens_assistant batch — generated-project README.md template added to the start-new-project Create scaffold (reproduce / continue-this-work via assistant refer-back / data-availability placeholder / citation; closes the gap where the Publish gate referenced a README Create never generated); Collaborate opens built-to-be-shared + a collaborator's fork-and-continue first session; Publish framed as the paper's open-source companion; top-level README "Built to be shared" pitch + share/publish example prompts; skill description gains continue-a-collaborator's-project + open-source-paper triggers. Citations check clean (388, 0 missing). Absorbed science_project_collaborator_clone.
- followups: batch queue continues sequenced — science_project_api_gate → per_project_literature (core hybrid) → script_to_notebook → live_visual_update_context → portable_user_defaults (discovery-half); stub_skill_recipes stays open (rolling queue, NOT done)

## Original prompt

# Shareable science projects — fork/clone-and-continue + open-source-your-paper emphasis

Type: docs
Target: autolens_assistant
Difficulty: medium
Autonomy: supervised
Priority: high
Status: formalised

A science project created by `start-new-project` already becomes its own git/GitHub repo with
a Create → Work → Collaborate → Publish lifecycle, a paper-hardening Publish gate, Zenodo/DOI
minting and CITATION.cff. What is missing is the **user-facing emphasis**: the design should
make sharing the default expectation, and pitch the project repo as the natural open-source
companion to a paper.

Three surfaces (all verified against the current repo state):

1. **Generated project `README.md` template — currently missing.** The Create scaffold in
   `@autolens_assistant/skills/start-new-project.md` generates no `README.md`, yet the Publish
   gate references one (data-availability statement). Add a README template to the Create
   scaffold that says, near the top:
   - this repo runs **standalone** for reproducing the analysis (env via `activate.sh`, code
     in `scripts/`, provenance in `results/manifests/`);
   - **fork or clone it and continue the work**: point your own `autolens_assistant` at it
     (`$AUTOLENS_ASSISTANT` → sibling → clone-on-demand, already implemented) — see `AGENTS.md`;
   - a placeholder data-availability section the Publish gate later fills in.
   This absorbs `docs/autolens_assistant/science_project_collaborator_clone.md` (its
   assistant-ref dependency is settled; that prompt is retired into this one).

2. **`start-new-project.md` Collaborate phase.** Actively encourage sharing, and spell out the
   fork-and-continue flow for a collaborator arriving at a cloned/forked project with their own
   assistant: what they get (skills + wiki via refer-back, the API code-gate, the journal), and
   what their first session looks like.

3. **`autolens_assistant` top-level `README.md`.** User-facing pitch: a science project is a
   wonderful way to **open-source the whole project behind a paper** — data (or its
   availability statement), results, and every python script — with the existing Publish
   gate / Zenodo / CITATION.cff machinery as the substance. Agentic-AI framing is first-class
   (per the user-docs framing rule); no llms.txt mechanics.

Keep the generated README short — the detail lives in the project's thin `AGENTS.md` and the
skill itself. The repo is a generic public template: no personal content.

## Original request

> I want it so that with autolens assistant a user can basically make a science project which
> becomes its own github repo, and then they should be encouraged to be able to easily share
> that project and another friend could come in, fork or clone it and cotinue the work with
> their own autolens assistant. Emphassie this aspect in the autolens_assistant design. Also
> make it clear this would be a wonderful way to put up the open-source repo that goes with a
> paper, so make sure autolens_assistant has user-facing aspects which make it clear its great
> for open sourceing a whole project (data, results, all python scripts).

<!-- formalised by the Intake (Conception) Agent on 2026-07-10 from user-intake; re-homed and
     expanded from triage/ by the routing session (verified scope, user-approved) -->
