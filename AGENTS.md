# AGENTS.md

This file is for AI coding agents (Claude Code, Codex, Cursor, etc.) discovering
this repository.

## What this repo is

**PyAutoMind is the Mind of the PyAuto organism and the starting point of the
PyAuto workflow.** It holds the organism's ideas, intent, goals, priorities and
workflow state. Every task that ends up as a PR in PyAutoConf, PyAutoFit,
PyAutoArray, PyAutoGalaxy, PyAutoLens, or any of the `*_workspace*` repos begins
as a markdown file here.

PyAutoMind is the organism's Mind (intent and direction). The organs and their
boundaries are defined once in `PyAutoBrain/ORGANISM.md`; see
[README.md](README.md) for this repo's full picture.

For the full workflow narrative, conventions, and registry schemas, read
[README.md](README.md). The summary below is just enough to operate.

## Layout (operational)

- **Prompts** — `<work-type>/<target>/<name>.md` (free-form markdown, one task
  per file). The **first** folder is the *kind of work*; the **second** is the
  *target repo or domain*. Work-types: `feature/`, `bug/`, `refactor/`, `docs/`,
  `test/`, `release/`, `maintenance/`, `research/`, `experiment/` (plus `triage/`
  for prompts whose classification is still unclear). PyAutoBrain routes by the
  first folder — see [README.md](README.md) "Prompt taxonomy" and `ROUTING.md`.
  Lifecycle/meta folders are **not** work-types and keep their own names:
  `issued/` (routed prompts), `z_features/` (multi-task epic trackers),
  `z_vault/` (deferred), `shelved/`, and `autoprompt/` (prompts about this repo's
  own infrastructure).
- **Registry** — root-level markdown files: `active.md`, `complete.md`,
  `planned.md`, `parked.md`, `queue.md`, `priority.md`, `ideas.md`. Mutate
  these only via the skills in `skills/` so commit messages stay consistent.
  `parked.md` holds tasks that were started or scoped but are not currently
  in flight (e.g. work parked in a stash, orphan worktrees); move back to
  `active.md` (or `planned.md` if re-scoping) when resuming.
- **Body map** — `repos.yaml` is the single source of repo *identity* (GitHub
  home, category, one-line role) for every repo in the workspace. The routing
  table in the workspace-root `AGENTS.md` and the owner map in
  `PyAutoBrain/skills/WORKFLOW.md` are generated from it, and the repo lists in
  Heart/Build/admin scripts are drift-checked against it:
  `python3 scripts/repos_sync.py --write`.
- **Skills** — `skills/<name>/` are Claude Code skills/commands tightly coupled
  to the registry. They source `scripts/prompt_sync.sh` for commit/push.
- **Scripts** — `scripts/status.sh` (inventory), `scripts/prompt_sync.sh`
  (commit/push helpers).

## Hard rules

1. **Never rewrite history on any branch with a remote.** No `git init` over an
   existing repo, no `git push --force` to `main`. The 2026-04-27 drift incident
   that motivated `autoprompt/03_history_rewrite_guard.md` is the reason.
2. **Pull before edit.** `git fetch && git status` first, every time. If behind
   `origin/main`, `git pull --ff-only` before touching anything. See
   `autoprompt/04_source_of_truth_rule.md`.
3. **One prompt = one task = one PR.** If a prompt outlines multiple
   loosely-related changes, split into separate prompt files before issuing.
4. **`tmp/` is scratch.** Never commit anything under it.

## When you are asked to add a new prompt

Write the file under `<work-type>/<target>/<name>.md` — pick the work-type from
the list above (use `triage/` if genuinely unsure) and the target repo/domain as
the second folder, e.g. `feature/autolens/potential_corrections.md` or
`bug/autoarray/mask_edge_case.md`. Don't touch `active.md` or `issued/` directly
— those are managed by `/start_dev` / `/create_issue`.

To skip the manual filing, run **`/intake`** (the PyAutoBrain Intake/Conception
Agent): it classifies a raw idea into the right `<work-type>/<target>/` folder,
writes the light header (incl. the optional `Difficulty:/Autonomy:/Priority:`
keys — see README "Prompt file format"), and files the prompt for you. It files a
prompt only; `/start_dev` remains the separate next step.

## When you are asked to start work on an existing prompt

Use `/start_dev <work-type>/<target>/<name>.md` (older `<target>/<name>.md` paths
from before the taxonomy migration still work too). It will route to
`/start_library` or `/start_workspace` based on the repos referenced in the
prompt body — routing keys off the `@RepoName` references in the content, not the
folder.

## When in doubt

Read [README.md](README.md). It is current as of the last commit on this branch.
## Never rewrite history

NEVER perform these operations on any repo with a remote:

- `git init` in a directory already tracked by git
- `rm -rf .git && git init`
- Commit with subject "Initial commit", "Fresh start", "Start fresh", "Reset
  for AI workflow", or any equivalent message on a branch with a remote
- `git push --force` to `main` (or any branch tracked as `origin/HEAD`)
- `git filter-repo` / `git filter-branch` on shared branches
- `git rebase -i` rewriting commits already pushed to a shared branch

If the working tree needs a clean state, the **only** correct sequence is:

    git fetch origin
    git reset --hard origin/main
    git clean -fd

This applies equally to humans, local Claude Code, cloud Claude agents, Codex,
and any other agent. The "Initial commit — fresh start for AI workflow" pattern
that appeared independently on origin and local for three workspace repos is
exactly what this rule prevents — it costs ~40 commits of redundant local work
every time it happens.
