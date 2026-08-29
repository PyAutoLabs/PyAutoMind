# AGENTS.md

This file is for AI coding agents (Claude Code, Codex, Cursor, etc.) discovering
this repository.

## What this repo is

**PyAutoMind is the Mind of the PyAuto organism and the starting point of the
PyAuto workflow.** It holds the organism's ideas, intent, goals, priorities and
workflow state. Every task that ends up as a PR in PyAutoNerves, PyAutoFit,
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
    (plus `triage/` for prompts whose classification is still unclear, and
    `human_review/` for work that already shipped and a human wants to sign
    off — declaration-only, see below).
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
  but not in flight), `condemned.md` (self-material staged for the Gut's
  transit-and-void lifecycle — see PyAutoGut), `epics.md` (long-running
  multi-phase programmes and the ledger file that holds each one's state),
  `ideas.md` (raw inbox swept by
  `$intake`, `/intake` in Claude). Mutate these only via the skills in `skills/` so commit
  messages stay consistent.
  `dashboard.md` is the **generated** read-only view over all of it (the page
  the README links): regenerate with `pyauto-brain intake --apply dashboard`
  after any registry or `draft/` change you want reflected immediately — never
  hand-edit it. `dashboard_refresh.yml` self-heals it on pushes to `main`, so a
  missed regeneration is drift that fixes itself, not a broken page — but it
  heals only the **render**. A prompt that shipped and was never retired to
  `complete/` renders faithfully, as pickable backlog, and no workflow can tell
  the difference; retiring it is a human/skill judgement. Per task that is
  `/prm`'s close-out (it sweeps the shipped prompt's folder and regenerates the
  page in the same commit); across the whole backlog it is
  `pyauto-brain intake reconcile` plus the refresh payload on the dashboard
  itself.
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
- **Ledger auto-merge** — a push to `claude/**` whose whole diff is *ledger*
  (`draft/`, `active/`, `complete/`, the root registry files, the dashboard
  pages) is merged into `main` by `.github/workflows/mind_ledger_merge.yml` and
  the branch deleted — no PR, no session step, no "please merge that" prompt.
  Anything touching `scripts/`, `tests/`, `.github/`, `skills/`, `policy/`,
  `docs/`, `repos.yaml` or the prose pages is left for a human, as is anything
  unclassified (the gate is default deny). So: **push your Mind work and move
  on** — do not leave a ledger branch hanging, and do not expect a code branch
  to land by itself. `python3 scripts/ledger_merge.py classify --base
  origin/main` tells you which side you are on before you push; the full
  contract is in [REFERENCE.md](REFERENCE.md) "How the ledger lands".
- **Scripts** — `scripts/status.sh` (inventory), `scripts/prompt_sync.sh`
  (commit/push helpers), `scripts/lifecycle.py` (state moves + drift checks;
  `lifecycle.py dates [--write]` reports/backfills the date every registry
  entry and issued prompt carries — see [REFERENCE.md](REFERENCE.md) "Task
  dates").

## Hard rules

1. **Never rewrite history on any branch with a remote.** No `git init` over an
   existing repo, no `git push --force` to `main`. (Motivated by the 2026-04-27
   drift incident.)
2. **Pull before edit.** `git fetch && git status` first, every time. If behind
   `origin/main`, `git pull --ff-only` before touching anything.
3. **One prompt = one task = one PR.** If a prompt outlines multiple
   loosely-related changes, split into separate prompt files before issuing.
4. **`tmp/` is scratch.** Never commit anything under it.

<!-- repos_sync:remote:begin -->
## Remote sessions (Claude Code on web and mobile)

Three facts, all measured in a web/mobile container, where this file is loaded
and little else is. They ride in every organ because a session may hold any
subset of them — and the session that needs this most is the one holding
several, which is exactly the session no hook fires in.

- **Bootstrap in the first turn, unconditionally** — before the first test
  command, not as a remedy once something looks wrong:

  ```
  bash PyAutoMind/scripts/session_bootstrap.sh          # ~10s cold, ~1s warm
  bash PyAutoMind/scripts/session_bootstrap.sh --check  # report only
  ```

  A session holding several organs registers no SessionStart hook — Claude Code
  reads project hooks from the project directory, which in that layout is the
  repos' *parent*, not a repo — so nothing has set this session up. It was once
  phrased as a remedy keyed to `No module named pytest` or collection
  `ImportError`s naming `yaml`; that symptom stopped appearing when the
  container image moved to Python 3.12, while the environment is still wrong in
  ways that read like a bad command rather than a stale session (`pytest -n
  auto` → `unrecognized arguments: -n`). The bootstrap also **unshallows the
  clones**: a remote session clones shallow, and `git merge-base --is-ancestor`
  then answers "not an ancestor" for a commit whose ancestry is merely absent —
  the answer the ship and close-out procedures act on when proving a branch
  merged.

- **Then run the suite in parallel.** 4 cores, subprocess-heavy suites, no
  single slow test: about 3.5x. `python3 -m pytest -q -n auto`, with
  `pytest-xdist` supplied by the bootstrap above.

- **There is no `gh`, and installing one does not help.** A remote session
  reaches GitHub through the `mcp__github__*` tools, already scoped to the
  session's repos. `gh` installs in two seconds and is a trap: it authenticates,
  then 403s every repo-scoped call, because the egress proxy serves neither the
  REST repo paths nor GraphQL beyond a pinned set of PR-review operations — a
  binary that looks healthy and fails everything that matters. It also defeats
  the surface probe, which keys off `gh auth status`. Read
  `PyAutoBrain/skills/GITHUB_ACCESS.md` at the top of any run that touches
  GitHub; it maps each `gh` operation onto its MCP tool. Spell that path from
  the workspace root, as written: a multi-organ session is cwd'd at the repos'
  *parent*, so a bare `skills/…` reads as a missing file rather than a missing
  repo prefix.
<!-- repos_sync:remote:end -->

## When you are asked to add a new prompt

Write the file under `draft/<work-type>/<target>/<name>.md` — pick the work-type
from the list above (use `triage/` if genuinely unsure — never `human_review/`,
see below) and the target
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

## When you are asked for a human review

`draft/human_review/<target>/<name>.md` holds work that has already **shipped**
and that a human wants to read and sign off before it counts as done. It is the
one work-type nothing may infer: file one only when a human asks for it, by
declaring `Type: human review` (`human-review`/`human_review` read the same) —
`/intake` will never choose it, and no completed task acquires it by default.
Review is opt-in, not a lifecycle stage: `/prm` and the ship skills close a task
out exactly as before and never file a review.

It renders as its own **Human review** section on `dashboard.md`, directly under
*In flight*, and is deliberately not counted as backlog — a review is not work to
pick up, it is work waiting on a person. Its 📋 hands out a read-and-report
prompt, not a `/start_dev`. Sign one off by retiring the prompt the usual way
(`scripts/lifecycle.py record …`, then regenerate the dashboard); if it does not
pass, the follow-up is an ordinary `$intake`.

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
