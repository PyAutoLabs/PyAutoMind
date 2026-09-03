## mind-post-cortex-p3-pr-ledger
- issue: https://github.com/PyAutoLabs/PyAutoMind/issues/392 (closed, completed 2026-09-03)
- completed: 2026-09-03
- library-pr: https://github.com/PyAutoLabs/PyAutoMind/pull/393 (merged `7d3ed60f`)
- library-pr: https://github.com/PyAutoLabs/PyAutoBrain/pull/344 (merged `fcb43755`)
- library-pr: https://github.com/PyAutoLabs/PyAutoHeart/pull/195 (merged `b91c026a`)
- epic: mind-post-cortex (phase 3 of 5; ledger draft/maintenance/pyautomind/mind_post_cortex_epic.md)
- shipped: the Mind's PR ledger is schematised, validated, rendered, and the release chain
  it opens now has a step that closes it. Assessment gaps 1 and 2.
  - **`REFERENCE.md` names the PR ledger.** `library-pr:` / `workspace-pr:` had been written
    by `ship_library` and read by `/prm` for months while absent from the `active.md` schema,
    so nothing validated them and the dashboard could render only the free-text `status:`.
    Both are now schematised and **repeatable** (one line per PR; the older `<url>, <url>`
    single line still parses), joined by `pending-release: <lib>@<pr-url>` and
    `release-gate: <lib>`. `pending-release:` is in the completion-record schema too, so the
    obligation outlives the pruned row. Two prose subsections state the contract once — "The
    PR keys" and "The pending-release chain" — and the division of labour is deliberately
    narrow: GitHub's `pending-release` label and the Hands release stay the source of truth,
    **Mind holds only the link and the gate**.
  - **`scripts/lifecycle.py check` enforces it.** Drift (exit 1): an `active.md` row whose
    `status:` says `awaiting-merge` / `PR open` / `shipped` and names no `*-pr:` — a row that
    says `/prm` has work to do and then withholds the only thing it needs. Warning (exit 0,
    and deliberately never escalatable): a `complete/` record whose `pending-release:` is
    uncleared 30 days on. `registry_multi()` is the repeat-tolerant twin of
    `registry_entries()`, which is first-wins by design and would have read a three-PR row as
    one PR; `_record_fields()` stops at `## Original prompt`, because that tail is another
    task's prompt verbatim.
  - **The dashboard renders it** (PyAutoBrain#344). Every `*-pr:` becomes a repo-labelled link
    (`PyAutoBrain#343`) suffixed to the In-flight task line rather than a fifth table column —
    the page is read on a phone. A new **Pending release** section under In flight groups
    merged-but-unreleased library PRs by library, with the in-flight tasks whose
    `release-gate:` names each one underneath; the empty section is omitted. **No `gh` call at
    render time, at any input** — this is the ledger view, and the Brain board's live label
    search stays the fresh view.
  - **The clearing step is named** (PyAutoHeart#195). Nothing in Hands, Brain or Heart removed
    the `pending-release` label: `pre_build` asserts and dispatches and never sees the publish.
    `/review_release` step 5's "Live run" branch is the one step that establishes a release
    *actually published*, so a new step 6 there drops the label from the merged PRs, deletes
    the matching `pending-release:` / `release-gate:` lines from Mind, and confirms via
    `lifecycle.py check` plus the regenerated dashboard. The invariant closes it: *a release
    that was dispatched is not a release that published.*
  - **The CI defect phase 2 found, fixed in passing.** `dashboard_refresh.yml` checks out
    PyAutoCortex beside the Mind and runs the renderer as `--mind .` from inside the Mind
    checkout; `Path(".").parent` is `.`, so `_cortex_root` looked for `PyAutoMind/PyAutoCortex`
    and **every CI render silently dropped the Cortex-gate badges** — the render succeeded, it
    just said less than it knew. Fixed by resolving the Mind path before taking its parent: one
    line and a test, and it fixes any `--mind <relative>` caller, not only the workflow.
  - **Ship-skill wording follows the schema** — `ship_library/reference.md` (one line per PR;
    write `pending-release:` when the PR carries the label), `ship_workspace` (write
    `release-gate:`; carry `pending-release:` into the record), `prm/prm.md` step 5.3 (carry an
    uncleared `pending-release:` into the completion record, and never clear it).
- verified: the prompt's `Witness:`, re-run at close-out on merged `main` — `REFERENCE.md`'s
  `active.md` schema lists `library-pr:`, `workspace-pr:`, `pending-release:` and
  `release-gate:`; `lifecycle.py check` fails on the fixture row with `status: awaiting-merge`
  and no `*-pr:` (`test_the_pr_key_rule_is_wired_into_check`) and prints `lifecycle check: OK`
  on the live ledger; the regenerated `dashboard.md` In-flight lines carry repo-labelled PR
  links (`euclid_strong_lens_modeling_pipeline#50`, `PyAutoMind#393`, …) and the Cortex-gate
  badge is present, which is the `--mind` fix proving itself. Mind `python3 -m pytest -q` →
  380 passed; PyAutoBrain green on 3.12 + 3.13; PyAutoHeart green on 3.12 + 3.13.
- traps: three, and the first two will meet every close-out that follows this one.
  1. **The new drift check bit a row that arrived while the branch was open.**
     `euclid-cpu-two-stage-route` landed on main after this branch was cut, declares
     `status: pr-open` and names its PR only inside the status prose — so `lifecycle check`
     went RED on PyAutoMind#393's own CI, never on main. The prompt's witness demands the check
     pass on the live ledger, which makes the migration part of the phase, so the row got
     `- workspace-pr: https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/pull/50`
     (`16bdd13f`). `REFERENCE.md` had already predicted the shape of this: "the live ledger
     passed the day it shipped, so the first failure can only be a new row."
  2. **The renderer changed under the branch.** Merging PyAutoBrain#344 first made the branch's
     committed `dashboard.md`/`.html` stale *by renderer version*, and `dashboard_refresh.yml`
     failed on the PR with "dashboard.md is stale". The fix is the one every generated-page
     close-out needs: `git pull --ff-only` the canonical PyAutoBrain, then re-render from a cwd
     **inside** the Mind checkout (`9621ced6`).
  3. **No conflicts against phase 2** — the pre-ship `merge-tree` prediction held exactly.
     `origin/main` merged into all three branches cleanly, `_intake.py` included, against phase
     2's `experiment` work-type removal and its `board/_theme.py` edit.

## Original prompt

# Mind's PR ledger: schematise `library-pr:`/`workspace-pr:`, render PRs and the pending-release chain

Type: feature
Target: pyautomind
Repos:
- PyAutoMind
- PyAutoBrain
Themes:
- mind-workflow
Difficulty: medium
Autonomy: safe
Priority: high
Status: draft
Consequence: judge
Witness: `REFERENCE.md` "Registry entries → active.md" lists `library-pr:`, `workspace-pr:` and `release-gate:`; `python3 scripts/lifecycle.py check` fails on a fixture row whose `status:` says `awaiting-merge` but carries no `*-pr:` key and passes on the live ledger; the regenerated `dashboard.md` In-flight table has a PR column linking every `*-pr:` and a new "Pending release" section listing merged-but-unreleased library PRs and the active tasks whose `release-gate:` names them; Brain intake tests cover both renders
Review-minutes: 20
Unattended: ready
Epic: mind-post-cortex
Phase: 3
Filed: 2026-09-03
Issued: 2026-09-03

Phase 3 of `mind-post-cortex` — assessment gaps 1 and 2. Two PRs: Mind
(schema + drift check) and Brain (dashboard renderer).

## Gap 1 — the PR ledger is unschematised (S)

`library-pr:` / `workspace-pr:` are written by `ship_library` (`skills/ship_library/ship_library.md` ~L113)
and read by `/prm` (`skills/prm/prm.md` ~L69) but absent from the `active.md`
schema (`REFERENCE.md` ~L525-553); they are documented only for completion
records (~L631). So nothing validates them and the dashboard renders only the
free-text `status:`.

- Add `library-pr:`, `workspace-pr:` (URL, repeatable — a task may have several
  per kind; keep the existing single-line form working) and `release-gate:`
  (see gap 2) to the `active.md` schema in `REFERENCE.md`, with the rule:
  a row whose `status:` contains `awaiting-merge`, `PR open` or `shipped`
  must carry at least one `*-pr:`.
- `scripts/lifecycle.py check`: enforce that rule (warn → error after one
  release cycle if you prefer; state which). Add a test.
- Brain `_intake.py` dashboard: In-flight rows get a **PR** column — one link
  per `*-pr:` labelled by repo (`PyAutoFit#1555`), plus the `pending-release`
  badge when the PR carries that GitHub label *as recorded in the ledger*
  (never a live `gh` call at render time). Extend the dashboard fixture test.
- Ship skills: confirm `ship_library`/`ship_workspace` write the keys in the
  schematised form; fix the wording in `skills/*/reference.md` if it differs.

## Gap 2 — no pending-release → release → unblocked-workspace chain (M)

Two libraries (PyAutoArray, PyAutoLens) have sat `pending-release` since
2026-09-02 (`epics.md` image-source-mappings status) and phase 3 was opened
ahead of the release by hand. The only machine view is the Brain board's live
`gh` search (`board/_board.py` ~L653-664).

Design (prefer the lean existing lever; do not build a fourth surface):

- **Source of truth stays GitHub** (the `pending-release` label on merged
  library PRs) and Hands (the release that clears it). Mind holds only the
  *link and gate*.
- `ship_library` writes `pending-release: <lib>@<pr-url>` into the task's
  `active.md` row when it opens a pending-release PR; `ship_workspace` writes
  `release-gate: <lib>` on a workspace task blocked behind an unreleased
  library. `/prm` close-out carries `pending-release:` into the completion
  record; the release path (`pre_build`/Hands post-publish or `/prm` on the
  release) clears it — specify exactly which step and edit that skill.
- Dashboard: a **Pending release** section under In flight, grouped by
  library: merged-but-unreleased PRs (from `active.md` rows and
  `complete/` records whose `pending-release:` is not yet cleared) and, under
  each, the active tasks whose `release-gate:` names it. Empty section is
  omitted.
- `lifecycle.py check`: a `complete/` record with an uncleared
  `pending-release:` older than N days is a warning, not an error.

Keep the Brain board's live query as the fresh view; the dashboard section is
the ledger view and must say so in one line.
