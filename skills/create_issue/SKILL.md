---
name: create-issue
description: Convert a PyAutoMind prompt file into a GitHub issue and register it — the Mind issue and registry primitive that start_dev delegates to.
---

Turn a `PyAutoMind/` prompt into a tracked GitHub issue and register it.

> **Which GitHub surface are you on?** This skill spells its GitHub steps as
> `gh` commands, which name the *operation*, not necessarily the command: a
> Claude Code remote session has no `gh` and reaches GitHub through the
> `mcp__github__*` tools instead. Probe once (`command -v gh`) and translate
> via `PyAutoBrain/skills/GITHUB_ACCESS.md`. Do not install `gh` to close the
> gap — that page records why an installed one still fails.

Mind owns the issue/registry write, prompt lifecycle move and push. Brain owns
classification and planning. When called by start-dev, use its supplied repo,
title, plan and branch verbatim; standalone, fill missing inputs with a light
pass. Deep triage and environment setup still go through start-dev.

Organ boundary and the execution-environment model: PyAutoBrain `skills/WORKFLOW.md`.

## Usage

```
$create-issue <prompt-file-path>    # /create_issue in Claude
```

Pass a path relative to the Mind checkout. Prompts live under
`draft/<work-type>/<target>/` (see REFERENCE.md "Prompt taxonomy");
pre-migration `<target>/<name>.md` paths still resolve. Examples:
`draft/bug/autofit/factor_graph_instance_iteration.md` and
`draft/feature/autoarray/oversampling.md`. The skill argument stays Mind-relative
in grouped and flat layouts. Use `PYAUTO_MIND` when the checkout is elsewhere.

From either workspace root, resolve the checkout once for the shell examples
below (an existing `PYAUTO_MIND` override takes precedence):

```bash
brain_dir="${PYAUTO_BRAIN:-$(test -d organs/PyAutoBrain && echo organs/PyAutoBrain || echo PyAutoBrain)}"
export PYAUTO_MIND="${PYAUTO_MIND:-$(python3 "$brain_dir/agents/_repo_paths.py" path PyAutoMind --root .)}"
```

## Inputs

These come from the **caller** (Brain/`$start-dev`) when delegated, or from a
**light standalone pass** here when run directly:

| Input | From caller | Standalone fallback |
|-------|-------------|---------------------|
| primary repo | Feature Agent classification | most-referenced `@RepoName` in the prompt; ask if ambiguous |
| title | caller | concise title (<70 chars), conventional prefix (`feat:`/`fix:`/`refactor:`/`docs:`/`perf:`) |
| plan (high + detailed) | caller | brief plan from a quick read of the prompt + referenced files |
| suggested branch | caller (`plan_branches`) | `feature/<short-desc>` kebab-case, <50 chars |

Resolve repository owners from `$PYAUTO_MIND/repos.yaml`; the generated summary
in `WORKFLOW.md` is the readable mapping. Do not reuse legacy owner defaults.

## Steps

### 0. Sync new prompt ideas (Mind)

```bash
source "$PYAUTO_MIND/scripts/prompt_sync.sh"
prompt_sync_new_prompts          # no-op if nothing untracked; else commits + pushes new ideas
```

### 1. Read the prompt

Read `<Mind checkout>/<argument>`. Resolve the checkout with `PYAUTO_MIND` when
set; otherwise use the existing Brain repository resolver for the active
workspace layout. If given an absolute path or a workspace-relative prefix
(`organs/PyAutoMind/` or `PyAutoMind/`), strip that resolved checkout prefix
exactly once; never prepend Mind twice. If missing, report and list prompts
in that folder.

### 2. Resolve the inputs

If the caller supplied repo/title/plan/branch, use them **verbatim**. Otherwise
do the light standalone pass from the Inputs table (don't run a full Brain
triage — that's `$start-dev`).

### 3. Assemble + create the issue

**If the prompt body carries an `Issue:` line, reuse that issue — skip creation** (a
Cortex-spawned gate ref, filed with its issue already open; see REFERENCE.md "A
Cortex-spawned dev follow-up gets its issue at filing"). Never open a second.

Build the body in this structure, then create it (present for review first):

```markdown
## Overview
<2-4 sentence summary of what this task is and why it matters>

## Plan
<high-level bullet plan — human readable, no code>

<details>
<summary>Detailed implementation plan</summary>

### Affected Repositories
- repo1 (primary)

### Branch Survey
| Repository | Current Branch | Dirty? |
|-----------|---------------|--------|
| ./RepoName | main | clean |

**Suggested branch:** `feature/<name>`

### Implementation Steps
1. <step with file paths>

### Key Files
- `path/to/file.py` — description
</details>

## Original Prompt
<details>
<summary>Click to expand starting prompt</summary>

<original prompt content copied verbatim>
</details>
```

```bash
gh issue create --repo <owner/repo> --title "<title>" --body "$(cat <<'ISSUE_EOF'
<body content>
ISSUE_EOF
)"
```

### 4. Register the task in active.md (Mind)

Add the task entry to `$PYAUTO_MIND/active.md` with the issue URL and today's
date (schema in [REFERENCE.md](../../REFERENCE.md) → "`active.md` schema"):

```markdown
## <task-name>
- issue: <issue-url>
- issued: <YYYY-MM-DD>
```

`issued:` is the date the issue was created — this step is the only moment
anyone knows it for certain, so write it now rather than leaving it to be
reconstructed later (`lifecycle.py dates --write` can only infer). It is what
the dashboard's "Recent" table reads.

**If the caller is handling registration itself** — e.g. `$start-dev` routing a
conflicted task to `planned.md` — skip this step and let it register (that
registry's date key is `filed:`).

### 5. Move the prompt to active/

The prompt advances from `draft/` (not started) to `active/` (issued, in
flight) — the second of the three lifecycle states (`draft/ → active/ →
complete/`; issue #71). Use `git mv` to preserve history:

```bash
mkdir -p "$PYAUTO_MIND/active"
git -C "$PYAUTO_MIND" mv <draft-path> active/<filename>
```

The `mkdir -p` matters on a **freshly-spawned** Mind, where `active/` does not
yet exist (it holds only instance state, so the template ships without it) —
`git mv` errors if the destination dir is missing. Timestamp-suffix the
filename if one already exists in `active/`.

Then add the prompt's own copy of the date to its light header, so an issued
prompt stays dated even if its registry row later goes missing:

```markdown
Issued: <YYYY-MM-DD>
```

Confirm both landed before pushing:

```bash
python3 "$PYAUTO_MIND/scripts/lifecycle.py" dates    # OK when nothing is undated
```

### 6. Push Mind

```bash
source "$PYAUTO_MIND/scripts/prompt_sync.sh"
prompt_sync_push "prompt: file issue for <task-name> (#<issue>)"
```

If step 0 already pushed, this carries only the active.md + `active/` changes.

## Notes

- Always present the issue body for review before creating it.
- On the `gh` surface, if `gh auth status` fails, tell the user to run
  `! gh auth login`. On the MCP surface there is nothing to log into —
  create the issue with `issue_write` and carry on.
- The detailed plan should be thorough enough that a fresh session could start
  from the issue alone.
