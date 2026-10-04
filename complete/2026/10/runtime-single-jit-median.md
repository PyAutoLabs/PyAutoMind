## runtime-single-jit-median
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/371
- completed: 2026-10-04
- epic: point-source-cpu-speed
- workspace-pr: https://github.com/PyAutoLabs/autolens_profiling/pull/374
- autolens_profiling#374 merged 2026-10-04T20:41Z (head 87a7fcc0, merge 4d9e6506) via human /prm (Heart RED development override). It ships option (a) of the PyAutoPulse contract `tasks/runtime_cell_single_jit_gpu_warmup.md`:
  - `timing.py`: adds `steady_median_profile` (≥ 5 warm calls, then N individually timed calls; returns median/p10/p90) and an opt-in `jit_profile(median_n_warm=, median_n_timed=)`;
  - `source_plane_solved.py`: the witness cell writes `full_pipeline_single_jit_median_ms` / `_p10_ms` / `_p90_ms` beside the unchanged `full_pipeline_single_jit`;
  - `build_dashboard.py`: labels GPU first-block rows "first block after compile" and shows the steady median where a row carries it. No row is re-based.
- Validation: 9 new tests, and pytest gave 1029 passed. The local CPU witness gave single_jit 0.417 ms vs steady median 0.388 ms. No HPC job was run.
- **Scope merged ≠ scope filed.** Not shipped:
  - the four imaging release-sweep cells (the contract's "Reach") are not wired;
  - the A100 witness, where the median should agree with job 366914's 0.267 ms to within p10–p90, runs at the next release sweep.
  Both are re-filed as `draft/bug/autolens/runtime_single_jit_median_reach_and_a100_witness.md`.

## Original prompt

# Runtime cells' A100 `single_jit` warm-up: option (a), a steady median beside the existing statistic

Type: bug
Target: autolens_profiling
Repos:
- autolens_profiling
Themes:
- profiling
- jax
Difficulty: small
Autonomy: supervised
Priority: low
Consequence: judge
Epic: point-source-cpu-speed
Issued: 2026-10-04

Contract: the PyAutoPulse task `organs/PyAutoPulse/tasks/runtime_cell_single_jit_gpu_warmup.md`
(https://github.com/PyAutoLabs/PyAutoPulse/blob/main/tasks/runtime_cell_single_jit_gpu_warmup.md).

## Human decision (2026-10-04, in-session)

The original request, verbatim: "do the proposed priority order stuff, all of it". The decision recorded
with it is **option (a)**:
- In the shared `jit_profile` helper, add ≥ 5 warm calls and a median-of-N field (with p10/p90),
  for example `full_pipeline_single_jit_median_ms`.
- Put it **beside** the existing `full_pipeline_single_jit`, which is kept byte-for-byte for
  continuity.
- Dashboard: label the existing A100 field "first block after compile" where it is headlined.
  Committed rows are not re-based.
- Add or extend a unit test for the helper.
- No HPC jobs. A local CPU run of one light cell may witness the new field.

## Scope

1. `scripts/misc/likelihood_breakdown/timing.py`:
   - add `steady_median_profile`, which runs ≥ 5 warm calls and then N individually timed calls, and
     returns the median, p10 and p90;
   - add opt-in `jit_profile(..., median_n_warm=, median_n_timed=)`. It runs after the existing
     statistic and records no timer section, so the old number is unchanged.
2. `scripts/point_source_source/likelihood_runtime/source_plane_solved.py`, the witness cell: write
   `full_pipeline_single_jit_median_ms`, `_p10_ms` and `_p90_ms`, plus the protocol, beside
   `full_pipeline_single_jit`.
3. `scripts/misc/tooling/build_dashboard.py`: on GPU rows headlined by `full_pipeline_single_jit`, show
   "first block after compile". Show the steady median where a row carries it.
4. Unit tests for the helper and the dashboard label. Regenerate, lint, and open the PR.

The four imaging release-sweep cells (the contract's "Reach") are not wired in this PR. They follow
once the source-plane A100 witness is re-run at the next release sweep.
