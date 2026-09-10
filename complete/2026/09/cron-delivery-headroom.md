## cron-delivery-headroom
- issue: https://github.com/PyAutoLabs/PyAutoMind/issues/396 (closed 2026-09-09)
- library-pr: https://github.com/PyAutoLabs/PyAutoMind/pull/397 (merged 0dad3b33 -> main; branch head eba38c32)
- completed: 2026-09-09
- bundle: ci-smoke (member 2 of 4; members 1 and 4 were dropped at the read-first step as already shipped, and retired the same day)

### The premise did not survive the measurement — that is the result

The prompt named a churn hypothesis and explicitly flagged it as "NOT yet
evidence". Measured over 2026-09-05..09, it is **not supported**:

- **r(PyAutoMind churn, PyAutoMind lag) = -0.155** — no correlation, marginally
  negative. The quietest day in the window (09-07, 9 runs) carries the *longest*
  lag (+5h04); the two busiest days sit mid-range.
- **r(PyAutoMind lag, PyAutoMemory lag) = +0.992**, mean gap 8.4 min — while
  PyAutoMemory has 240 runs in its entire history against PyAutoMind's 5,497
  (~4.4/day vs ~190/day, a ~45x difference in volume).

The lag tracks the calendar day, not the repo: GitHub's global scheduler
backlog, stable at ~+5h through September, drifted up from ~+1h in mid-August
with no matching change in churn. **No offset reduces it**, and the shipped
comments do not claim otherwise.

Two corollaries worth not re-deriving:

- **`registry_reconcile`'s `:23` is not privileged.** The prompt cited it as the
  least-delayed of the set on 08-26; across September it medians +5h05,
  indistinguishable from the top-of-hour crons. A good instinct that the wider
  sample does not support as a remedy.
- No delivery was actually *missed* in the window — 22/22 weekdays for
  `arxiv_papers`, 16/16 days for `morning_status`. The failure is lateness, not
  absence, which is a different bug from the one the 08-28 observation implied.

### What shipped, and the one real find

Six cron lines, 9 insertions / 9 deletions, no logic touched:
`arxiv_papers` 02:00->02:07, `arxiv_interests` 02:30->02:37 (keeping the 30-min
gap its dedupe depends on), `dashboard_refresh` 03:20->03:26,
`branch_sweep` 04:10->04:52, `morning_status` 05:00->05:09,
`morning_health` 06:00->06:13. No minute is 0, 30, or shared by any cron in
either repo; day-of-week fields byte-identical.

**The one genuine find is `branch_sweep`**: it fired at exactly 04:10, the same
wall-clock minute as PyAutoMemory's `arxiv_refs`. A real collision between two
of our own schedules, removed.

Each line carries a `do not round (#396)` comment in `registry_reconcile`'s
inline style, so the next tidy-up pass leaves the offsets alone. Two block
comments naming the old nominal minute were corrected so they no longer lie.

Untouched, as the prompt required: `dashboard_refresh`'s unconditional
`pages_dashboard.yml` dispatch and its `DO NOT fold this back into the heal
path` guard (a token push fires no `push` event — that comment guards the
2026-08-27 stranding); `arxiv_papers`' content path; `registry_reconcile`;
`spawn_drift`.

### PyAutoMemory: no change, no commit, no PR

Both its crons were already off the hour with unique minutes, and a common-mode
lag gives no reason to move them. The repo was left byte-for-byte untouched
rather than given a cosmetic edit to have something to show. One consequence
flagged rather than papered over: `arxiv_refs.yml`'s comment says "after
PyAutoMind's 02:00 digest", now nominally 02:07 — still true as an ordering
statement (04:10 >> 02:07).

### The follow-up the evidence actually argues for

Item 3 of the prompt's suggested shape — a **catch-up leg** that fires the digest
if the day's post has not gone out — was out of scope here and is now the live
question. With a stable ~+5h backlog that no offset touches, "should the morning
post depend on cron delivery at all?" is the real design decision, and it is a
different change rather than a bigger version of this one. Worth an `/intake`.

### Traps

- **Mind's PR CI surface is one workflow.** Of 13 workflows, only
  `spawn_drift.yml` runs on every PR without a path filter (jobs: `privacy`,
  `drift`); `dashboard_refresh`, `firewall_gate` and `lifecycle_drift` are all
  path-filtered and correctly did not fire for a `.github/workflows/*.yml` diff.
  The 411-test suite runs in the **pre-commit hook**, not in CI — so on a remote
  session the local run is the only thing that exercises it, and the hook takes
  2+ minutes, which needs a generous command timeout or a background run.
- **`test_the_hook_survives_an_unwritable_tools_dir` fails in any root
  container.** It chmods a directory to `0o500` to make it unwritable; root
  bypasses directory permissions, so `policy/session_start_hook.sh` succeeds
  where the test expects failure. Verified pre-existing by running it on a tree
  carrying no cron change. Not a regression, and not something to fix by editing
  the test — a container artifact.
