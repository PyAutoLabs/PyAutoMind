- completed: 2026-08-27
- issue: https://github.com/PyAutoLabs/PyAutoHeart/issues/188 (closed 2026-08-27)
- prs:
  - https://github.com/PyAutoLabs/PyAutoHeart/pull/189 (merged, `2a1391f`)
- summary: |
    The general case behind autocti_workspace#29/#30, filed and shipped the same
    day. `heart/checks/ci_status.rollup()` scores a repo over its group's
    `required_workflows`, and a required workflow with **no runs** is never
    scored as a failure — it just never satisfies `all_green`, so the repo sits
    at `{"conclusion": "", "status": "in_progress"}` forever: able to go red,
    never able to go green. On the dashboard that is indistinguishable from a
    run in flight, which is why the state survives unnoticed.
    `heart/checks/required_workflow_drift.py` makes it nameable.

## What landed

- `heart/checks/required_workflow_drift.py` — for every repo in a group that
  declares `required_workflows`, assert a workflow exists whose `name` matches
  each required entry. `polled_repos` / `gating_repos` / `fetch_workflow_names`
  / `check_one` / `run`, mirroring `manifest_drift.py`'s shape (own sidecar,
  `available: false` when it cannot run, coloured one-line `main()`).
- `heart/state.py` — aggregates `required_workflow_drift.json` into `state.json`.
- `heart/tick.sh` — runs it, `|| heart_log WARN` like its siblings.
- `heart/readiness.py` — YELLOW per missing workflow (`required_workflow_drift`),
  plus a stale `required workflows unverified` reason
  (`required_workflow_unknown`); scoring weights for both keys.
- 15 new tests (`tests/test_required_workflow_drift.py` + four cases in
  `tests/test_readiness.py`). Full suite 656 passed.

## The two design calls, and why

**Read the workflow list, not the runs.** The runs payload `ci_status` already
fetches cannot separate the two causes of "no runs" — a workflow file that does
not exist, and one that exists but has never run on `main`. Only
`GET /repos/{owner}/{repo}/actions/workflows` can, so that is the one call
added. The second case is genuinely pending and must stay pending; a test pins
it (`test_workflow_present_but_never_run_is_not_missing`).

**Match on `name`, never the filename.** `name` is what `ci_status` matches runs
against, so a filename-based check could pass while the roll-up still starves.
Confirmed against a live repo: `actions/workflows` returns
`name: "Navigator Check"` with `path: ".github/workflows/navigator_check.yml"` —
exactly that case.

Classified YELLOW and as a **configuration** finding rather than red CI: the
repo's code is fine, its gate is not wired up, and red would misattribute the
fault.

## The trap: the tenant firewall scans docstrings and tests

`heart-tests.yml` runs `repos_sync.py --only "tenant firewall (organ code)"` on
every Heart PR. It scans every organ `.py`/`.sh` **line** — docstrings, comments
and test fixtures included — for non-organ repo names and GitHub owners, and
treats *any* instance fact in an unlisted file as drift.

