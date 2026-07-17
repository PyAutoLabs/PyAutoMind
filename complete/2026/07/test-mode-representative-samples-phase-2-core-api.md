## test-mode-representative-samples-phase-2-core-api
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1379 (CLOSED)
- completed: 2026-07-17
- epic: test_mode_representative_outputs_size_realistic phase 2/4 (phase 1 record: [[test-mode-representative-samples-phase-1-design]]; phases 3+4 in draft/feature/autofit/)
- library-pr:
  - https://github.com/PyAutoLabs/PyAutoConf/pull/126 (merged 2026-07-17, FIRST — accessor)
  - https://github.com/PyAutoLabs/PyAutoFit/pull/1381 (merged 2026-07-17)
- repos: PyAutoConf, PyAutoFit (worktree ~/Code/PyAutoLabs-wt/test-mode-representative-samples)
- notes: PYAUTO_TEST_MODE_SAMPLES=N live — bypass (PYAUTO_TEST_MODE=2/3) writes N size-realistic fake samples; default 4 byte-identical (literal branch untouched + pinned by test); N<4 raises. Implemented D1-D4 from #1378 verbatim: autoconf accessor test_mode_samples() re-exported via the existing autofit shim; N>4 = vectorized numpy (default_rng(0), prior-median row 0, logL_i=best-i, weights ∝ exp(-i/(N/10)) normalized) → production Sample.from_lists path. Evidence: PyAutoConf 138p; PyAutoFit full 1493p/1s; e2e DynestyStatic af.ex.Gaussian at N=10k → 1.7s wall, samples.csv 10,000 rows/1.31MB, min weight 4.5e-8 > 1e-10 threshold, chaining intact. Shipped through Heart RED on human ack 2026-07-17 (5 pre-existing unrelated reasons: PyAutoLens uncommitted source, workspace validation 3-failed 2026-07-09, 58 stale parked scripts, manifest drift ×6, release validation stale 5 libs); merged by human same morning. NICE SIDE EFFECT: at N>~11 max weight <0.99 so SamplesPDF.pdf_converged=True → real weighted-quantile median_pdf path runs in test mode (4-sample branch keeps max-likelihood fallback); covariance.csv non-degenerate. TRAP AVOIDED: weight pruning is updater.py-only (bypass write never prunes) but the exp(-i/(N/10)) floor ≈ (10/N)e^-10 was chosen ≥ 4.5e-10 at N ≤ 1e5 so later threshold-applying LOADS keep the full set (cf. #1375 2-sample incident). CONCURRENCY TRAP: mind_commit_guard blocked a bare-path commit, and an uncommitted active.md edit was clobbered by another session's morning sync — re-apply-and-commit-immediately is the pattern. NEXT: phase 3 recipe naturally lands in the PAUSED slam-resume-profiling task (#70, harness already test-mode-ready, owns the autolens_profiling pipeline_resume subtree) — consider resuming #70 as phase 3 instead of a fresh conflicting claim; phase 4 docs after.

## Original prompt

# Test-mode representative outputs — Phase 2: core API

Type: feature
Target: autofit
Repos:
- PyAutoFit
- PyAutoConf
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: formalised

Phase 2 of 4 of `draft/feature/autofit/test_mode_representative_outputs_size_realistic.md`.
Implements the D1–D4 decisions locked in phase 1 (`..._phase_1_design.md`) — do not
reopen them. Blocked until phase 1's decisions are posted.

## Scope

- Implement the sample-count knob (per D1) — default 4, so existing behaviour is
  byte-identical when the knob is unset. Touch @PyAutoConf only if D1 placed the
  accessor next to `test_mode_level()` in `autoconf/test_mode.py`.
- Extend `_build_fake_samples` in @PyAutoFit
  (`autofit/non_linear/search/abstract_search.py`) to synthesize N samples per the
  D2 recipe. **Vectorized numpy** — no per-Sample python loops; N=50k must generate
  in seconds or the feature defeats its purpose.
- Unit tests for the D3 downstream contract at large N: `samples.summary()`
  quantiles, `result.model` / `result.instance` chaining, multi-batch structural
  guarantees; plus default-unset back-compat (exactly today's 4 samples). Library
  unit tests are numpy-only — no JAX.
- Aggregator scrape / database load on a large-N synthetic output verified as part
  of the ship gate (workspace_test if a library unit test can't cover it cleanly).

## Ship

`ship_library`: PyAutoFit PR (+ PyAutoConf PR if touched, merged first per the
dependency graph). The PR's API-change summary unblocks phase 3.