- Heart was **UNAVAILABLE, not RED**, throughout: `pyauto-brain vitals` reports
  `CI unavailable (query failed)` for all 17 repos because the remote session's
  egress proxy serves no REST repo paths. The documented fallback applies — the
  worktree suite is the gate. Do not read that as a Heart verdict.

## Original prompt

# Every scheduled workflow is delivered hours late, or not at all

Type: bug
Target: ci
Repos:
- @PyAutoMind
- @PyAutoMemory
Themes:
- ci-smoke
Difficulty: medium
Autonomy: safe
Consequence: judge
Review-minutes: 20
Unattended: ready
Priority: high
Filed: 2026-08-28

The `#papers` arXiv digest did not arrive on 2026-08-28 and arrived ~10.5 hours
late on 2026-08-27. The digest workflow is not the cause: `arxiv_papers.yml` is
`state: active`, unmodified since July, and its last run
([#40](https://github.com/PyAutoLabs/PyAutoMind/actions/runs/33072860801)) was
green — it posted to Slack and filed two papers into `arxiv-inbox.md`. What
failed is the *delivery* of the cron.

## What was observed

Every scheduled workflow in both repos, measured 2026-08-28 13:05Z:

| cron | 08-26 | 08-27 | 08-28 |
|---|---|---|---|
| `arxiv_papers` 02:00 | 03:09 (+69m) | 12:38 (+10h38) | — |
| `arxiv_interests` 02:30 | (not yet added) | (dispatched by hand) | — |
| `dashboard_refresh` 03:20 | 04:05 (+45m) | 14:17 (+10h57) | — |
| `morning_status` 05:00 | 05:23 (+23m) | 15:58 (+10h58) | — |
| `morning_health` 06:00 | 06:56 (+56m) | 17:29 (+11h29) | — |
| `registry_reconcile` 06:23 | 07:13 (+50m) | 17:41 (+11h18) | — |
| Memory `arxiv_refs` 04:10 | 04:50 (+40m) | 15:07 (+10h57) | — |

Three things this rules out. It is not one workflow — it is all of them, in two
repos, shifted by the same amount, so no per-workflow change can explain it. It
is not a disabled schedule — `get_workflow` reports `state: active`, and the
60-day inactivity rule does not apply to repos pushed to hourly. And it is not
the runs failing: the last run of each is green.

It also predates the outage. The 20–70 minute baseline drift on 08-25/26 is
already GitHub's documented "scheduled workflows may be delayed during periods
of high load", and it means the crons have no headroom: a morning post pinned to
02:00 has been arriving whenever the scheduler gets to it for weeks, and nobody
noticed because it still landed before the human woke up.

## The hypothesis that is NOT yet evidence

`PyAutoMind` carries 3,139 workflow runs and does ~28 in a half hour overnight:
every push to `main` fans out to Lifecycle Drift + Dashboard Refresh + Pages
Dashboard, and since 2026-08-27 Dashboard Refresh also `gh workflow run`s Pages
Dashboard on *every* non-PR run — the fresh path as well as the heal path. That
is real churn and worth measuring. It is **not** demonstrated to cause the
scheduler lag, and the dispatch it would remove is a deliberate fix (the
`DO NOT fold this back into the heal path` comment in `dashboard_refresh.yml`
guards a real bug: a token push fires no `push` event, so the published page
stranded on 2026-08-27 while `main` was correct). Do not "fix" that comment away
to reduce run count. If the churn is to be cut, cut it somewhere that does not
re-open the stranding.

## Why this is worth work rather than waiting

The `#papers` empty-day heartbeat exists so that silence in the channel always
means a broken run, never a quiet day. A cron that may or may not fire breaks
that contract in the other direction: silence now means "delayed, probably",
which is exactly the ambiguity the heartbeat was built to remove. The same is
true of the Memory board's staleness banner, which spent 2026-08-28 correctly
reporting "the nightly filing may be broken" about a filing that was merely
un-delivered.

## Suggested shape

1. Measure the churn before assuming it. Runs-per-day per workflow, and whether
   scheduled delivery lag correlates with the repo's own concurrent usage.
2. Give the crons headroom rather than precision: move off the top of the hour
   (`registry_reconcile` already does, with the comment "offset to dodge
   top-of-hour load", and it was the *least*-delayed of the set on 08-26).
3. Decide whether the morning post should depend on cron delivery at all — a
   catch-up leg that fires the digest if the day's post has not gone out is a
   different design from trusting a 02:00 trigger.

## Not to re-derive

- `arxiv_papers.yml` itself is fine. Two sessions have now checked it; the run
  history is green and the content path (Slack payload, `arxiv_survivors.json`,
  the inbox filing step) works. Start at the scheduler, not the workflow.
- `arxiv_interests.yml` has never fired on schedule — it was added 2026-08-27
  and its only run is a manual dispatch. That is this outage, not a second bug.
- Today's post was recovered by a `workflow_dispatch` on 2026-08-28 13:13Z
  ([run #41](https://github.com/PyAutoLabs/PyAutoMind/actions/runs/33174407734)),
  so the 08-28 papers are not lost and no backfill is owed for that day.