The first draft named a workspace repo in the module docstring (recounting the
incident) and used real repo names in the test fixture config. Both would have
reddened CI. Rewritten to name no instance fact at all — the docstring says "one
workspace repo", the fixture uses invented names — rather than growing
`FIREWALL_ALLOWLIST`, which `repos_sync.py` explicitly warns against ("never
grow it casually — a new entry means a new file an adopting fork must rewrite").
So this change added no allowlist entry, and the module is tenant-agnostic,
which is the better design anyway.

Verified the gate genuinely scans the new files rather than trusting a green:
appended a canary token, watched the check fail naming the exact file and line,
removed it, watched it pass.

## The prompt's cost note held up

The original proposal (autocti_workspace#29) assumed a periodic Actions-API
sweep or a check that runs where sibling checkouts exist, and so belonged in a
deep/on-demand tier. `ci_status.sh` says otherwise: it already loops every
polled repo in parallel making two cheap `gh api` metadata calls each
(`actions/runs?branch=main`, `commits/main`). The third is the same shape and
cost, and only repos in a group that *gates* need it — 17 today; advisory groups
are skipped without a call.

## Deliberately not done

- Folding the finding into `ci_status`'s sidecar or `rollup()`'s return.
  `rollup()` is the release gate; reshaping it to carry a configuration finding
  would ripple through readiness, dashboard and publish for no gain.
- The release-ci profile's `unobserved` list, whose sentence is specifically
  about dev-box-local evidence. This check is not dev-box-local.
- `docs/readiness_evidence_audit.md` — a dated 2026-07-16 audit deliverable with
  "writer last ran" columns, not a living index; adding a 2026-08-27 row would
  misdate it.

## Session notes (remote web session)

No `gh` and no task worktree: PyAutoHeart was attached with `add_repo` and cloned
flat at `/home/user/pyautoheart`, GitHub driven through the `mcp__github__*`
tools. Two consequences worth knowing:

- **Heart's own gate read YELLOW, entirely from the environment.** 17 ×
  "CI status unavailable" (no `gh` for `ci_status.sh` to call) and one
  "manifest drift: local checkout origins" — `add_repo` clones from
  `PyAutoLabs/pyautoheart` while the body map says `PyAutoHeart`, and GitHub is
  case-insensitive where `repos_sync.py` is not. Nothing about the diff.
- **`--depth 1` clones single-branch.** Its fetch refspec is
  `+refs/heads/main:refs/remotes/origin/main`, so `git push -u` set the upstream
  but no `origin/feature/*` tracking ref ever existed, and a local git-state
  check read the pushed branch as unpushed. The remote branch was correct
  throughout; the fix is to widen the refspec, never to re-push.

## Original prompt

# Heart cannot see a required workflow that has no file — the silent never-green defect

Type: feature
Target: pyautoheart
Repos:
- @PyAutoHeart
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: formalised
Filed: 2026-08-27
Issued: 2026-08-27

`PyAutoHeart/config/repos.yaml` declares `required_workflows` per group, and
`heart/checks/ci_status.py`'s `rollup()` scores a repo over exactly those
workflows. A required workflow that has **no runs at all** is not scored as a
failure — it simply never satisfies `all_green`, so the repo sits at
`{"conclusion": "", "status": "in_progress"}` forever: able to go red, never
able to go green, and invisible to the readiness/release gate as CI-clean.

That is indistinguishable, on the dashboard, from "a run is in flight". Nothing
anywhere says "this repo is missing a gate".

This was found the hard way: `autocti_workspace` sat in that state from whenever
it was added to the `workspaces` group until 2026-08-24, when a human noticed the
asymmetry (a red Smoke Tests still reported failure correctly, so the repo could
go red but never green). Fixed for that instance by autocti_workspace#30; the
class was left as a proposal, deliberately, so the fix PR was not widened. This
is that proposal, filed.

## Why it is worth a check even though the class is currently empty

A survey of all 15 repos across the four groups carrying `required_workflows`
(run 2026-08-24, on the issue) found `autocti_workspace` was the **only**
instance, and #30 removed it. So this is not a bug hunt — it is a guard against
the hole reopening, which it does on every edit to `config/repos.yaml`:

- adding a repo to a group silently makes it un-greenable until it carries a file
  for each of that group's required workflows;
- adding a workflow to a group's `required_workflows` silently does the same to
  **every** repo in the group at once.

Both edits look harmless in review. Neither produces a red anything.

## Shape

A cheap per-repo assertion: for every repo in a group with `required_workflows`,
a workflow exists whose parsed `name:` field matches each required entry. Match
on `name:`, not the filename — `name:` is what `ci_status` matches against, so a
filename-based check could pass while the roll-up still starves.

Two design notes, one of which corrects the original proposal:

1. **It probably needs no new data source, and no sibling checkouts.** The
   original proposal assumed either a periodic Actions-API sweep or a check that
   runs where the workspace checkouts exist. But `heart/checks/ci_status.sh`
   already loops every polled repo in parallel and makes two cheap `gh api`
   metadata calls each (`actions/runs?branch=main`, `commits/main`). A third —
   `GET /repos/{owner}/{repo}/actions/workflows`, which returns every workflow
   file with its `name` — is the same shape and the same cost, and it is the
   only call that can tell *missing file* from *file exists, has never run on
   main*. Check whether that fits the <30 s tick budget before falling back to a
   deep/on-demand tier; `ci_status.sh`'s own header argues the existing two calls
   are cheap enough, so a third plausibly is too.
2. **A missing file is a configuration finding, not red CI.** The repo's code is
   fine; its gate is not wired up. Colouring it red misattributes the fault.
   `heart/checks/manifest_drift.py` is the precedent to mirror — a drift check
   that classifies as YELLOW ("hygiene that will eventually break something, not
   an immediate release blocker"), writes its own sidecar, and is consumed by
   `readiness.py` as a caution rather than a gate.

The `required_workflows` block in `config/repos.yaml` already carries each
group's filenames in a trailing comment (`# smoke_tests.yml + navigator_check.yml`),
which is a useful cross-check but not the matching key.

## Acceptance

- Adding a repo to a group whose required workflows it does not have produces a
  named finding, not a silent `in_progress`.
- The finding distinguishes "no workflow file" from "workflow exists, no runs on
  main HEAD yet" — the second is genuinely pending and must stay pending.
- A test in `PyAutoHeart/tests/` alongside `test_manifest_drift.py` /
  `test_ci_status.py`.

## Context

- `PyAutoMind/complete/2026/08/autocti-workspace-navigator-check.md` — the
  instance, and the roll-up table that shows the defect.
- https://github.com/PyAutoLabs/autocti_workspace/issues/29#issuecomment-5401319712
  — the original proposal and the full 15-repo survey.

## Original prompt

# Heart cannot see a required workflow that has no file — the silent never-green defect

Type: feature
Target: pyautoheart
Repos:
- @PyAutoHeart
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: formalised
Filed: 2026-08-27
Issued: 2026-08-27

`PyAutoHeart/config/repos.yaml` declares `required_workflows` per group, and
`heart/checks/ci_status.py`'s `rollup()` scores a repo over exactly those
workflows. A required workflow that has **no runs at all** is not scored as a
failure — it simply never satisfies `all_green`, so the repo sits at
`{"conclusion": "", "status": "in_progress"}` forever: able to go red, never
able to go green, and invisible to the readiness/release gate as CI-clean.

That is indistinguishable, on the dashboard, from "a run is in flight". Nothing
anywhere says "this repo is missing a gate".

This was found the hard way: `autocti_workspace` sat in that state from whenever
it was added to the `workspaces` group until 2026-08-24, when a human noticed the
asymmetry (a red Smoke Tests still reported failure correctly, so the repo could
go red but never green). Fixed for that instance by autocti_workspace#30; the
class was left as a proposal, deliberately, so the fix PR was not widened. This
is that proposal, filed.

## Why it is worth a check even though the class is currently empty

A survey of all 15 repos across the four groups carrying `required_workflows`
(run 2026-08-24, on the issue) found `autocti_workspace` was the **only**
instance, and #30 removed it. So this is not a bug hunt — it is a guard against
the hole reopening, which it does on every edit to `config/repos.yaml`:

- adding a repo to a group silently makes it un-greenable until it carries a file
  for each of that group's required workflows;
- adding a workflow to a group's `required_workflows` silently does the same to
  **every** repo in the group at once.

Both edits look harmless in review. Neither produces a red anything.

## Shape

A cheap per-repo assertion: for every repo in a group with `required_workflows`,
a workflow exists whose parsed `name:` field matches each required entry. Match
on `name:`, not the filename — `name:` is what `ci_status` matches against, so a
filename-based check could pass while the roll-up still starves.

Two design notes, one of which corrects the original proposal:

1. **It probably needs no new data source, and no sibling checkouts.** The
   original proposal assumed either a periodic Actions-API sweep or a check that
   runs where the workspace checkouts exist. But `heart/checks/ci_status.sh`
   already loops every polled repo in parallel and makes two cheap `gh api`
   metadata calls each (`actions/runs?branch=main`, `commits/main`). A third —
   `GET /repos/{owner}/{repo}/actions/workflows`, which returns every workflow
   file with its `name` — is the same shape and the same cost, and it is the
   only call that can tell *missing file* from *file exists, has never run on
   main*. Check whether that fits the <30 s tick budget before falling back to a
   deep/on-demand tier; `ci_status.sh`'s own header argues the existing two calls
   are cheap enough, so a third plausibly is too.
2. **A missing file is a configuration finding, not red CI.** The repo's code is
   fine; its gate is not wired up. Colouring it red misattributes the fault.
   `heart/checks/manifest_drift.py` is the precedent to mirror — a drift check
   that classifies as YELLOW ("hygiene that will eventually break something, not
   an immediate release blocker"), writes its own sidecar, and is consumed by
   `readiness.py` as a caution rather than a gate.

The `required_workflows` block in `config/repos.yaml` already carries each
group's filenames in a trailing comment (`# smoke_tests.yml + navigator_check.yml`),
which is a useful cross-check but not the matching key.

## Acceptance

- Adding a repo to a group whose required workflows it does not have produces a
  named finding, not a silent `in_progress`.
- The finding distinguishes "no workflow file" from "workflow exists, no runs on
  main HEAD yet" — the second is genuinely pending and must stay pending.
- A test in `PyAutoHeart/tests/` alongside `test_manifest_drift.py` /
  `test_ci_status.py`.

## Context

- `PyAutoMind/complete/2026/08/autocti-workspace-navigator-check.md` — the
  instance, and the roll-up table that shows the defect.
- https://github.com/PyAutoLabs/autocti_workspace/issues/29#issuecomment-5401319712
  — the original proposal and the full 15-repo survey.
