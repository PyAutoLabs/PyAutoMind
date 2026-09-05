# CI timing & fast tests — epic

Type: feature
Target: PyAutoHeart
Repos:
- PyAutoHeart
- workspaces
Difficulty: too-large
Autonomy: supervised
Priority: high
Status: formalised
Epic: ci-timing-fast-tests

Epic slug: `ci-timing-fast-tests`
Born: 2026-08-31. Design doc: `docs/pyautoheart/test_performance_board_assessment.md`
(Plane B per-script ingestion and Plane C durable baselines are the unshipped parts this
epic finishes).

## Standing assumptions (hold for the whole epic)

- **All other source/workspace development is PAUSED while this epic runs.** The stack is
  treated as a stable state of truth: changes that alter hardcoded likelihood pins and
  simulated datasets are allowed, with library unit tests and the `*_workspace_developer`
  / `autolens_profiling` surfaces as independent validation that nothing else moved.
- Compile-time doctrine from the closed jax-compile-time arc applies: **settings and
  caches, never likelihood/sampler restructuring, are the sanctioned compile-time lever**
  (persistent cache certified 51x local / 5.9x A100; tracing floor is jax-internal).
- The XLA CPU Eigen-pool workaround `--xla_cpu_multi_thread_eigen=false` is a correctness
  flag (jax-compile-stall epic) — keep it; do not trade it for speed. Coverage of that bug
  class (`multi_dataset/jax_likelihood/*`) must survive any dataset shrinking.

## Ground truth at birth (2026-08-31 survey)

