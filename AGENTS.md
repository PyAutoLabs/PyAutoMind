# AGENTS.md

PyAutoMind holds task intent and workflow state. For registry schemas, prompt
conventions, and operational detail, read [REFERENCE.md](REFERENCE.md) only
when the task needs them. Read [README.md](README.md) for the public overview.

## Where work lives

- Inference campaign intent and pending domain tasks live in **PyAutoInsight**
  (`campaigns.yaml`, `tasks/`, `CHECKIN.md`). Mind retains bounded implementation
  issue/PR lifecycle and claims. See `docs/insight-task-migration.md`; source
  removal follows the destination merge, never precedes it.

- Profiling campaign intent and pending tasks live in **PyAutoPulse**
  (`campaigns.yaml`, `tasks/`, `CHECKIN.md`). Use its single-chat check-in first.
  Mind holds bounded implementation phases and repository claims, linking the
  canonical Pulse task. See `docs/pulse-task-migration.md`.


- `draft/<work-type>/<target>/<name>.md` holds unstarted prompts. Work types:
  `feature`, `bug`, `refactor`, `docs`, `test`, `release`, `maintenance`,
  `research`, and `triage` when genuinely unclear. `human_review` is reserved
  for work a human explicitly asks to review after shipping.
- `active/<name>.md` holds issued prompts; `complete/<YYYY>/<MM>/<slug>.md`
  holds shipped records. `scripts/lifecycle.py` owns these moves.
- `repos.yaml` owns repository identity and generated adapter rollout. Change
  it, then run `python3 scripts/repos_sync.py --write`; never edit generated
  policy copies directly. Root routing and Brain owner maps come from it.
- Codex users must review and trust the current `.codex/hooks.json` hash with
  `/hooks`; changed or untrusted project hooks are skipped. The remote Python
  SessionStart bootstrap applies to Claude sessions only.
- Registry files (`active.md`, `planned.md`, `parked.md`, `condemned.md`,
  `epics.md`, `ideas.md`) are changed through skills in `skills/`.
  `dashboard.md` is generated: run `pyauto-brain intake --apply dashboard`
  after registry or draft changes. Never hand-edit it.

## Hard rules

1. **Never rewrite history on any branch with a remote.** No `git init` over an
   existing repo, no `git push --force` to `main`.
2. **Pull before edit.** `git fetch && git status` first, every time. If behind
   `origin/main`, `git pull --ff-only` before touching anything.
3. **One prompt = one task = one PR.** Split loosely related work before issuing.
4. **`tmp/` is scratch.** Never commit anything under it.
5. **A human review is explicit.** Only file `draft/human_review/` when a human
   asks for it and declare `Type: human review`; neither intake nor close-out
   may infer it.

<!-- repos_sync:remote:begin -->
## Remote sessions (Claude Code on web and mobile)

Three facts, measured in a web/mobile container. A session holding several
organs is cwd'd at the repos' *parent*, where no project hook fires, so
nothing has set it up — this block is what does.

- **Bootstrap in the first turn, unconditionally** — before the first test
  command, not as a remedy: `bash PyAutoMind/scripts/session_bootstrap.sh`
  (`--check` reports only). It supplies pytest/PyYAML/xdist and **unshallows
  the clones**, without which `git merge-base --is-ancestor` calls a merged
  branch "not an ancestor" and the close-out acts on it.
- **Run the suite in parallel**: `python3 -m pytest -q -n auto` (4 cores,
  ~3.5x).
- **There is no `gh`, and installing one does not help** — it authenticates,
  then 403s every repo-scoped call through the egress proxy. GitHub is the
  `mcp__github__*` tools; `PyAutoBrain/skills/GITHUB_ACCESS.md` maps each
  `gh` operation onto its tool and is the one full page on the subject.
<!-- repos_sync:remote:end -->

## Workflow entry points

For a new prompt, write `draft/<work-type>/<target>/<name>.md` or use `$intake`.
Do not move it into `active/` or edit completion records by hand. For existing
work, use `$start-dev draft/<work-type>/<target>/<name>.md`; it routes from
`@RepoName` references in the body. Skill arguments are Mind-relative in both
grouped and flat layouts, e.g. `draft/bug/autoarray/mask_edge_case.md`.
Resolve the actual checkout once; set `PYAUTO_MIND` for an explicit location.

Mind ledger-only pushes on `claude/**` or `codex/**` auto-merge under
`.github/workflows/mind_ledger_merge.yml`; code, skills, policy and prose
changes require a PR. Check with `python3 scripts/ledger_merge.py classify
--base origin/main` before pushing. Push ledger-only work and let the merge
workflow land it. Read [REFERENCE.md](REFERENCE.md) "How the
ledger lands" for conflict handling and classification details.

<!-- repos_sync:history:begin -->
## Never rewrite history

Never rewrite pushed history on any repo with a remote — no `git init` over a
tracked repo, no force-push to `main`, no fresh-start "Initial commit", no
`filter-repo` / `filter-branch` / `rebase -i` on pushed branches. To get a
clean tree: `git fetch origin && git reset --hard origin/main && git clean -fd`.
<!-- repos_sync:history:end -->

<!-- repos_sync:deliverable:begin -->
## Sessions end at their deliverable

A session ends when it reports its deliverable — never arm anything that
outlives the turn to wait for CI, a review or a merge: no `send_later`, no
`subscribe_pr_activity`, no `CronCreate`, no `ScheduleWakeup`, no `/loop`, no
`RemoteTrigger` create/update/run. Judge once, report, stop; the human re-runs
`/prm` (or the batch review) when it is green. Measured: five batch members
armed hourly check-ins on 2026-08-31, and a mobile `/prm` re-armed a 60-minute
`send_later` hourly all night on 2026-09-03 with no task active, draining usage.
<!-- repos_sync:deliverable:end -->

<!-- repos_sync:filing:begin -->
## Where to file

Questions, help with code or an analysis, ideas, bug reports and results from a
user or collaborator — or an agent acting for one — go to
<https://github.com/orgs/PyAutoLabs/discussions> in the matching category
(Help & Questions, Ideas & Proposals, Bugs & Errors, Show and tell;
Announcements is maintainers-only), never to this repo's Issues. An agent never
runs `gh issue create` for such a report: it drafts the title, category and
body and hands them to the human (sessions cannot create Discussions). Only the
development flow — Mind prompt → `/start_dev` → `/create_issue` → one issue per
task → PR — opens issues here. Why: `PyAutoMind/policy/community_surface.md`.
<!-- repos_sync:filing:end -->

<!-- repos_sync:standards:begin -->
## Shared standards

Before changing a shared interface, consult the applicable
[organism standard](https://github.com/PyAutoLabs/PyAutoBrain/blob/main/docs/standards.md)
on demand, identify affected consumers, and validate their adoption. Change
generated guidance at its canonical source and regenerate.

For board changes, follow the applicable sizing, navigation and orchestration
standards and reuse Brain’s shared components. Keep domain data, prompt meaning
and approval boundaries with the board’s owner.
<!-- repos_sync:standards:end -->
