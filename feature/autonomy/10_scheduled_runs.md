# Scheduled runs — overnight queue passes with a morning report

Type: feature
Target: autonomy
Repos:
- PyAutoBrain
Difficulty: medium
Autonomy: supervised
Priority: low
Status: blocked

## Why

The end-state of the autonomy series: the organism does useful work while the
human is away — a nightly queue-runner pass over `safe`/`supervised` tasks, or
a scheduled health-loop tick — and the morning interaction is reading one
report and validating PRs. Deliberately **last**: scheduling multiplies
whatever discipline exists, including bad discipline, so it is only worth
building once checkpoint-and-continue and the queue runner have proven
themselves interactively.

## What

1. A scheduled entry point (harness scheduled agents / cron) that launches
   `/run_queue` (or a health tick) on a cadence, capped: max N tasks per run,
   serial worktrees, hard stop-at-PR.
2. **Morning report**: one summary — per task outcome, PR URLs, parked
   questions, calibration rows, anything RED — posted somewhere the human
   actually reads (Mind dashboard section and/or a pinned issue).
3. Guardrails: a scheduled run that hits any unexpected state (dirty
   registry, worktree conflict, Heart RED) parks immediately and says so in
   the report; it never "tidies up" autonomously.

## Boundaries

- No new daemon infrastructure — use the harness's scheduling surface.
- Cost/attention budget is a real constraint: overnight runs burn tokens
  unattended; the cap and the serial rule are contract, not tuning.
- Everything the interactive `--auto` mode forbids (merge, close, force-ship,
  history rewrites) stays forbidden on a schedule — no exceptions for "it's
  just a cron job".

Blocked-by: 7_queue_runner.md (and transitively 1–5). Do not start before the
queue runner has completed several supervised interactive runs cleanly.
