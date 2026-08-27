- completed: 2026-08-24
- issue: https://github.com/PyAutoLabs/autocti_workspace/issues/29 (closed 2026-08-24)
- prs:
  - https://github.com/PyAutoLabs/autocti_workspace/pull/30 (merged, `4b162ae`)
- summary: |
    `autocti_workspace` is in PyAutoHeart's `workspaces` group, whose
    `required_workflows` are `["Smoke Tests", "Navigator Check"]`. Only the
    former existed (added days earlier by #27/#28, the repo's first CI), and
    `heart/checks/ci_status.rollup()` never satisfies `all_green` while a
    required workflow has no runs — so the repo rolled up as permanently
    `in_progress`: able to go red, never able to go green. This added the
    missing `Navigator Check` and committed the catalogue it gates on.

## What landed

- `.github/workflows/navigator_check.yml` — a thin caller of PyAutoHands'
  reusable `navigator_check.yml@main` with `project: autocti`, mirroring the
  four sibling workspaces.
- `llms-full.txt` + `workspace_index.json` — the generated catalogue, 79
  scripts.
- 12 script docstrings: title underline `-----` → `=====`.
- `AGENTS.md` — a "Navigator catalogue (CI)" section.

## Traps and findings

**`Navigator Check` is a PyAutoHands reusable, not a Heart one.** Each workspace
owns a ~30-line thin caller of
`PyAutoLabs/PyAutoHands/.github/workflows/navigator_check.yml@main`, whose only
input is `project:`. The reusable runs three jobs: `check_navigator.py
--banners=fail` (paths + banner lint), `check_search_memory.py` (unbatched
multi-start guard), and a staleness job that regenerates the catalogue and then
`git diff --exit-code llms-full.txt workspace_index.json`.

**The filing prompt's premise did not hold, and it was load-bearing.** The
prompt said the repo already had root-level catalogue files (`llms.txt`,
`llms-full.txt`, `workspace_index.json`). `git ls-files` found none of the
three — the line it drew that from, in `autocti_assistant`'s
`wiki-currency.yml`, is a comment about git's *cone-mode* behaviour, not an
assertion the files exist. That matters because `git diff --exit-code` on
**untracked** paths exits 0: the staleness job would have gone green while
checking nothing. Committing the generated pair is the substance of the fix,
not a side effect of it.

**Twelve docstrings catalogued as a run of dashes.** The generator only treats a
line as a title underline when it is `=`, so twelve scripts whose underline was
`-----` catalogued with the dashes as their summary. Fixed one line per file,
line endings preserved (six of the twelve are CRLF).

## Acceptance criterion — the roll-up, not the workflow

The prompt was explicit that "the workflow passes" is not the criterion. Both
required workflows completed `success` on `main` HEAD `4b162ae` (Navigator Check
run 32778904395, Smoke Tests run 32778904379), and `rollup()` fed with the real
`workspaces` required list flipped:

```
BEFORE (Navigator Check had never run) -> {'conclusion': '',        'status': 'in_progress'}
AFTER  (both green on 4b162ae)         -> {'conclusion': 'success', 'status': 'completed'}
```

Re-verified on 2026-08-27 against the then-current `main` HEAD `ea3e424`: both
workflows `success` on that sha too, so `on_head` (the third of `rollup`'s three
per-workflow conditions, alongside `conclusion == "success"` and `status ==
"completed"`) still holds. The repo can reach `conclusion: success`.

## Work item 4 — the general case, surveyed not implemented

The prompt asked for a proposal, not a widened task. All 15 repos in the four
groups carrying `required_workflows` were surveyed for "does a workflow file
exist whose `name:` matches each required entry":

| group | required | missing a file |
|---|---|---|
| `libraries` | `Tests` | none (all carry `main.yml`) |
| `workspaces` | `Smoke Tests`, `Navigator Check` | **autocti_workspace** only |
| `workspaces_test` | `Smoke Tests` | none |
| `howto` | `Smoke Tests`, `Navigator Check` | none |

So the class had exactly one instance, which #30 removed. It is still worth a
Heart-side drift check: the failure mode is silent by construction (a missing
gate reads as *pending*, indistinguishable from *a run is in flight*), and the
hole reopens on every edit to `repos.yaml` that adds a repo to a group or a
workflow to a group's required list. Suggested shape — a cheap static check in
the deep/on-demand tier (not the <30 s tick), matching on each workflow's parsed
`name:` field rather than its filename, and reporting a miss as a
**configuration** finding rather than red CI, since the repo's code is fine and
its gate is not wired up. Full survey:
https://github.com/PyAutoLabs/autocti_workspace/issues/29#issuecomment-5401319712
Filed and shipped 2026-08-27 as PyAutoHeart#188 — `active/required_workflow_file_drift.md`.

## Left for separate tasks

- A hand-curated `llms.txt` (the siblings carry one; the generator never writes
  it).
- 13 scripts that catalogue as `(no summary in script docstring)`.
- Notebook regeneration, blocked for this workspace entirely because `autocti`
  is absent from `build_util.COLAB_PROJECTS`.

## Mind-side note (why this record is late)

The work shipped on 2026-08-24 but the prompt was never advanced out of
`draft/maintenance/ci/` — no `active.md` entry, no `active/` prompt, no record.
It therefore kept rendering on the dashboard as pickable backlog, and a
`/start_dev` run on 2026-08-27 picked it up before finding PR #30 already
merged. Nothing detects this class automatically (`lifecycle.py check` reported
OK throughout — a `draft/` prompt with no registry entry is a valid state); it
is the "shipped but never retired" drift `PyAutoMind/AGENTS.md` warns about.
This record is that retirement, written retrospectively from the merged PR, the
closed issue and its three comments.

## Original prompt

# autocti_workspace has no Navigator Check, so its CI can never roll up green

Type: maintenance
Target: autocti_workspace
Repos:
- @autocti_workspace
- @PyAutoHeart
Difficulty: medium
Autonomy: supervised
Priority: high
Status: formalised
Filed: 2026-08-24

`PyAutoHeart/config/repos.yaml` lists `autocti_workspace` in the `workspaces`
group, whose required workflows are:

```yaml
required_workflows:
  workspaces: ["Smoke Tests", "Navigator Check"]   # smoke_tests.yml + navigator_check.yml
```

`Smoke Tests` now exists (autocti_workspace#27/#28, 2026-08-24 — the repo's first
CI). **`Navigator Check` does not.** That is not cosmetic.

## Why this blocks readiness, not just tidiness

`heart/checks/ci_status.py` rolls a repo up over its *required* workflows. A
required workflow with **no runs at all** is not scored as a failure — it simply
never satisfies `all_green`. Verified directly against the real function:

```
required for `workspaces`: ['Smoke Tests', 'Navigator Check']

Smoke green, Navigator MISSING -> {'conclusion': '',        'status': 'in_progress'}
both green                     -> {'conclusion': 'success', 'status': 'completed'}
smoke red, Navigator MISSING   -> {'conclusion': 'failure', 'status': 'completed'}
```

So `autocti_workspace` rolls up as **permanently `in_progress`** — never green,
never red. It cannot reach `conclusion: success` no matter how healthy it is,
which means the readiness/release gate can never see this repo as CI-clean.
Adding Smoke Tests was necessary but not sufficient.

Note the asymmetry in that table: a *red* Smoke Tests still reports failure
correctly. So the repo can go red but can never go green — the worst shape for a
gate to be in.

## Work

1. **Find out what `Navigator Check` actually is.** It is not a Heart reusable
   workflow — `PyAutoHeart/.github/workflows/` has no `navigator_check.yml`; the
   name appears only in `config/repos.yaml` and `heart/checks/ci_status.py`.
   Each workspace owns its own `.github/workflows/navigator_check.yml`. Read a
   sibling that has one (`autolens_workspace`, `autogalaxy_workspace`,
   `autofit_workspace`, or a `HowTo*` repo) and mirror it. Do **not** invent a
   check from the name.
2. **Add it to `autocti_workspace`**, adapted to this repo's actual navigator
   surface. autocti_workspace has root-level catalogue files the assistant's
   citation checks already lean on (`llms.txt`, `llms-full.txt`,
   `workspace_index.json` are sparse-checked out by
   `autocti_assistant/.github/workflows/wiki-currency.yml`), so there is a real
   navigator surface here to validate.
3. **Confirm the roll-up flips to `success`** once both workflows are green on
   `main` HEAD — that is the actual acceptance criterion, not "the workflow
   passes".
4. **Consider the general case.** If other repos in a required group are missing
   a required workflow, they have the same silent-never-green defect. A Heart-side
   drift check ("every repo in a required group has a workflow file for each of
   its required workflows") would catch this class rather than this instance.
   Raise it as a proposal with findings; do not widen this task unilaterally.

## Why it was left out of the smoke task

autocti_workspace#28 was scoped to the ordered-trap smoke coverage (CTI epic
Phase 5). Adding a second, unrelated workflow would have widened that PR beyond
its task. Filed here instead, deliberately.

## Context

`PyAutoMind/complete/2026/08/phase5-smoke-ordered-trap-scripts.md` — how the
repo got its first CI, and the `arcticpy: true` caller convention it uses.
