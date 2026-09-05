# Per-script smoke timings reach the ⏱ board — the deferred ingester exists

PyAutoHeart#203 → `7a286ea`, closing PyAutoHeart#202, merged 2026-09-05 on
branch `claude/ci-test-timing-epic-ke2lul`. Phase 1 of the
`ci-timing-fast-tests` epic (`draft/feature/pyautoheart/ci_timing_fast_tests_epic.md`);
Plane B of `docs/pyautoheart/test_performance_board_assessment.md`. Planned on
Opus, Fable-reviewed before issue (review recorded in the epic ledger),
implemented by an Opus subagent under the Brain's delegation ladder from a
web session (no task worktree; issue, PR and merge driven through the GitHub
MCP surface).

- issue: https://github.com/PyAutoLabs/PyAutoHeart/issues/202
- completed: 2026-09-05
- library-pr: https://github.com/PyAutoLabs/PyAutoHeart/pull/203

## What shipped

- **`heart/checks/smoke_timings.{sh,py}`** — the fifth cloud-safe check in
  the daily `heart-health.yml` run, in the `ci_timing` shape. Per smoke-gated
  repo (groups `workspaces`, `workspaces_test`, `howto`): list artifacts via
  the Actions API, select the newest non-expired `smoke-timings-<py>` per
  python leg (the weekly `smoke-timings-{scripts,notebooks}-*` channel is
  deliberately not ingested yet), download + unzip, parse the
  `smoke_timings/1` dataset, write `<name>.smoke_timings.json`; an aggregate
  pass folds every sidecar plus the previously published `board.json` into
  `smoke_timings.json`. Every row carries `run_id` / `run_url` / branch / leg.
- **Rows and verdicts.** `TIMEOUT` entries are hard events with a
  `/bug kill timer: <repo> <entry> TIMEOUT (<cap>s) on <run url>` prompt; a
  script slower than its previous observation by ≥2.0× AND ≥5 s is an
  advisory `warn` row with a `/bug slow script …` prompt
  (`config/repos.yaml thresholds.smoke_timings`, own numbers because
  `ci_timing`'s 1.5×/120 s is sized for multi-minute gates). `null` seconds
  (skipped / never ran) are never a 0 s row. A failed listing or download is
  an honest per-repo / per-leg error, never a quiet-looking empty result.
- **Self-carried previous observation**, keyed by run id: the aggregate
  re-reads `performance.scripts.rows` from the published board and compares a
  `(repo, python, entry)` only when the run id differs, so a same-day
  re-render never compares a run against itself. Durable committed history is
  phase 2.
- **Board**: a "Smoke scripts" section after CI wall-clock (FAIL on
  timeouts, WARN on slowdowns/errors; per-repo top-N slowest with coverage
  counts beside every total) and the additive `performance.scripts` block,
  emitted only when the slice was observed so older snapshots render a
  byte-identical block. Readiness verdict, `badge.json` and the Brain board
  untouched (the Brain ignores the new key; a headline row is a follow-up).
- **Workflow**: `actions: read` permission and
  `GH_TOKEN: ${{ secrets.HEART_TIMINGS_TOKEN || secrets.GITHUB_TOKEN }}`.
- Tests 684 → 735 (34 in `test_smoke_timings.py`, 13 in `test_dashboard.py`,
  4 in `test_heart_health_wiring.py`, 2 shell tests driving `ingest_one_repo`
  with stub `gh`/`unzip`); fake names throughout.

## Key traps / findings

- **Cross-repo artifact downloads may 403 on the repo-scoped token.**
  actions/download-artifact documents a cross-repo download as needing
  `actions: read` on *that* repo; the default `GITHUB_TOKEN` has no standing
  there. Designed in from the start as a secret, not a code change: the check
  records the refusal per repo, and `HEART_TIMINGS_TOKEN` (fine-grained PAT,
  Actions: read on the workspace repos) is the remedy. **Watch the first
  05:00 UTC run** — `N unavailable` on the Smoke scripts row means the secret
  is needed.
- **Per-script drift needs its own thresholds.** The phase prompt said
  "consistent with ci_timing's warn thresholds"; read literally, a 120 s floor
  would never fire on a 5–60 s script. Same doctrine (both gates), own
  numbers — the profiling conductor's 2.0× with a 5 s floor above the ~5–7 s
  import-floor jitter.
- **Dedupe on run id, not date** — the defect phase 0 fixed in
  `script_timing` ("one value repeated seven times") is one quiet week away
  for any daily appender; every row carries `run_id` so phase 2 can key its
  durable record on (repo, python leg, run id).
- **The ledger auto-merge is default-deny on drift anywhere in `active.md`.**
  Another session's row with a bare `- pr:` key (schema wants
  `library-pr:`/`workspace-pr:`) blocked this task's first Mind push from
  landing; the repair was one key rename. A remote session should run
  `lifecycle.py check` before every Mind push, not only its own rows.
- **Delegation worked as the ladder says.** Fable planned and reviewed,
  one Opus subagent implemented from the issue body as spec (~12 min,
  735 green, one docstring repo name removed for the tenant firewall); the
  progress-file heartbeat + `Monitor` made the wait legible.

## Follow-ups (tracked, not started here)

- Phase 2 of the epic: `draft/feature/pyautoheart/permanent_ci_timing_history.md`
  (durable committed history, deduped on run id).
- Weekly `smoke-timings-{scripts,notebooks}-*` channel ingestion; Brain-board
  headline row for the slowest script — both small, neither filed yet.

## Original prompt

# Smoke-timings ingester: per-script CI timing rows on the Heart performance board

Type: feature
Target: PyAutoHeart
Repos:
- PyAutoHeart
- PyAutoHands
Difficulty: large
Autonomy: safe
Priority: high
Status: formalised
Consequence: judge
Review-minutes: 25
Unattended: needs-slicing
Epic: ci-timing-fast-tests
Phase: 1
Issued: 2026-09-05

Build the smoke-timings ingester: per-script CI timing rows on the Heart performance board.

Every gate run in all ten workspace/_test/HowTo repos already uploads a
`smoke-timings-<py>` artifact (`test-results/smoke_timings.json`, schema `smoke_timings/1`:
entry, kind, status, seconds, cap_s, exit_code — emitted by
`PyAutoHands/autohands/result_collector.py`, PyAutoHands#265), and the weekly
`workspace-validation.yml` uploads `smoke-timings-scripts-*` / `smoke-timings-notebooks-*`.
Nothing reads them: `workspace-validation.yml:389` calls this "the deferred Heart-board
timing ingester" and there are zero references to `smoke_timings` under `PyAutoHeart/heart/`.

Add the ingester to the daily `heart-health.yml` cloud run (which already runs `ci_timing`
at 05:00 UTC): fetch the latest smoke-timings artifacts per repo via the Actions API, fold
per-script rows into the board's performance surface next to the existing workflow-level
gates. Board rendering: most-recent per-script times with the slowest scripts highlighted
(per-repo top-N), status/cap context, and drift marking against the previous observation
consistent with ci_timing's existing warn thresholds. Design reference: Plane B of
`PyAutoMind/docs/pyautoheart/test_performance_board_assessment.md`. Follow the existing
check pattern (`heart/checks/ci_timing.py` + sidecar/aggregate split) so the dashboard
section renders from `board.json` like the current performance block.

Scope guard: this phase is read-and-render only — durable history is phase 2 of the epic
(`Epic: ci-timing-fast-tests`); do not build storage here beyond what the board already
self-carries.
