# CI smoke speed-up: `hygiene ci` + `/ci_speedup`, and the three slowest smoke scripts

Four PRs merged 2026-09-08 from one web session (no Mind prompt, no issue,
no task worktree — the task started as a chat ask, ran the new skill it built,
and shipped through the GitHub MCP surface; PRs opened in the ship_* format,
judged and merged by `/prm` on the same surface):

- PyAutoLabs/PyAutoBrain#369 → `8232bd1` — `hygiene ci` mode + `/ci_speedup` door
- PyAutoLabs/PyAutoArray#534 → `180c8a4` — vectorised over-sampled grid builder; mask-edge overlay skipped under fast plots (`pending-release`)
- PyAutoLabs/autolens_workspace_test#308 → `71a8b16` — caps knob in the smoke profile; shared_preloads jit + per-band caching
- PyAutoLabs/autocti_workspace#31 → `63fce45` — `PYAUTO_FAST_PLOTS: "1"` in the smoke profile

- issue: none (chat-initiated; recorded retroactively at close-out)
- completed: 2026-09-08
- library-pr: https://github.com/PyAutoLabs/PyAutoArray/pull/534
- library-pr: https://github.com/PyAutoLabs/PyAutoBrain/pull/369
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace_test/pull/308
- workspace-pr: https://github.com/PyAutoLabs/autocti_workspace/pull/31
- pending-release: PyAutoArray@https://github.com/PyAutoLabs/PyAutoArray/pull/534

