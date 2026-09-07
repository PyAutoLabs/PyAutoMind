# The smoke gate's fixed per-leg overhead, measured and trimmed: depth-1 clones, a pip wheel cache, `setup_s` as data

PyAutoHeart#218 → `551f165`, closing PyAutoHeart#216, merged 2026-09-07, stacked on #217.
Fable-planned from a web session (no task worktree); implemented by an Opus subagent under the
delegation ladder; workflow and Heart-side Python only, no library source changed.

- issue: https://github.com/PyAutoLabs/PyAutoHeart/issues/216
- completed: 2026-09-07
- library-pr: https://github.com/PyAutoLabs/PyAutoHeart/pull/218

## What shipped
- **Measured first** (12 legs, six autolens_workspace_test runs, Actions job-step timestamps,
  table on the issue): `setup_s` (job start → first script) 104 s mean = 22.6% of the job;
  install 83.6 s (80%), chain clone 16.5 s (16%), everything else ~4 s. The legacy digest's
  "~2–3 minutes per leg" was an over-estimate; the measured range is 86–119 s.
- `smoke-tests.yml`: `--depth 1` on the chain + PyAutoHands clones and on the matching-branch
  fetch, with the fallback as `fetch --depth 1 origin "$BRANCH"` + `checkout -B "$BRANCH"
  FETCH_HEAD` (a shallow clone is single-branch, so plain `checkout "$BRANCH"` fails); an
  `actions/cache@v4` on `~/.cache/pip` keyed on the dependency declarations' content + python
  leg + epoch salt, prefix fallback, `continue-on-error`; two non-fatal `Mark …` steps the
  recorder differences into `setup_s` in the sidecar (`null` when a mark is missing).
- Ingest/record/board: `setup_s` through `parse_cache_state`/`cache_view`, recorded on
  `timings/scripts/<repo>.jsonl` lines beside `cache`, appended as `· setup Ns` to the board's
  per-repo line only when known. Runner command byte-identical. Tests 924 → 939.
- Reported, not done (on the issue): `--no-deps` for the chain (15–30 s, moves the intra-family
  floor guarantee into eleven workspace epilogues), prebuilt wheels (10–20 s, a second artefact
  per library), dropping `--upgrade pip setuptools wheel` (3–6 s, the line that absorbs
  runner-image drift).

## Key traps / findings
- A shallow source install still stamps `9999.0.0.dev0`: `setup.py`'s `VERSION` default wins over
  the `[tool.setuptools_scm]` block, checked by installing the family from shallow clones in the
  session venv — so depth-1 clones do not break the intra-family `>=` floors.
- setup-python's `cache: pip` was the wrong tool here: it cannot be non-fatal, cannot carry the
  epoch salt, and hard-errors on a `cache-dependency-path` that matches no file while the chain is
  caller-supplied text. The libraries declare dependencies in `pyproject.toml`, not
  `requirements*.txt`.
- `setup_s` is measured from the `smoke` job's first step, so it excludes the `changes` job and
  runner-provisioning slack: "what this workflow spends", not "what the PR waits".

## Follow-ups
- Read `setup_s` back from `timings/scripts/<repo>.jsonl` after the callers' next `main` runs and
  put the before/after beside the 104 s baseline; the ceiling if both levers land fully is
  ~15–25 s per leg.
- Each report-only lever becomes its own prompt if wanted; `--no-deps` is the one worth the most.

## Original prompt

# Trim the fixed per-leg overhead of the reusable smoke workflow: measure the steps, then depth-1 clones and a pip cache

Type: feature
Target: PyAutoHeart
Repos:
- PyAutoHeart
Difficulty: medium
Autonomy: safe
Priority: high
Status: formalised
Consequence: glance
Witness: a wiring test pins `--depth 1` on every chain clone and a pip cache step in smoke-tests.yml, and the before/after per-step table on the issue (same runner class, Actions API) shows clone+install per leg below the measured baseline
Review-minutes: 3
Unattended: ready
Filed: 2026-09-06
Issued: 2026-09-06

The legacy digest (PyAutoHeart `timings/legacy_round_2026-09.md` §1) measures
the two `_test` flagships spending **~2–3 minutes per leg on checkout + install
before the first script runs** (autogalaxy_test 714 s gate vs 537 s of scripts;
autolens_test 552 s vs 435 s). That cost is identical on every PR, is now about
a quarter of each `_test` gate, and becomes the floor as phases 5–8 shrink the
scripts. Nobody has measured it step by step.

**What the workflow does today** (`PyAutoHeart/.github/workflows/smoke-tests.yml`):
full `git clone` of every dependency-chain library plus PyAutoHands (no
`--depth`), `actions/setup-python@v5` with **no `cache: pip`** (while
`lib-tests.yml` has it), `pip install --upgrade pip setuptools wheel` then the
chain from source, plus the workspace's own epilogue.

**Do.**
1. **Measure first.** Pull the per-step durations of the last N runs for the
   ten caller repos (the Actions jobs API, via the same `HEART_TIMINGS_TOKEN`
   path the ingester uses, or a one-off read) and write a short table into the
   issue: checkout, chain clone, setup-python, arcticpy, install, cache
   restore, dataset restore, scripts, cache save. This is the number the change
   is judged against; if install is not the dominant fixed cost, stop and
   report.
2. **Depth-1 clones** for the chain: `git clone --depth 1` with the
   matching-branch fallback preserved (`ls-remote --exit-code --heads` then
   `fetch --depth 1 origin <branch>`). The dataset-cache key hashes each dep's
   `rev-parse HEAD`, which a shallow clone still answers.
3. **pip cache**: `cache: pip` on `setup-python` keyed on the chain's
   requirement files (`cache-dependency-path`) — or an explicit `actions/cache`
   on `~/.cache/pip` if the requirements live outside the caller's checkout.
   Source installs of the PyAuto* libraries themselves stay from source; the
   win is the third-party wheels (jax, numpy, scipy, matplotlib, astropy).
4. Consider, and report on rather than do unless the measurement says so:
   `pip install --no-deps` for the chain once deps are installed once; a
   prebuilt wheel step; skipping `--upgrade pip setuptools wheel`.
5. Record the fixed overhead as data: add a `setup_s` (time from job start to
   first script) to the `cache_state.json` sidecar or the smoke-timings
   rollup so the board can show scripts vs overhead per leg; `ci_timing`'s
   gate wall already carries the total.

**Guard.** The runner command stays byte-identical; every new step
`continue-on-error`; the arcticpy path (autocti callers) untouched unless the
measurement names it. Behaviour of the matching-branch checkout of the chain
must be preserved exactly — that is how a library PR is tested against its
workspace.

**Validation.** PyAutoHeart suite + a wiring test pinning the clone flags and
the cache step; before/after per-step table on one `_test` repo from the
Actions API on the same runner class (never local numbers).
