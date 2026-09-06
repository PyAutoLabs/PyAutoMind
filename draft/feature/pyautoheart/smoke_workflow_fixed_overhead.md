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
