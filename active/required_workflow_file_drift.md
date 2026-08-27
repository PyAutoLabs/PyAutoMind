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
