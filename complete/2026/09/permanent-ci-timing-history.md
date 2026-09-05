# The permanent CI timing record — history that outlives a Pages publish

PyAutoHeart#205 → `7b4e109`, closing PyAutoHeart#204, merged 2026-09-05 on
branch `claude/ci-test-timing-epic-ke2lul`. Phase 2 of the
`ci-timing-fast-tests` epic (`draft/feature/pyautoheart/ci_timing_fast_tests_epic.md`);
Plane C ("durable baselines") of
`docs/pyautoheart/test_performance_board_assessment.md`. Fable-planned on the
issue, implemented by an Opus subagent under the Brain's delegation ladder from
a web session (issue, PR and merge driven through the GitHub MCP surface; no
task worktree).

- issue: https://github.com/PyAutoLabs/PyAutoHeart/issues/204
- completed: 2026-09-05
- library-pr: https://github.com/PyAutoLabs/PyAutoHeart/pull/205

## What shipped

- **`timings/`** — the append-only record in the Heart repo: `gates.jsonl`
  (one line per UTC date; every tracked gate's `p50_s`/`pr_median_s`/`max_s`/
  `queue_median_s`/`runs`) and `scripts/<repo>.jsonl` (one line per python leg
  × run id; `run_url`, `head_branch`, `head_sha`, `env_profile`, and
  `entries: {path: [seconds, status, cap_s]}` for every timed script).
  Compact sorted-key single lines, so a daily diff is the added lines only.
  `timings/README.md` carries the schema and the rules; `timings/epochs.jsonl`
  is reserved (named in code as `EPOCHS_FILE`, not created) for phase 4's
  labeled LEGACY boundary.
- **`heart/timings.py`** — writer (`append_gates`, `append_scripts`, never
  truncates), readers that feed the checks (`gates_history` in the exact
  shape `ci_timing.history_baseline`/`dashboard._gate_spark` consume;
  `previous_script_rows` in the shape `smoke_timings.classify_drift` expects),
  a census, and a CLI (`append`, `show`).
- **Record first, board as fallback.** `ci_timing.aggregate(record_history=)`
  and `smoke_timings.aggregate(record_prev_rows=)` prefer the committed record;
  the previously published `board.json` is used only when the record is empty
  (first run, fresh clone). The `performance` block shape is unchanged, so the
  Brain board reads exactly what it always read.
- **Workflow** — a new step after the checks appends today's observations
  (safe before the render: `ci_timing` excludes today's date from its
  baseline, `smoke_timings` compares by run id); the README-commit step now
  commits `timings/` beside the README block, one `[skip ci]` commit a day,
  guarded by `git status --porcelain` so a repo's first, untracked line is
  seen. The workflow is the record's single writer; a dev-box tick never
  appends.
- **Board** — one `record: …` detail line under each timing row from the
  census (`state.aggregate()` gains `timings_record`); absent census renders
  byte-identically.
- Tests 735 → 767; fake names throughout; tenant firewall OK.

## Key traps / findings

- **Dedupe on identity, never on the day.** `gates.jsonl` is keyed by date
  (a re-run of the daily job is a no-op); `scripts/<repo>.jsonl` by
  `(python, run_id)`. The second key is load-bearing: the smoke artifacts only
  change when a PR runs, so a quiet week hands the daily job the same run
  seven days running — keyed on the day that is the `script_timing` "one value
  repeated seven times" defect all over again. Phase 1 stamped `run_id` on
  every row for exactly this.
- **Untimed entries are not in the record.** A skipped script's `null`
  seconds was never a measurement; writing it as a row would fabricate a
  zero-second observation. Coverage stays visible on the board's per-leg
  census instead.
- **Data files are not committed empty.** An empty file is not a record; the
  first scheduled run creates them. Verify the next daily commit on `main`
  carries `timings/gates.jsonl` and at least one `timings/scripts/*.jsonl`.
- **`git diff --quiet` cannot see an untracked file.** The README-commit
  guard had to become `git status --porcelain README.md timings/`, or the
  record's first line for a repo would never have been committed.
- **Two writers on an append-only file in git is a merge conflict waiting
  for a human** — hence the single-writer rule, stated in the workflow, the
  README and the module docstring.

## Follow-ups (tracked, not started here)

- Phase 3 of the epic: `draft/feature/pyautoheart/offtick_timing_legs_live.md`
  (unit_test_timing / import_time / workspace_testmode_timing live —
  ingestion-first per the epic ledger's Fable review).
- Phase 4 writes `timings/epochs.jsonl` (the LEGACY boundary) and the first
  labeled snapshot, no earlier than the day after this lands in a live run.
- Yearly sharding of the record when a file gets unwieldy — not now
  (`timings/README.md` "Growth").

## Original prompt

# Permanent CI timing history stored in PyAutoHeart

Type: feature
Target: PyAutoHeart
Repos:
- PyAutoHeart
Difficulty: medium
Autonomy: safe
Priority: high
Status: formalised
Consequence: judge
Review-minutes: 20
Unattended: ready
Epic: ci-timing-fast-tests
Phase: 2
Issued: 2026-09-05

Permanent CI timing history stored in PyAutoHeart (replace the 30-day self-carried window).

Today the only "history" is the performance block's rolled-forward window: the aggregate
step re-reads the previously published Pages `board.json` (`heart/checks/ci_timing.sh:64-79`)
and caps at 30 entries (`history_cap: 30`) — a publish gap loses it and nothing is ever
committed to the repo. The user's intent: run-time information on all CI tests tracked with
the nightly run and stored in PyAutoHeart as a PERMANENT record, with the dashboard showing
the most recent times but having access to all history.

Build the durable record: the daily heart-health run appends the day's observations (the
workflow-level gates from ci_timing AND the per-script rows from the phase-1 ingester) to
committed history files in the PyAutoHeart repo (e.g. under `state/` or a dedicated
`timings/` tree — append-only, compact JSON/JSONL per repo, committed by the workflow the
way `state/devbox_board.json` already is). The board keeps rendering the recent window but
links/reads from the committed record; the 30-day Pages self-carry becomes a cache, not the
source of truth. Design reference: Plane C ("durable baselines") of
`PyAutoMind/docs/pyautoheart/test_performance_board_assessment.md`.

Mind the file-growth shape: daily append across ~26 gates + a few hundred script rows must
stay reviewable (one commit/day, stable ordering, no churn of past lines).
