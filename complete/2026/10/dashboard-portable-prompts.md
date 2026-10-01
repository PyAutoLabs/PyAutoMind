# Dashboard prompts portable across assistants

Completed: 2026-10-01
Issue: https://github.com/PyAutoLabs/PyAutoHeart/issues/257

## Delivered
All dashboard AI copy actions use explicit skill prose: Heart repair/timing prompts, Brain and Mind task/maintenance actions, Cortex science actions, Eyes figure reviews, Memory, Hands and the overview board. Converted legacy cached prompts while preserving shell commands, arguments, paths and safety gates. Nerves audited and already portable.

Regenerated Mind/Cortex/Eyes artifacts. Final Eyes refresh uses published manifests to match CI; survey/critique context preserved.

## Validation and merge evidence
896 relevant local tests passed; independent review CLEAN. Eyes final repair: 77 tests, Ruff/format, live 265-figure URL check and all manifest/state checks passed. Every configured exact-head CI run and job passed before merge. Gut and Scientist have no PR CI; human explicitly approved merges based on 16 and 8 passed local tests. Every claimed worktree head proven ancestor of origin/main and every PR confirmed MERGED.

## Authorization
User: "yes you may commit push open prs and merge once CI is green"; later "yes I approve run prm" and final explicit prm. Development-only Heart RED override recorded in all four required sinks. Current shipping RED reason: `release validation FAILED (stage integrate)`; earlier workspace-validation timeout cleared. No release authorization or check bypass.

## Merged PRs
- https://github.com/PyAutoLabs/PyAutoBrain/pull/436
- https://github.com/PyAutoLabs/PyAutoHeart/pull/259
- https://github.com/PyAutoLabs/PyAutoHands/pull/293
- https://github.com/PyAutoLabs/PyAutoMemory/pull/113
- https://github.com/PyAutoLabs/PyAutoEyes/pull/10
- https://github.com/PyAutoLabs/PyAutoGut/pull/17
- https://github.com/PyAutoLabs/PyAutoScientist/pull/38
- https://github.com/PyAutoLabs/PyAutoCortex/pull/53

## Preservation
Canonical Cortex science-ledger edits untouched. Task worktrees contain only reproducible Python/test/lint caches, no irreplaceable data. No background monitoring or auto-merge armed.

## Original prompt

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
