# Audit and improve autolens_assistant as the reference assistant

Type: feature
Target: autolens_assistant
Difficulty: medium
Autonomy: supervised
Priority: high
Status: formalised

Goal: audit and improve autolens_assistant as the reference implementation of a
PyAuto domain assistant.

**Scope for the first pass:** the audit report plus README/AGENTS.md cleanup
only. Skill-stub completion and larger structural changes are deferred to a
second PR.

## Context

autolens_assistant is intended to be an AI assistant for PyAutoLens science. It
combines:

- repository-level agent instructions;
- Teacher / Assistant / Agent interaction modes;
- procedural skills;
- core, literature and project wiki material;
- science-project scaffolding;
- safety rules for real data, source editing, API drift, generated scripts and
  git history.

Review the repository deeply and improve it where useful, but keep the scope
controlled. The aim is not a rewrite. The aim is to make autolens_assistant
clearer, more robust, more internally consistent, and easier to use as the
canonical pattern for future PyAuto assistants.

## Important design constraints

- Treat AGENTS.md as the canonical agent-agnostic source of truth.
- Do not create parallel duplicated instruction files that will drift.
- Teacher mode is definitely important — preserve it. The Assistant / Agent
  split is up for assessment (see "Interaction modes" below); do not treat the
  three-mode model as fixed.
- Preserve the safety invariants, especially:
  - inspect real data before fitting;
  - never write into output/ or sources/;
  - keep wiki/core/ read-only except through the update workflow;
  - do not edit PyAuto source code in normal user sessions;
  - never rewrite git history.
- Keep the assistant practical and user-facing. It should help a scientist get
  work done, not become an over-engineered meta-framework.
- Prefer small, reviewable improvements over broad rewrites.
- Do not break existing skill names or expected workflows.

## Audit areas

### Interaction modes (explicit design question)

Assess whether Assistant mode and Agent mode should remain distinct. The
working hypothesis: **merge them into a single Assistant mode** that adapts
its planning depth, amount of conversation and autonomy to the user's request
— defaulting to more conversational, and only running autonomously when the
user asks for it. Teacher mode stays as a distinct mode. If the audit
supports the merge, propose the reworded mode model (README + AGENTS.md) as
part of this PR; if there is a strong reason to keep the split, say why.

### Onboarding and README

- Is the README clear for a new user?
- Is the distinction between the assistant repo and a separate science project
  clear?
- Are the examples still the right three examples?
- Are Teacher / Assistant / Agent modes explained in a way a user will
  understand?

### Agent instructions

- Is AGENTS.md concise enough for coding agents while still complete?
- Are the session-start steps sensible?
- Are the safety invariants clear and non-contradictory?
- Are maintainer mode, user profile, mode selection and source-of-truth
  resolution well defined?
- Are there any instructions likely to confuse Claude Code, Codex, Gemini,
  OpenCode or Copilot?

### Skills

- Audit skills/README.md and the individual skills.
- Identify which skills are mature, which are stubs, and which are missing.
- Improve the most important high-leverage skill documentation first.
- Do not try to fill every pending stub in one PR.
- If you choose a stub to complete, pick one with clear value and limited
  scope. (First pass: identify and label only — completion is a second PR.)

### Wiki

- Check whether the wiki/core/, wiki/literature/ and wiki/project/ split is
  explained clearly.
- Check whether wiki references from skills are discoverable and not stale.
- Do not rewrite large scientific content unless necessary.
- Flag places where the wiki is missing obvious assistant-critical concepts.

### Project lifecycle

- Review start-new-project and related project workflow material.
- Check whether the assistant clearly separates:
  - the assistant's own skills/wiki/tooling;
  - a user's science project data/scripts/results/journal;
  - PyAutoLens source code.
- Improve wording or structure if this boundary is unclear.

### Assistant-as-template

- While reviewing, think ahead: this repo may become the template for future
  assistants such as autofit_assistant, autogalaxy_assistant, or
  autoarray_assistant.
- Identify which parts are genuinely PyAutoLens-specific and which are generic
  assistant infrastructure.
- Do not prematurely generalise the codebase, but leave clear notes about what
  would need abstraction later.

## Deliverables

- A short audit report in the PR body covering: what was inspected; what was
  changed; what was deliberately not changed; the most important follow-up
  work.
- A focused PR that improves the repo. First-pass candidates:
  - clearer README onboarding;
  - cleaner mode explanation;
  - improved AGENTS.md structure;
  - better skill index / maturity labels;
  - clearer documentation of the assistant repo vs science project boundary;
  - notes preparing the repo to serve as a future assistant template.
- Deferred to a second PR: upgrading a high-value skill stub from TODO
  scaffold to usable recipe.

The Clone Agent / Mitosis Agent design (a future PyAutoBrain agent that
generates new assistants modelled on autolens_assistant) is filed as a
separate prompt under PyAutoBrain — do not implement it here.

## Validation

- Run any available tests or lint/check scripts in the repo.
- Check markdown links where practical.
- Check that any edited instructions remain internally consistent.
- If there is a line-count or skill-format guard, run it.
- Do not push directly to main. Create a branch named something like
  feature/autolens-assistant-audit and open a draft PR with a clear summary.

<!-- formalised by the Intake (Conception) Agent on 2026-07-08 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/3690563e-5959-43ff-b131-b00fe70bd60c/scratchpad/intake_1_assistant_audit.md -->
