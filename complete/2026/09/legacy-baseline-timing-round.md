# The legacy timing round — the record is labeled, the digest is written

PyAutoHeart#209 → `ad56720`, closing PyAutoHeart#208, merged 2026-09-06 on
branch `claude/ci-test-timing-epic-ke2lul`. Phase 4 of the
`ci-timing-fast-tests` epic (`draft/feature/pyautoheart/ci_timing_fast_tests_epic.md`).
Fable-planned; the epoch code implemented by an Opus subagent under the
Brain's delegation ladder, the digest written in the judgment tier from the
seeded data; web session (issue, PR, merge and the workflow dispatches through
the GitHub MCP surface; no task worktree).

- issue: https://github.com/PyAutoLabs/PyAutoHeart/issues/208
- completed: 2026-09-06
- library-pr: https://github.com/PyAutoLabs/PyAutoHeart/pull/209

## What shipped

- **The round itself.** `heart-health.yml` dispatched by hand on 2026-09-05
  rather than waiting for the 05:00 UTC cron; it seeded `timings/`: 26 gates
  in `gates.jsonl`, 22 legs / 494 script rows across all 11 smoke-gated repos
  in `scripts/<repo>.jsonl`, **0 legs unavailable** — the cross-repo artifact
  403 risk carried since #203 did not materialise and the `HEART_TIMINGS_TOKEN`
  fallback was never needed.
- **`timings/epochs.jsonl` live** — one append-only line per boundary
  (`{date, label, note}`); every record reader (`gates_history`,
  `previous_script_rows`, `previous_unit_rows`, `import_history`) takes
  `since` and compares only within the current epoch (the latest boundary
  dated on or before today; undated lines count as older than any boundary).
  No boundary = one unbroken epoch = the previous behaviour. The first
  boundary, `legacy @ 2026-09-05`, was written by the new `heart.timings
  epoch` verb — the human door; the daily `append` never touches the file
  (pinned). The board shows the epoch on both timing rows and in an additive
  `performance.epoch`. **The phase that lands the rebuild appends the next
  boundary in its own PR** (README instruction).
- **`timings/legacy_round_2026-09.md`** — the digest: gate wall-clock
  medians (autogalaxy_test 11.9 m, autolens_test 9.2 m, autolens_workspace
  7.8 m …, with ~2–3 min/leg of checkout + install overhead); in both `_test`
  flagships the time sits in ~15 compile-dominated `jax_likelihood` scripts
  (autogalaxy_test 537 s / 39 scripts, 9 in the 20–40 s band = 232 s;
  autolens_test 435 s / 27, the 8 scripts ≥ 20 s = 251 s), with
  `imaging/visualization/visualization.py` the one execution-dominated
  outlier; the user workspaces and HowTos are import-floor dominated
  (HowToLens 47 of 50 scripts under 10 s at a ~5 s median); the slowest
  single script anywhere is autocti_workspace
  `imaging_ci/modeling/start_here.py` at 61 s; Python 3.13 legs run faster on
  the user workspaces; six historical hang events (Jul–Aug) still in the
  50-run window. Unit/import section is a placeholder until a library CI run
  produces the `unit-timings` artifact.
- **Hermeticity fix**: two `main --aggregate` tests fell through to the live
  record; one went red on main after the first `[skip ci]` record commit.
- **`heart-tests.yml` `workflow_dispatch`** — see the trap below.
- Tests 841 → 864; fake names; tenant firewall OK.

## Key traps / findings

- **A PR opened on top of a `[skip ci]` base got no CI at all.** #209 was
  opened while main's tip was the daily record commit (`docs(heart): … [skip
  ci]`). No `pull_request` run was created on open, and none on a later
  `synchronize` push either; the three earlier epic PRs, opened on merge
  commits, all ran. Nothing could run the suite on the head — `heart-tests.yml`
  had no manual trigger, and the rules forbid empty commits and close/reopen.
  Fix: a `workflow_dispatch` door, then dispatch on the branch; the check runs
  land on the head sha. **Every day now ends with a `[skip ci]` commit on
  Heart's main**, so any PR opened right after it is exposed; the dispatch
  door is the remedy until the cause is understood.
- **Live data on `main` can break tests that were hermetic by accident.** The
  first record commit landed with `[skip ci]`, so main's suite never ran
  against it; the red only showed on the next branch. Aggregate-mode tests
  must always pass `--record-dir` to an empty dir.
- **Where the digest lives matters for the ledger gate.** A `docs/` file in
  PyAutoMind is *code* to `mind_ledger_merge.yml`, which would have held the
  epic's ledger branch for a human; beside the record in PyAutoHeart
  `timings/` it rides the code PR, and the Mind stays ledger-only.
- **Seed the record by hand.** Dispatching the daily workflow rather than
  waiting for the cron turned "phase 4 no earlier than tomorrow" into the same
  evening.

## Follow-ups (tracked, not started here)

- Phase 7 of the epic (CI caches:
  `draft/feature/pyautoheart/smoke_ci_caches_jax_datasets.md`) next, per the
  ledger's review order, before the phase-5/6 rebuild waves.
- The rebuild's own PR appends the `fast-tests` epoch boundary.
- Fill the digest's unit/import section from the record once library CI runs
  have produced `unit-timings` artifacts (phase 9 reads the same rows).
- Understand the `[skip ci]`-base / no-`pull_request`-run behaviour; if it
  reproduces, consider dropping `[skip ci]` from the daily record commit in
  favour of a paths filter.

## Original prompt

# Legacy baseline timing round: snapshot pre-rebuild timings of every CI test surface

Type: test
Target: PyAutoHeart
Repos:
- PyAutoHeart
- workspaces
Difficulty: medium
Autonomy: safe
Priority: high
Status: formalised
Consequence: judge
Review-minutes: 20
Unattended: ready
Epic: ci-timing-fast-tests
Phase: 4
Issued: 2026-09-05

Legacy baseline timing round: snapshot the pre-rebuild timings of every CI test surface.

With phases 1-3 live, do the first full timing round across the workspace, _test workspace
and HowTo repos plus unit tests and import times: trigger/collect a complete pass, verify
every repo reports, and record the snapshot in the phase-2 durable history explicitly
LABELED AS THE LEGACY RECORD. The user's framing: the epic's later phases (the _test
physical+fast rebuild, CI caches) will change script content, datasets and pinned
likelihoods, so this round is a legacy reference — NOT the starting point of the long-term
tracking history, which begins after the rebuild lands. Mark it so in the stored record and
on the board (a labeled epoch boundary, so post-rebuild drift warnings do not fire against
pre-rebuild baselines).

Deliverables: the labeled snapshot committed to PyAutoHeart; a short written digest of
where the time currently goes (slowest scripts per repo, slowest unit tests, import
floors, compile-dominated vs execution-dominated classes) — this digest is the input
evidence for phases 5, 6, 8 and 9 of the epic.
