# Make dashboard AI prompts portable across assistants

Type: bug
Issued: 2026-10-01
Issue: https://github.com/PyAutoLabs/PyAutoHeart/issues/257
Autonomy: safe

## Original request

I copied the "Fix Heart systematically" prompt from PyautoHeart dashboard but get this for codex, can we make its command (and any other dashboard commands) AI agnostic or have codex support dash? • Unrecognized command '/health'. Type "/" for a list of supported commands.

## Scope

@PyAutoHeart @PyAutoBrain: replace assistant-specific leading slash commands in copied dashboard AI prompts with explicit plain-language skill invocation. Audit dashboard prompt producers and shared copy rendering, including Mind dashboard generation. Preserve arguments, task paths, approval boundaries and shell-command payloads. Other dashboard owners discovered by the audit must be surveyed before edits.

## Acceptance

- Fix Heart systematically and other copied AI prompts are usable without a client-specific slash parser.
- Named skills remain explicit and resolvable; existing guardrails and command arguments remain intact.
- Shell snippets and filesystem paths are not rewritten as skill prompts.
- Focused rendering tests cover portable prompts and shell-command preservation; regenerate affected dashboard artifacts through their owning generators.

## Initial evidence and plan

Heart `heart/dashboard.py:build_fix_plan` starts its prompt with `/health`; multiple other payload producers do likewise. Brain owns shared dashboard code in `board/_theme.py`, `board/_board.py` and dashboard generators in its conductors.

Audit prompt producers, choose a shared conversion boundary where practical, update affected producers/renderers and tests, then regenerate artifacts and validate copied text. Plan approved 2026-10-01, including full dashboard coverage. Implemented in feature/dashboard-portable-prompts worktrees; tests and independent review passed. Awaiting explicit Heart RED development-shipping override for issue #257.
