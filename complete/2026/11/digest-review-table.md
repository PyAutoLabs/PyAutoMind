## digest-review-table
- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/718
- completed: 2026-11-25
- library-pr: https://github.com/PyAutoLabs/PyAutoBrain/pull/719
- mind-pr: https://github.com/PyAutoLabs/PyAutoMind/pull/606
- epic: autonomous-orchestrators (M3; before the M3 gate shift; folds M3.3 slice 2 item 1)
- summary: PyAutoBrain#719. The shift digest opens with a numbered `### Review table` (after the closed-early line and inbox notice, before `### Brief work`), with one count line above it. Groups in order, empty ones left out: Merge: your /prm · Answer: question on the issue · Fix: CI failed or crashed · Blocked or not started · Still running · Done (plus Proposed (shadow) on a shadow brief). Each task sits in its single most urgent group; an unrecognised state fails toward Merge. Rows numbered 1..N; Work lists PRs as `repo#n` in merge order with "after repo#m"; cells escape `|`, `<`, `>`. Everything from `### Brief work` down is byte-identical; `validate`/`_slug` ignore the table. PyAutoMind#606 documents it in `batches/AGENTS.md`.
- trigger: human review of shift 2026-11-24-am: "a more structured table like format ... so I know what needs comments, prm, was blocked".
- witness: PASS. Replaying 2026-11-24-am put all 9 tasks in exactly one row, PRs in merge order, `validate` → `[]`; all 19 real slots replayed under HEALTHY/RUNNING/FAILED (57 builds) clean. Brain 2544 passed; Mind 1056 passed.
- review: independent fresh-context review round 1 FINDINGS (branch-updated PR with CI FAILED landed in Still running; CI-running and sweep waits belong in Merge; others), all fixed in bd4b2e6; round 2 CLEAN.
- heart: GREEN (dev-ship gate); judge tier, human /prm.

## Original prompt

# Shift digest: open with one review table grouped by what the human does next

Type: feature
Target: PyAutoBrain
Repos:
- PyAutoBrain
- PyAutoMind
Difficulty: small
Autonomy: supervised
Priority: high
Status: active
Filed: 2026-11-24
Issued: 2026-11-24
Issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/718
Epic: autonomous-orchestrators
Consequence: judge
Witness: the digest of a replayed real shift (2026-11-24-am's counters and slot) opens with a review table in which every named and backlog task sits in exactly one action group (merge, answer, blocked/not started, done), each PR listed in merge order with its repo#n link, and `_digest.validate` still passes on the full record
Review-minutes: 10
Unattended: never
Lane: local-dev

Original request (human, 2026-11-24, after reviewing shift 2026-11-24-am in 15 minutes):
"its all quite good but I think having a more structured table like format for this, so I know what needs comments, prm, was blocked would help make reviews faster and more structured"

## Why

The digest's `### Brief work` section (`agents/conductors/batch/_digest.py`,
`entry_lines` / `build`) is one two-line bullet per task. The outcome words
are there ("Needs you — not merged unattended", "Needs you — question on the
issue", "Not started"), but a task with several PRs puts them all in one long
`<sub>` line with each PR's state and merge-order note. The human has to read
every line to work out three lists: what to `/prm` (and in which order), what
needs a reply on an issue, and what was blocked or never started and why.

## What to build

Add a `### Review table` section at the top of the digest, before
`### Brief work`. It covers named tasks and backlog picks, grouped by the
human's next action, in this order:

| Group | Rule (from `task_state` / `plain_outcome`) |
|---|---|
| **Merge: your /prm** | awaiting /prm, CI green awaiting merge, no CI checks, waits behind (in merge order) |
| **Answer: question on the issue** | PARKED-ON-ISSUE, parked or blocked on a person |
| **Fix: CI failed or crashed** | CI failed, crashed, abandoned, killed |
| **Blocked or not started** | not started (with the skip reason, e.g. "autogalaxy held by X"), dropped, obsolete |
| **Still running** | still running at review time, close-out running or updating |
| **Done** | merged, already merged |

Columns: `Task` (title linked to the Mind prompt), `Tier`, `Work` (each PR or
issue as `repo#n`, one per line in merge order, with "after repo#m" where a PR
waits behind another), and `Note` (the short reason: "tier judge", "merge-cap
0", "question on PyAutoLens#871", "autogalaxy held by …"). Empty groups are
left out. A one-line count goes above the table: "4 to /prm (9 PRs) · 3 to
answer · 2 not started".

Keep the existing `### Brief work` / `### Backlog picks` entries below it
unchanged: `validate`, `_slug` and the tests read them. The table is an
addition, not a replacement. Update the "Digest" format in
`PyAutoMind/batches/AGENTS.md` to match, plus the `/cockpit` shift-end line
and the batch skill's review section if they describe the digest layout.

GitHub renders the digest as a Markdown comment. Make sure a pipe in a PR
title is escaped and the table does not break.

## Boundaries

- This changes the shift's own digest writer, so the organ rule applies: it is
  never a shift task. Run it in chat through start_dev → start_library.
- No change to what the watcher decides or merges, only to how the digest
  presents it.

## Related, not in scope

In shift 2026-11-24-am, `mge_deflections_reverse_mode_nan_at_grid_centre` and
`jit_cache_not_hit_modeling_visualization` were held behind
`substructure_util_zero_padded_halo_slots_make`'s worker. When that worker
parked, the shift closed early (08:34Z, review-at 09:30Z) instead of starting
them. That looks like an early-close gap in the watcher and should be filed as
its own bug if confirmed.