Retires `draft/test/autocti_workspace/imaging_ci_start_here_61s.md` (filed
2026-09-06, split out of the ci-timing-fast-tests epic's phase 8): its ask —
diagnose where the script's time goes under the smoke profile, fix it the
phase-8 way (shared machinery and a profile override first, script content
last, never the tutorial prose), CI as the acceptance — is exactly what
PyAutoArray#534 + autocti_workspace#31 did; the script itself is untouched
and the before/after rows are below. Its full text is folded under
`## Original prompt`.

## What shipped

- **`pyauto-brain hygiene ci [--top N] [--lane scripts|tests|gates|all] [--json]`**
  — the conductor's read of the Heart board's published `performance` block
  (`board.json` v3: `scripts.rows`, `unit.tests`, `gates`). Stdlib helper
  `agents/conductors/hygiene/_hygiene_ci.py`: fetches Pages /
  `HYGIENE_HEART_BOARD` / a local Heart checkout (org derived from the body
  map — tenant firewall clean), ranks three lanes, folds a script's python legs
  into ONE candidate whose cost is the slowest leg (the gate waits for it),
  carries the evidence (seconds, share of leg, `cache_jax`, run URL) and reads
  levers off the script text when checked out (`env_knob`, `simulates`,
  `jax_jit`, `full_datasets`, `real_search`, `subprocess`, `plots`). One 📋
  per item. Unreachable board = exit 3, never a clean zero. On demand only —
  never the default scan. 10 tests.
- **`/ci_speedup`** (`skills/ci_speedup/`) — the maintenance door that
  executes an item: reproduce under the smoke profile (cold + warm cache),
  name the split (compile / simulate / search / repeated construction /
  plots), pick the smallest lever that keeps the assertion, ship through
  `start_dev` → `ship_*`. Never demotes or skips a script to get the number
  down; a *slowdown* row is `/bug`'s; likelihood compute is `/profiling`'s.
- **First run — the three slowest smoke scripts on the board**, all measured
  locally under the exact smoke profile with the libraries from source:

  | script (board, slowest leg) | CI | local before → after (cold / warm) | lever |
  |---|---|---|---|
  | autocti_workspace `imaging_ci/modeling/start_here.py` | 89.5s | 117s → 26s / 16s | PyAutoArray vectorisation + `PYAUTO_FAST_PLOTS` |
  | autolens_workspace_test `misc/jax_assertions/delaunay_nn_caps.py` | 41.5s | 41s → ~24s / 13s | `DELAUNAY_NN_CAP_RANDOM_SAMPLES=10` via `profile_smoke.yaml` `set:` |
  | autolens_workspace_test `multi_dataset/jax_likelihood/shared_preloads.py` | 36.7s | 47s → 23s / 11s | one `jax.jit` instead of ~500 eager compiles; datasets built once per band |

  No assertion changed anywhere; the shared_preloads likelihoods printed
  before and after are identical; the vectorised grid routine is bit-identical
  to the loop it replaced (the old loop is the oracle in a new test).

## Key traps / findings

- **The autocti cost was a library bug, not the script.** `FitDataset.__init__`
  forces `dataset.grids.border_relocator`, whose `BorderRelocator.__init__`
  called `grid_2d_slim_over_sampled_via_mask_from` — a per-pixel Python loop
  (a `linspace`, a `meshgrid` and a `stack` per unmasked pixel; ~180k
  iterations, ~12s, on a 2000x100 CTI frame) — once per fit, four fits, for a
  relocator a CTI fit never uses. ~50s of the script. The same routine is on
  every imaging fit's path, so large-mask autolens fits pay it too.
- **Eager JAX likelihoods never hit the persistent compile cache.** Evaluated
  op by op, `shared_preloads.py` compiled 496 tiny XLA programs per run
  (~11s + ~7s dispatch), each under the cache's 1s minimum-compile-time
  threshold — a `cache_jax: hit` leg would have saved nothing. One traced
  program compiles once and caches.
- **`cache_jax: miss` on both autolens_workspace_test legs (2026-09-06 run)**
  — every compile paid in full; ~12s of the caps script is six distinct
  compiles. Not fixed here; it is a Heart `smoke-tests.yml` cache-key
  question, and the ranker now flags it on each item.
- **Warm autocti runs were slower than cold before the fix** (171s vs 117s):
  a completed bypass result re-visualises on resume (12 fits and 100 plots vs
  8 and 56). CI never resumes (no `output/` cache), so the cold number is the
  CI number.
- **`PYAUTO_FAST_PLOTS` drops the figure before draw/save** — so under it the
  mask-edge overlay `plot_array` derived on every call (~0.4s each on the CTI
  frame) was work nobody could see; now skipped under the flag only.
- **The workspace smoke gates run on PR/main only**, so a pushed branch gives
  no CI number: the PR is the measurement. The next Heart render shows the
  rows.
- **Local measurement needs arcticpy from source** (GSL headers +
  `pip install arcticpy==2.6 --no-build-isolation --no-deps`, the Heart
  action's recipe) and the libraries on `PYTHONPATH`; PyPI `autocti` is a
  2023 pin and does not install against current autofit.

## Not done / follow-ups (not filed — surfaced by `hygiene ci`)

- Unit-test lane: PyAutoLens `potential_correction/test_fit.py::test__fit_dpsi_src_imaging__end_to_end_evidence_is_finite` 14.0s; PyAutoFit `test_blackjax_smc.py::test__cold_run_recovers_the_analytic_log_evidence` 11.6s (1.36× baseline), `test_linear_regression.py::test_laplace` 10.5s (1.71×).
- Gates lane: autogalaxy_workspace_test Smoke Tests median 698s (max 13299s, 4 hang events on the board); PyAutoBrain Nightly Release median 87m.
- The JAX compile-cache miss on the autolens_workspace_test smoke legs.
- Pre-existing, unrelated: `tests/test_branch_sweep.py::test_a_failed_delete_reports_why` fails on `origin/main` in the web container (git error-text dependent).

## Original prompt

> look up 3 slowest smoke tests and work out how to speed them up for ci,
> pyautoheart has dashboard info on this. actually can we make this a skill?
> some sort of skill which automatically picks out slowest parts of CI from
> dashboard and speeds them up. then run the skill once weve made it

(Chat ask, 2026-09-08. No `draft/` prompt was filed; this record is the
retroactive ledger entry.)

### Retired draft: `draft/test/autocti_workspace/imaging_ci_start_here_61s.md`

> # autocti_workspace imaging_ci/modeling/start_here.py: the slowest smoke script in the organism (61 s)
>
> Type: test
> Target: autocti_workspace
> Repos:
> - autocti_workspace
> - PyAutoCTI
> Difficulty: medium
> Autonomy: supervised
> Priority: normal
> Status: formalised
> Filed: 2026-09-06
>
> Split out of phase 8 (autolens_workspace#536) because it is the one script on a
> different stack (PyAutoCTI + arcticpy). The ingested record (PyAutoHeart
> `timings/scripts/autocti_workspace.jsonl`, run 33908175450, py3.12) puts
> `imaging_ci/modeling/start_here.py` at **61.0 s** — the slowest smoke script
> anywhere — with `dataset_1d/modeling/start_here.py` 17.0 s and
> `dataset_1d/modeling/features/species_x3.py` 15.9 s behind it; the repo's three
> gate entries total 93.9 s at a 17 s median, against a 5-7 s floor everywhere
> else. The legacy digest (PyAutoHeart `timings/legacy_round_2026-09.md` §3) names
> it as the one genuine per-script bottleneck on the user-facing surface.
>
> Ask: diagnose where the 61 s goes under the smoke profile (arcticpy clocking at
> full size under `PYAUTO_SMALL_DATASETS`? a real search the TEST_MODE bypass does
> not reach? plot/output work the skip variables miss?), then fix it the phase-8
> way — shared machinery (autonerves cap helper, profile override) first, script
> content last and conservative, never the tutorial prose. CI is the acceptance;
> record the before/after rows in the epic ledger.
>
> <!-- was a member of the ci-timing-fast-tests epic (retired COMPLETE 2026-09-06, ledger complete/archive/epics/ci_timing_fast_tests_epic.md); now ordinary backlog -->
