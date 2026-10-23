# A dedicated Documentation conductor in PyAutoBrain

Type: feature
Target: PyAutoBrain
Repos:
- PyAutoBrain
Difficulty: medium
Autonomy: supervised
Priority: medium
Filed: 2026-10-23
Status: formalised
Consequence: judge

@PyAutoBrain

## Context

`skills/docs/docs.md` says `/docs` is only a work-type entry ("No dedicated Documentation conductor exists yet …
Follow-up: promote to a dedicated Documentation conductor"). On 2026-10-23 the human approved a human-first rewrite
of the autolens_assistant README and asked for the style to become "the go to style and agent or writing thing for
GitHub README.md pages and probably more RTD pages". The style shipped as `skills/WRITING_STYLE.md`; this task gives
it an owner.

## Ask

Promote `/docs` to a Documentation conductor under `agents/conductors/docs/` that:

- classifies a docs request by surface (GitHub README, setup/how-to page, Read the Docs page, tutorial narrative,
  agent-facing file) and applies `skills/WRITING_STYLE.md` to the people-facing ones;
- emits a decision (target repo, surface, page template from the style guide, pages to move long material to,
  cross-repo siblings to keep in step — e.g. the four assistant READMEs) that `start_dev` consumes, like the
  Workspace conductor's `WorkspaceDecision`;
- can run a read-only audit mode: score a page against the style guide's checklist and list concrete fixes;
- defers tutorial science prose to the Workspace conductor's `howto`/`workspace` registers rather than duplicating
  them.

## Done when

`pyauto-brain docs <prompt>` returns a decision, `/docs` routes through it, the audit mode reports on a README, and
the board lists the conductor.

## Original request (verbatim, 2026-10-23)

> This was a brilliant rewrite and I am very happy with the tone and style, can we put this somewhere (PyAutoBrain?)
> as the go to style and agent or writing thing for GitHub README.md pages and probably more RTD pages?

> 1. do it