- LIVE: `ci_timing` check + daily 05:00 UTC `heart-health.yml` run + Pages board
  `performance` block (26 gates, 8-day workflow-level history). Per-script
  `smoke_timings.json` emission + `smoke-timings-<py>` artifact upload on every gate run
  across all ten workspace/_test/HowTo repos (PyAutoHands#265, schema `smoke_timings/1`).
- DEAD: no ingester reads those artifacts (workspace-validation.yml:389 calls it "the
  deferred Heart-board timing ingester"); no permanent history (30-day self-carried Pages
  window only; nothing committed to PyAutoHeart); `unit_test_timing` /
  `workspace_testmode_timing` never run, `import_time` ran once 2026-07-11; the documented
  "daily cron" for the off-tick legs does not exist.
- _test smoke gates: autolens 26 / autogalaxy 39 / autofit 11 / autocti 3 entries;
  profile `PYAUTO_TEST_MODE=2` + `PYAUTO_SMALL_DATASETS=1` + `PYAUTO_DISABLE_JAX=1`;
  `ENV: jax full_datasets` scripts (the ~50s class) are exempt from every cap — compile
  ~12-18s + full-res vmap + ~5-7s import floor. JAX persistent compile cache is written to
  `~/.cache/pyauto_jax` by `autonerves/jax_wrapper.py` but CI has **no actions/cache step**
  — discarded between runs.

## Phases

| Phase | Prompt | State |
|---|---|---|
| 1 | active/smoke_timings_ingester_per_script_board.md | **issued 2026-09-05** — PyAutoHeart#202, branch `claude/ci-test-timing-epic-ke2lul` |
| 2 | draft/feature/pyautoheart/permanent_ci_timing_history.md | filed |
| 3 | draft/feature/pyautoheart/offtick_timing_legs_live.md | filed |
| 4 | draft/test/pyautoheart/legacy_baseline_timing_round.md | filed |
| 5 | draft/test/autogalaxy_workspace_test/physical_fast_rebuild.md | filed |
| 6 | draft/test/autolens_workspace_test/physical_fast_rebuild.md | filed |
| 7 | draft/feature/pyautoheart/smoke_ci_caches_jax_datasets.md | filed |
| 8 | draft/test/workspaces/user_workspace_howto_slow_script_pass.md | filed |
| 9 | draft/research/workspaces/unit_test_import_time_hotspot_census.md | filed |

Order: 1→2→3 build the instrument (3 may run alongside 2); 4 snapshots the legacy record;
5 rehearses the rebuild on the smaller repo before 6 does the flagship; 7 is independent
infrastructure and may run any time after 1; 8 and 9 are data-driven and follow once
ingested timings exist. Issue ONE phase at a time — no bulk issue queues.

## Fable review of the Opus plan (2026-09-05, before phase 1 was issued)

The nine-phase decomposition stands; these are the corrections and design calls
it needed, recorded here so later phases do not re-derive them.

- **Phase 0 of the board arc is already done.** The design doc's "issue
  `script_timing_baselines_orphaned_and_window_filled.md` first" shipped as
  PyAutoHeart#166 on 2026-08-24 (`complete/2026/08/script-timing-baselines-fix.md`);
  the ground-truth survey above omits it. Nothing is pending before phase 1.
- **Recommended order: 1→2→3→4→7→5→6→8→9.** Phase 7 (CI caches) is
  content-independent and already certified (51x local / 5.9x A100), so it
  belongs immediately after the legacy snapshot and *before* the rebuild waves:
  the rebuilds then target what remains once compile is cached, and every
  phase-5/6 before/after is measured on one cache state. Keeping 7 after 4
  preserves the snapshot as the pre-everything record. The original "7 may run
  any time after 1" is superseded by this unless the human objects.
- **Phase 1 design calls (in PyAutoHeart#202):** per-script rows get their own
  declared thresholds (`thresholds.smoke_timings`: 2.0x AND >=5 s — the
  profiling ratio with a floor above import-floor jitter) rather than
  ci_timing's 1.5x/120 s, which is sized for multi-minute gates; the prompt's
  "consistent with ci_timing" is read as same doctrine, own numbers. Only the
  PR-gate `smoke-timings-<py>` artifacts are ingested; the weekly
  `smoke-timings-{scripts,notebooks}-*` channel is a follow-up. Every row
  carries its source `run_id`/`run_url`. Known risk: the artifact `/zip`
  endpoint may refuse the repo-scoped `GITHUB_TOKEN` for other repos'
  artifacts; the check records that per repo and the workflow already reads a
  `HEART_TIMINGS_TOKEN` secret (fine-grained PAT, Actions: read) as the remedy —
  a secret, not a code change.
- **Phase 2 must dedupe on run id, not date.** A repo with no new gate run
  between two daily ticks yields the same artifact twice; appending by date
  would write a quiet week as seven copies of one run — the exact "one value
  repeated seven times" defect phase 0 fixed in `script_timing`. Phase 1
  records `run_id` on every row for this reason; the durable record appends one
  observation per (repo, python leg, run id).
- **Phase 3 execution home: prefer ingestion over a new cloud leg.** The five
  libraries' own `Tests` gates can emit a `pytest --durations` JSON artifact
  (one PyAutoHands/library change, ingested exactly like phase 1) instead of a
  daily job that source-installs the stack. `workspace_testmode_timing` is the
  exception (it needs the installed stack) and may stay dev-box-observed and
  published via `pyauto-heart publish`, which the board already renders
  (`state/devbox_board.json`). Phase 3 decides; this is the default.
- **Phase 4 timing.** It needs one live `heart-health.yml` run after phases 2
  and 3 have merged (the first run seeds the durable record), so it is issued
  no earlier than the day after; its deliverable is the labeled snapshot plus
  the written digest, and both are human-judged.
- **Phases 5/6.** Before/after per-script seconds must come from the phase-1
  artifact rows (same runner class), never from local timings; pins regenerate
  once, from the final simulations, with `--xla_cpu_multi_thread_eigen=false`
  in force. Already in the prompts; restated because it is the one place the
  wave can silently invalidate itself.
- **Pause exception on record.** `epics.md` notes image-source-mappings
  proceeds alongside this epic by user decision (2026-09-02); that is the only
  sanctioned exception to "all other development paused".

## Original request (verbatim, 2026-08-31)

> We recently built infrastructure for a workspace, test workspace and HowTo CI test
> timing dashboard. The idea is for me to be able to quickly look at the run times of all
> the CI tests, which it is pivotal run fast for AI development, and to have a history so
> we can track when things slow down or speed up.
>
> A key task is to finish this work, the dashboard feels incomplete, I cant see all this
> information and Im not sure the dashboard is live or being written too. I am probably
> picturing that run time information on all CI tests in these repos is tracked with the
> nightly run, and stored in PyAutoHeart as a permenant record. The dhasboard probably
> displays the most recent times (maybe focusing on the slowest or something), but has
> access to history to all.
>
> Then do a first round of intiial timings, but note below the changes we make mean this
> is more a legacy timing run than the starting point for the full tracking history.
>
> However, I first want us to make two important changes to the _test_workspasce CI tests:
>
> 1) Make sure they are all physical and realistic galaxy and lens models where
> appropriate, with high likelihood solutions and sensible physical inputs. I think this
> is the case for most, but if the simulator and model used in a script have a mismatch,
> update them so this is not the case. I want _test workspaces to use physical and
> sensible models, as if a user does need to inspect and interpret their failures its a
> lot more interpretable.
>
> 2) The _test CI scripts should run as quickly as possible, without losing test
> coverage. At the moment, many run in and around 50 seconds or less, but this is still a
> major botleneck when it comes to CI testing during AI development. Assess how we can
> make thehm run faster, I think the obvious first focus would be to reduce pixel_scale to
> even lower than 0.2" (or other values used in scripts, maybe to 0.3" which still makes
> just about a resolveable lens). However, do a census of all our options, obviously
> targetnig the bottlenecks the most. One worthwhile arm to consider is whether
> enviroment variables, especially those controlling JAX, could be used to enable some
> speed up, if compile times are the bottleneck. Recent work has done a lot of research on
> this when trying to fix XLA bugs in the dataset_multi scripts, which dont really seem
> able to compile well on CPU.
>
> I want the same timing infrastructure and whatnot to be available on the normal
> workspaces and HowTo's, albeit because these are user facing and use PYAUTO_SMALL_DATASET
> env for fast run times, the speed ups on these is probably different to the test
> workspaces. We reduced autolens important time recently, this probably also includes
> compile times, but has less low hanging fruit, these scripts are often faster though,
> but I suspect there are some big bottlenecks.
>
> This should all also include in the dashboard some stats on unit test run times and
> bottlenecks, with options to target speeidng them up, and inform on import times, any
> other things which generally drive this. It could even be that small refactors to often
> used parts of the source code in the numpy or JAX mode could produce good performance
> increases across the board.
>
> When we work on this, we will pause all other work on source code and workspace
> development. This measn you can assume we are owrking at a "stable" state of truth and
> can make changes which change hardcoced likelihood values and whatnot. Unit tests and
> _profiling workspaces offer an inpdenedent validation that any changes like this have
> not impacted elsewhere.
