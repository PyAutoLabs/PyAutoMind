# The test-performance board — scoping assessment

Date: 2026-08-24. The deep-research write-up for "the speed of AI development
is heavily dependent on the speed of tests": a dashboard that always shows the
run times of the testing/integration infrastructure (PR smoke gates on the
`*_workspace_test` and normal workspaces, HowTo, unit tests, import time), with
history to flag performance drops, kill-timer/hang events surfaced, NO_RUN
scripts listed with their reasons, and one-tap Claude prompts on every row so
"speed this one up" is a paste, not an archaeology session. Actionable prompt:
`draft/feature/pyautoheart/test_performance_board.md`.

## The problem, with receipts

- Manual timing archaeology is the current tool. The jax_grad budget work
  records that "the diagnosis had to be rebuilt from CI job logs by hand"
  (`complete/2026/08/jax-grad-smoke-timeout-budget.md`), and the 2026-08-23
  slow-vs-stall audit hand-scraped `[PASS] <name> — <n>s` lines per run.
- The cost of not watching is measured: four `autogalaxy_workspace_test` runs
  burned ~24h of runner time at the 6-hour Actions ceiling before the kill
  timer existed (`complete/archive/epics/jax_vmap_jit_compile_stall.md`); the
  autolens_workspace_test PR gate is ~11m20s wall-clock of which 553s is
  scripts, at ~17 runs/week (`draft/test/workspaces/slowest_smoke_gate_scripts.md`,
  `draft/test/pyautoheart/smoke_relevance_gate.md`).
- The existing markers are untrustworthy: "**a SLOW marker is not evidence of
  slowness**" — the first SLOW-marked entry ever measured was wrong by ~50×,
  and every 2026-07-14 marker records no timing at all
  (`complete/2026/08/jax-compile-stall-slow-vs-stall-audit.md`).
- The tracked signal is broken: Heart's `script_timing` baselines are orphaned
  by path-derived slugs (no history accumulated for the moved jax_grad scripts
  since 2026-07-24) and every stored history is one value repeated seven times
  (`draft/bug/pyautoheart/script_timing_baselines_orphaned_and_window_filled.md`
  — filed 2026-08-04, **never issued**).

## What is recommended

**A "⏱ Performance" section on the Heart board, published in the Heart's
`board.json` (schema v2, additive) with every row carrying its own one-tap
prompt — and a headline row on the Brain board consuming it verbatim, exactly
the way `heart_blockers` already works.** Not a seventh board.

Why Heart, not Brain:

- The doctrine is explicit and repeated: "**measurement lives in Heart;
  hygiene acts**" and "new standing signals (import cost, CLI noise) become
  Heart *legs*, not a new repo"
  (`PyAutoBrain/agents/conductors/hygiene/AGENTS.md:143-149`). Heart already
  owns every timing signal in the organism: `script_timing`, `test_run`,
  `import_time`, `unit_test_timing`, `workspace_testmode_timing`.
- The consumption seam already exists and is tested: the Heart board publishes
  structured blockers (`{text, severity, repo, repo_url, run_url, prompt}`)
  and the Brain board renders them verbatim, never re-deriving the prompt
  (`PyAutoBrain/board/_board.py:228-249`, `tests/test_board.py:43-53`).
  A `performance` block rides the same contract; schema v2 is additive by
  design (`complete/2026/08/actionable-health-board.md`).
- The cadence already lines up: Heart renders at 05:00 UTC, the Brain board
  reads it at 05:30 (`PyAutoBrain/.github/workflows/brain_board.yml:20-25`).
