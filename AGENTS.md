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

- **Prompt lifecycle (issue #71)** — a prompt file advances through three
  top-level state folders, mirroring the task ledger:
  - `draft/<work-type>/<target>/<name>.md` — intaken, **not started**. The
    first folder under `draft/` is the *kind of work*; the second is the
    *target repo or domain*. Work-types: `feature/`, `bug/`, `refactor/`,
    `docs/`, `test/`, `release/`, `maintenance/`, `research/`, `experiment/`
    (plus `triage/` for prompts whose classification is still unclear).
    PyAutoBrain routes by the work-type folder — see [README.md](README.md)
    "Prompt taxonomy" and `ROUTING.md`.
  - `active/<name>.md` — **issued** (an open GitHub issue / in flight). The
    ship skills advance the file to `complete/` on merge.
  - `complete/<YYYY>/<MM>/<slug>.md` — **shipped**; the rich completion record
    (see `complete/AGENTS.md`). Months are zero-padded so lexical order is
    numerical order. `scripts/lifecycle.py` owns the moves and drift-checks
    them.

  Retired non-record material lives in **`complete/archive/`** (skipped by
  `lifecycle.py check`/`index`): `archive/epics/` (former `z_features/`
  multi-task trackers) and `archive/shelved/` (former `z_vault/` deferred
  prompts + dev notes). The old `z_features/`, `z_vault/` and `autoprompt/`
  top-level folders were retired here on 2026-07-13.
- **Registry** — root-level markdown files, each with one job: `active.md`
  (in-flight tasks), `planned.md` (scoped, not started), `parked.md` (started
  but not in flight), `queue.md` (ordered
  input for `register_and_iterate --queue`), `ideas.md` (raw inbox swept by
  `$intake`, `/intake` in Claude). Mutate these only via the skills in `skills/` so commit
  messages stay consistent.
  `parked.md` holds tasks that were started or scoped but are not currently
  in flight (e.g. work parked in a stash, orphan worktrees); move back to
  `active.md` (or `planned.md` if re-scoping) when resuming.
- **Body map** — `repos.yaml` is the single source of repo *identity* (GitHub
  home, category, one-line role) for every repo in the workspace. The routing
  table in the workspace-root `AGENTS.md` and the owner map in
  `PyAutoBrain/skills/WORKFLOW.md` are generated from it, and the repo lists in
  Heart/Build/admin scripts are drift-checked against it:
  `python3 scripts/repos_sync.py --write`.
- **Skills** — `skills/<name>/` are agent skills and command bodies tightly
  coupled to the registry. Claude and Codex discovery is installed by
  PyAutoBrain; they source `scripts/prompt_sync.sh` for commit/push.
- **Scripts** — `scripts/status.sh` (inventory), `scripts/prompt_sync.sh`
  (commit/push helpers).

## Hard rules

1. **Never rewrite history on any branch with a remote.** No `git init` over an
   existing repo, no `git push --force` to `main`. (Motivated by the 2026-04-27
   drift incident.)
2. **Pull before edit.** `git fetch && git status` first, every time. If behind
   `origin/main`, `git pull --ff-only` before touching anything.
3. **One prompt = one task = one PR.** If a prompt outlines multiple
   loosely-related changes, split into separate prompt files before issuing.
4. **`tmp/` is scratch.** Never commit anything under it.

## When you are asked to add a new prompt

Write the file under `draft/<work-type>/<target>/<name>.md` — pick the work-type
from the list above (use `triage/` if genuinely unsure) and the target
repo/domain as the second folder, e.g. `draft/feature/autolens/potential_corrections.md`
or `draft/bug/autoarray/mask_edge_case.md`. Don't touch `active.md`, `active/`
or `complete/` directly — those are managed by `$start-dev`, `$create-issue`
and the ship skills (`/start_dev` and `/create_issue` in Claude).

To skip the manual filing, run **`$intake`** (`/intake` in Claude), the
PyAutoBrain Intake/Conception Agent. It classifies a raw idea into the right
`draft/<work-type>/<target>/` folder,
writes the light header (incl. the optional `Difficulty:/Autonomy:/Priority:`
keys — see README "Prompt file format"), and files the prompt for you. It files a
prompt only; `$start-dev` (`/start_dev` in Claude) remains the separate next step.

## When you are asked to start work on an existing prompt

Use `$start-dev draft/<work-type>/<target>/<name>.md` (`/start_dev` in Claude).
Older `<work-type>/<target>/<name>.md` and bare `<target>/<name>.md` paths from
before the lifecycle migration still resolve. It
routes to `$start-library` or `$start-workspace` (`/start_library` or
`/start_workspace` in Claude) based on the repos referenced in the prompt body;
routing keys off `@RepoName` references in the content, not the folder.

## When in doubt

Read [README.md](README.md). It is current as of the last commit on this branch.

<!-- repos_sync:history:begin -->
## Never rewrite history

Never rewrite pushed history on any repo with a remote — no `git init` over a
tracked repo, no force-push to `main`, no fresh-start "Initial commit", no
`filter-repo` / `filter-branch` / `rebase -i` on pushed branches. To get a
clean tree: `git fetch origin && git reset --hard origin/main && git clean -fd`.
<!-- repos_sync:history:end -->
