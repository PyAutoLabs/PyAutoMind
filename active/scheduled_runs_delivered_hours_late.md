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