- Timing rows are **advisory, never gating** — the precedent is the
  `import_time` leg ("advisory dashboard section, NOT in the readiness gating
  set", `complete/2026/07/import-time-heart-leg.md`). The four-tier
  GREEN/STALE/YELLOW/RED verdict is untouched.

Why not a Brain-board section (considered): the Brain board holds the exact
code to copy — `gh_json` (`_board.py:136-150`), the overnight scrape
(`:167-211`), the self-carrying history (`:456-466`) and `sparkline()` — but
putting the *measurement* there splits ownership against the doctrine, and the
Brain "owns no state, no health checks". The Brain board's role is the morning
headline: "N gates slowed / 1 hang flagged", chip → the Heart page. That row
can ride `draft/feature/pyautobrain/brain_board_follow_ups.md`.

## How the timing information gets calculated and populated

Three data planes, in cost order. "Just scrape recently completed PRs" — the
suggestion that seeded this scoping — is plane A, it works today, and it is
already proven in production.

### Plane A — workflow wall-clock, scraped from the Actions API (ships first)

The default `GITHUB_TOKEN` reads other public PyAutoLabs repos' workflow runs:
`PyAutoMind/.github/workflows/morning_health.yml:68-101` already does exactly
this daily against PyAutoHeart/PyAutoBrain/PyAutoHands/PyAutoFit with
`permissions: contents: read` and no PAT. Per run the API serves everything
the board needs:

- **duration** = `updated_at − run_started_at` (also served directly as
  `run_duration_ms` by `GET /actions/runs/{id}/timing`; ignore the `billable`
  fields — they are 0 on public repos). **Trap, already recorded by the Hands
  board: use `run_started_at`, never `created_at`** — re-attempted runs
  otherwise report multi-day durations (`complete/2026/08/release-board.md`).
- **queue delay** = `run_started_at − created_at`.
- **conclusion** (`success | failure | cancelled | …`) — see the kill-timer
  section for disambiguating `cancelled`.
- **PR association**: `event: pull_request` + `head_branch` — so "what a
  contributor waits on a PR" is directly measurable, per gate, per week.
- **per-job and per-step timings** via `GET /actions/runs/{id}/jobs` — matrix
  leg identity is in the job `name` (`"pytest (3.12)"`), and the *Run smoke
  tests* step is separable from checkout/install overhead. Fan out to `/jobs`
  only for runs worth the detail (the slowest of the day, every `cancelled`
  one) — that keeps the request budget at ~1 call per tracked workflow per
  render, trivially inside the 1000 req/hr limit.

The tracked-workflow list is declared config, not code (the tenant-firewall
rule): a `performance:` block in `PyAutoHeart/config/repos.yaml` naming each
`repo:workflow` pair — every workspace's `Smoke Tests` caller, the HowTo
gates, the organ self-test gates (`tests.yml`), Heart's weekly
`workspace-smoke.yml`, `release-integrate.yml`, and the Brain's
`nightly-release.yml`. One channel note: since #122 the validation channels
are split so runs attribute to the **caller** workflow
(`complete/2026/07/split-validation-channels.md`) — query the callers.

What plane A yields per gate: last-N durations, p50/max, conclusion mix,
queue delay, and the two contributor-facing numbers that matter — median PR
gate latency and its trend.

### Plane B — per-script timings, promoted from log lines to a standing dataset

The runner already prints `[PASS] <name> — <n>s` per entry and a
`=== Smoke test summary ===` terminal line; today that data evaporates into
job logs (retained ~90 days) and is only recovered by hand-scraping. The
smoke-runner delegation (`complete/2026/08/smoke-runner-delegation.md`) turned
all ten workspace runners into thin shims over `autohands/run_python.py` —
**so per-script timing recording is now one PyAutoHands change, not ten
repo sweeps**: extend the existing report machinery (`--report-dir` is
already load-bearing — "without it the gate runs to completion and always
exits 0") to emit a `smoke_timings.json` (entry, status, seconds, cap in
force, exit code), uploaded as a run artifact and/or written to
`$GITHUB_STEP_SUMMARY`. The Heart render fetches the latest artifact per gate.

This is precisely the open question item 4 of
`draft/research/ci/smoke_timing_and_profiling.md` already poses ("should the
runner record per-script timings routinely, so this is a standing dataset
rather than a periodic archaeology exercise?") — this assessment's answer is
**yes, via the delegated runner**. The `retime.yml` classifier and its
verdict vocabulary (STALL/SLOW/NEITHER/AMBIGUOUS/ERROR, `retime_results.json`)
stay as the on-demand deep probe, reached through `smoke-tests.yml`'s
`runner`/`runner-args`/`script-timeout` inputs.

**STALL ≠ SLOW is a first-class dimension, not a footnote.** "A slow script
has a tight timing distribution. A stalling one is bimodal" — a healthy
compile of `rectangular_mge.py` is 3.1s; a stalled one exceeds 300s, same
commit, same runner image (`jax-compile-stall-slow-vs-stall-audit.md`). A
single wall-clock number per entry cannot express this; the board should carry
the retime verdict where one exists, and flag bimodality from the standing
dataset where it doesn't.

### Plane C — baselines and regression flagging (the "history" that must be durable)

Two history mechanisms exist in the board family, with different guarantees:

1. **Self-carrying published artifact** — the Brain board fetches its own
   previous `board.json` at render, appends today, caps at 30 entries
   (`PyAutoBrain/board/_board.py:456-466`). Free, no commits, idempotent per
   date — but lossy (a publish gap loses everything) and 30 days max. Right
   for the plane-A per-gate daily aggregates and their sparklines.
2. **Heart's tracked rolling baselines** (`~/.pyauto-heart/`, the
   `script_timing` mechanism) — durable, but currently broken as filed. Right
   for per-script baselines once fixed.

The fix is a prerequisite, and its prompt is already written:
`draft/bug/pyautoheart/script_timing_baselines_orphaned_and_window_filled.md`
(rename-aware slugs or a loud no-baseline signal; real 7-run accumulation;
record the source run id per duration). **Issue it first.**

For flagging drops, do not invent thresholds — reuse the profiling
conductor's considered doctrine: a regression counts only if it is newer than
its pin, **at least 2.0× the pinned value AND at least 1.0s above it in
absolute terms**, with sticky pins that never move without an explicit
`--repin` ("host load alone has produced 7× errors in this corpus and an
alarm that cries wolf gets ignored" —
`PyAutoBrain/agents/conductors/profiling/AGENTS.md`). The comparability-key
lesson from the compile-warm dashboard transfers too: never pool different
hosts under one label — for CI the key is runner image × Python leg × event
type (`complete/2026/08/compile-warm-baseline-dashboard.md`).

Unit tests and import time ride the same planes: the organ/library `tests.yml`
gates are plane-A rows (they are seconds-to-a-minute today — the board's job
is to notice when that stops being true), and the existing `import_time` leg
(advisory, off-tick, subprocess-measured) surfaces its red/yellow counts as a
row with a `/hygiene` chip — the standing leg promotion that
`hygiene/AGENTS.md:117-119` already names as the deferred follow-up.

## Kill-timer and hang events on the board

The kill timer (PyAutoHands `build_util.timeout_for` + `kill_group`; 300s
smoke default, 900s `jax_grad/`, 1800s release; exit 124; `TIMEOUT` status
with the truncated output tail and the cap in force attached) and the
in-process watchdog (faulthandler dump at 80% of `BUILD_SCRIPT_TIMEOUT`,
heartbeat lines) already leave ingestible traces. The board renders, per gate:

- **Per-script TIMEOUT rows** (plane B): entry, cap, count over the window,
  and the retime verdict if one exists. Chip:
  `/bug kill timer: <repo> <script> TIMEOUT (<cap>s) on <run url> — 22s when
  it passes, stall suspected; stack tail attached to the run log`.
- **Job-level `cancelled` — disambiguated.** `cancelled` with a newer run on
  the same `head_branch` is a superseded PR run (benign — the concurrency
  block cancels non-`main` refs by design, `complete/2026/07/ci-dedupe.md`);
  `cancelled` with duration ≈ the job's `timeout-minutes`, or with no
  successor, is a kill/hang and gets a red row with the run URL. `cancelled`
  on `main` is always red (it is in Heart's `FAILURE_CONCLUSIONS`).
- **Aborted-run detection**: a run whose log lacks the
  `=== Smoke test summary ===` line discarded its remaining coverage
  (`complete/2026/08/smoke-runner-jupyter-guard.md`) — that is a contract
  break, not a pass.
- **Coverage beside time, always.** The `Running N listed scripts` count
  renders next to every duration. "A skipped script is not a failure — CI
  would have stayed green" (`smoke-runner-delegation.md`); a speed dashboard
  that does not carry the entry count rewards deleting coverage.

One standing caution for anyone extending the caps: **a watchdog whose
threshold equals the cap never fires** — the 300s dump collided with the 300s
cap in all 20 stalled runs until #1518 derived it as 80% of the cap, with
tests asserting the *relationship*, not the numbers
(`jax-compile-stall-slow-vs-stall-audit.md`).

## The NO_RUN section

Source: each workspace's `config/build/no_run.yaml`, fetched at render via the
contents API (cheap, one call per repo). Parse the entry plus its trailing
comment — the three marker tiers are established convention
(`complete/2026/07/unblock-release-validation.md`):

| Tier | Meaning | Board treatment | Chip |
|---|---|---|---|
| `SLOW <date> - <reason>` | too slow for the cap; a to-do | row with marker age; **flag any entry with no measured timing in its reason** | `/bug no_run: <repo> <script> SLOW since <date> with no measurement — retime against the real cap, then fix it or delete the marker` |
| `NEEDS_FIX <date> - <reason>` | broken; a to-do | row with marker age | `/bug no_run: <repo> <script> NEEDS_FIX since <date> — <reason>. Reproduce first: this is the third census where the marker had already evaporated` |
| untagged | correct-by-design skip | count only, collapsed | — |

The section encodes three recorded lessons: "a NEEDS_FIX marker is a claim
with a timestamp, not a fact" (`complete/2026/07/scrape-general-stale-needs-fix.md`);
"measure against the real cap before restoring — restoring a skip is not the
safe default" (`complete/2026/07/howto-no-run-stale-entries.md`); and the
41%-dead-entries census (`complete/2026/07/no-run-config-purge.md`) — so the
board also cross-checks each entry against the repo tree and flags matchers
that match zero files. Parser traps to carry into the implementation: a bare
`off`/`on`/`yes` entry parses as a YAML boolean and crashes `should_skip`;
`autocti_workspace_test` has no `no_run.yaml` at all. The allowlist governs
the PR gate and `no_run.yaml` governs the release run — they are different
policies and the board must not conflate them (the #262 near-miss).

## One-tap prompts (the chip mechanism, unchanged)

A chip is a plain slash-command string in `data-cmd`, copied by the shared
`_theme.py` clipboard JS; a row is actionable iff it carries a payload
(`PyAutoBrain/board/_board.py:805-815`). The producer writes the prompt, the
renderer never re-derives it — the invariant the Heart blockers already
follow. Representative payloads for this section:

- `/bug smoke gate <repo>: p50 wall-clock 9.2m → 14.1m over 14 days — <url>`
- `/start_dev draft/test/workspaces/slowest_smoke_gate_scripts.md` (the
  standing hot-spot row: 3 entries are 36% of the autolens gate)
- `/start_dev draft/test/pyautoheart/smoke_relevance_gate.md` (the
  run-less-often lever — note `autogalaxy_workspace_test` has **no** hot spot,
  so only this lever exists for it)
- `/hygiene perf` (the door for standing dev-loop cost)

## Relationship to existing prompts

| Prompt | Relationship |
|---|---|
| `draft/bug/pyautoheart/script_timing_baselines_orphaned_and_window_filled.md` | **Prerequisite (phase 0)** — issue it; plane C reads what it fixes |
| `draft/research/ci/smoke_timing_and_profiling.md` | Companion — its item 4 is answered "yes" here (plane B); its batched re-measure sweep populates the first per-script dataset and rewrites the SLOW markers the NO_RUN section will then trust |
| `draft/test/workspaces/slowest_smoke_gate_scripts.md` | Kept — the "make entries cheaper" lever; becomes a standing chip |
| `draft/test/pyautoheart/smoke_relevance_gate.md` | Kept — the "run less often" lever; becomes a standing chip |
| `draft/feature/pyautohands/release_board_run_logs_enrichment.md` | Adjacent, not subsumed — mega-run pass/fail/timeout counts stay on the Hands board; this board links |
| `draft/feature/pyautobrain/brain_board_follow_ups.md` | The Brain-board consumption row rides it |

## Implementation cautions (every board hit these)

1. **Tenant firewall**: repo/workflow names live in declared config
   (`repos.yaml` / policy blocks), never in organ code; tests use fake names
   (`RepoA`) — the Heart board itself hit this on its first PR
   (`complete/2026/08/actionable-health-board.md`).
2. **Pages enablement**: if `configure-pages` fails with "Resource not
   accessible by integration", create the site once:
   `gh api -X POST repos/<owner>/<repo>/pages -f build_type=workflow`.
3. **HTML self-containment test**: strip `data-cmd` attributes before
   asserting no external assets — payloads legitimately carry URLs.
4. **badge.json is a cross-board contract** — do not reshape the Heart's
   badge message for this; the performance surface is new keys in
   `board.json`, additive.
5. **Trust the page's own generation stamp, never the cron schedule** —
   GitHub cron jitters 0–3h under load.
