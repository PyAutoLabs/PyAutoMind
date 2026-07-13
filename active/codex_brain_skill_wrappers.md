# Add Codex discovery for every PyAutoBrain agent

Type: maintenance
Target: PyAutoBrain
Repos:
- @PyAutoBrain
Difficulty: medium
Autonomy: safe
Priority: normal
Status: formalised

## Original request

> yes, make SKILL.md wrappers for PyAutoBrain and any other repos you see a Claude bias

## Scope

Add thin Codex `SKILL.md` wrappers for every public agent exposed by
`bin/pyauto-brain` and for existing Brain command/workflow surfaces. Keep the
existing command Markdown and deterministic agent entrypoints canonical.

Update `bin/install.sh` so a directory containing both `SKILL.md` and
`<name>.md` installs both surfaces for Claude while installing the skill into
Codex. Add isolated tests for dual-harness installation and remove
Claude-specific assumptions from shared Brain workflow prose.

## Acceptance criteria

- Every public `pyauto-brain` conductor and faculty has a discoverable skill.
- Existing Claude commands remain installed when a wrapper is present.
- Existing and new skills install into both Claude and Codex skill roots.
- Tests use temporary destinations and do not modify live agent configuration.
- Skill metadata, links, shell syntax, and line-count checks pass.
