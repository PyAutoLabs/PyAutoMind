## release-advisory-tier-slow-scripts
- issue: https://github.com/PyAutoLabs/PyAutoHeart/issues/74 (closed)
- completed: 2026-07-14
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace_test/pull/169 (merged, squash) + https://github.com/PyAutoLabs/autogalaxy_workspace_test/pull/73 (merged, squash)
- repos: autolens_workspace_test, autogalaxy_workspace_test
- summary: mode=release integrate kept going RED not on bugs but on a shifting perf-flake tail of slow real-search scripts timing out near the per-script cap (PyAutoHeart#74, follow-up to release-tail epic). FIRST built a full advisory tier (advisory.yaml = run-but-de-gate; new TIMEOUT_ADVISORY status in Build; readiness YELLOW-not-RED in Heart) across Heart+Build+3 workspaces, verified + shipped to 5 PRs under corrective-red --auto. Human then judged it over-engineered: advisory's premise (no_run SLOW-skips erode coverage / whack-a-mole) is already bounded by the maintainer's hygiene sweep of no_run, and for reliably-too-slow scripts a skip ≡ an advisory-timeout. REVERTED fully (closed all 5 PRs, deleted branches, removed mechanism) and instead SLOW-no_run'd the 17 flaky real-search scripts (jax_likelihood_functions interferometer/datacube/multi + jax_grad, .py-anchored + verified 1:1) in the two _test workspaces. EXCLUDED cpu_fast_modeling (singular fix PyAutoArray#388, not a timeout) + autolens shapelets (uncertain; autogalaxy already agw#131). Accepted trade-off: flaky set shifts run-to-run → next handful added via hygiene, not an automated tier. Lesson: prefer the lean existing lever when the user hygiene-manages the debt bucket (feedback_prefer_lean_existing_lever). Merged by human direction; Heart stays RED on unrelated PyAutoArray branch reason. See project_release_advisory_tier_slow_scripts.

## Original prompt

# mode=release should tier slow real-search scripts as advisory, not RED-block on the perf tail

Type: feature
Target: PyAutoHeart
Repos:
- PyAutoHeart
- PyAutoBuild
Difficulty: medium
Autonomy: supervised
Priority: high
Status: formalised

The 2026-07-13 release-validation burn-down (PyAutoHeart#72) fixed every real
correctness bug in the tail (A–H + the jax_grad config gap). But the
`workspace-validation.yml mode=release` integrate stage **still cannot reach a clean
verdict**, because it runs the FULL script set — including a *population* of genuinely
slow **real-search** scripts (`PYAUTO_TEST_MODE=0`/`1` real Nautilus fits +
finite-difference JAX gradients) that flake around the per-script timeout cap. The
failure set **shifts run to run**:

- re-val #3 → shapelets, jax_grad×2, multi/delaunay_mge
- re-val #4 (after fixing those) → cpu_fast_modeling, interferometer datacube/delaunay,
  interferometer mge/slam, multi/shared_preloads — **all of which passed in #3**
  (`shared_preloads` literally flip-flopped).

Raising `BUILD_SCRIPT_TIMEOUT` (300→1800) and adding `no_run` SLOW-skips one script at
a time does **not converge** — each run surfaces a different handful of borderline
scripts, and de-gating them individually is whack-a-mole that also erodes coverage.

**The structural problem:** `mode=release` gates a RELEASE on the *full-set* run, but a
big fraction of that set is genuinely-slow real work whose pass/fail near a per-script
cap is nondeterministic (CI runner load). Correctness and perf-flakiness are conflated
into one RED. (This is the "mode=release full-tail RED policy" question first raised on
#72 comment-4966797130.)

**Proposal — tier the run so integrate gates on CORRECTNESS, not the perf tail:**
- Introduce a **slow/advisory tier** for known-slow real-search scripts (a
  `slow: true` marker in `config/build/no_run.yaml` or a companion `slow.yaml`, or a
  duration threshold): these still RUN and are reported, but a timeout on an
  advisory-tier script is **advisory (yellow)**, not an integrate-RED.
- Alternatively/additionally, run the slow tier as a **separate off-critical-path job**
  with a large budget (e.g. 3600s+), so a slow-tier flake never blocks the release
  verdict while still surfacing regressions.
- A **timeout on a non-advisory script is still RED** (a script that should be fast
  timing out IS a signal). Only the declared-slow population is de-gated.
- Keep it loud: advisory failures surface in the report + Heart's YELLOW reasons
  (same spirit as the existing SLOW/NEEDS_FIX banners), so they're a tracked backlog,
  not silently hidden — the durable speedups are the Profiling Agent's job
  (`draft/feature/profiling/profiling_agent_jax_compile_time_scope.md`).

Outcome: after the real bugs are fixed, `mode=release` reaches GREEN/YELLOW on
correctness and the release-decision gate stops being held hostage by real-search
perf-flakes. Design in PyAutoHeart (`workspace-validation.yml` + `heart/validate.py`
tiering) with the runner support in PyAutoBuild (`run_python.py`/`build_util.py`).
Cross-ref [[project_release_2026_07_13_blocked_3bugs]] and PyAutoHeart#72.
