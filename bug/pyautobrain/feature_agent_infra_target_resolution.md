Feature Agent misclassifies PyAutoBrain-infra prompts as research-first.

## Symptom

`bin/pyauto-brain feature feature/pyautobrain/bug_agent.md` returned
`Recommended workflow: research [re-home as research/]` and `Phase decision:
research-first` for a well-scoped PyAutoBrain-infra task (implementing the Bug
Agent). The same misfire applies to the already-shipped
`feature/pyautobrain/{feature,build,health}.md` prompts.

## Root cause

`_feature.py` resolves affected repos from `@RepoName` mentions against
`LIBRARY_REPOS` / `WORKSPACE_REPOS`. PyAutoBrain-infra work names no library or
workspace repo, so `repos` is empty; `recommend_workflow` then falls through to
`research` and `phase_decision` to `research-first`. The organs themselves
(PyAutoBrain / PyAutoHeart / PyAutoBuild / PyAutoMind / PyAutoMemory) are neither
library nor workspace, so there is no target class for them.

## Fix (small, in @PyAutoBrain)

Teach the Feature Agent an **infrastructure** target class, mirroring the Bug
Agent's `INFRA_TARGETS` map in `agents/conductors/bug/_bug.py`:

- add an `INFRA_TARGETS` (or `INFRA_REPOS`) set to `_feature.py`;
- when the prompt's `target` (second folder, e.g. `pyautobrain`) or an `@`-mention
  resolves to an organ, classify the workflow as `infrastructure` and skip the
  `research-first` fallback;
- `feature/pyautobrain/*` prompts should plan `direct` (or phased on genuine size),
  not re-home to research.

Consider factoring the shared `INFRA_TARGETS` map into one place both agents import
(the Bug Agent already imports `_feature`), so the two cannot drift.

## Validation

`bin/pyauto-brain feature feature/pyautobrain/bug_agent.md` (from `issued/`, or an
equivalent infra prompt) classifies as `infrastructure` / `direct`, not
`research` / `research-first`. The four `feature/pyautobrain/*` prompts all
classify sensibly.

## Provenance

Found while shipping the Bug Agent (PyAutoBrain#18); the misfire was overridden by
hand during that task.
