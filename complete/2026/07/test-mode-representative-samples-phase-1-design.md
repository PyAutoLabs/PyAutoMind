## test-mode-representative-samples-phase-1-design
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1378 (CLOSED)
- completed: 2026-07-16
- epic: test_mode_representative_outputs_size_realistic phase 1/4 (umbrella in draft/feature/autofit/; phases 2-4 filed alongside)
- repos: PyAutoFit, PyAutoConf (design-only — no source edits, no PRs, no worktree)
- notes: D1-D4 locked on #1378 for phase 2 to implement verbatim. D1: PYAUTO_TEST_MODE_SAMPLES env var, default 4, N<4 raises; accessor in autoconf/test_mode.py re-exported via the existing autofit/non_linear/test_mode.py shim — PyAutoConf IS in scope, its PR merges first. D2: N==4 keeps today's literal branch byte-identical; N>4 = vectorized numpy synthesis (rng seed 0, prior-median row 0, logL_i = best - i best-first, weights ∝ exp(-i/(N/10)) normalized) fed into the SAME production path Nautilus uses (arrays → .tolist() → Sample.from_lists → SamplesPDF → write_table), so CSV layout/byte size representative by construction. Parity target measured from slam-resume-profiling: source_lp[1] = 10,187 rows × 21 cols = 9.07 MB (~890 B/row). KEY FIND: samples_above_weight_threshold_from pruning is ONLY called from updater.py (real-run perform_update) — the bypass write path never prunes; the exp weight profile keeps w_min ≈ (10/N)e^-10 ≥ 4.5e-10 > threshold 1e-10 for N ≤ 1e5 so later threshold-applying loads are safe too (cf. #1375 2-sample pruning incident). D3: 7-item numpy-only phase-2 test list (exact 4-sample back-compat, summary/chaining, save-load round trip, aggregator+database at N=1000, functional N=50k without hard timing asserts, ValueError at N=3). D4 recorded-not-solved: no search_internal checkpoint, adapt-image FITS prior-median values, latents auto-skipped, log_evidence stubbed — timing-honest not science-honest. Side benefit: non-degenerate covariance.csv at N>4 (today's 4 near-collinear samples are borderline singular). SEQUENCING: phase 2 blocked by aggregator-sqlite's PyAutoFit claim (#1377 in flight; #1376 merged 2026-07-16 14:14 but the Phase D follow-on holds the worktree).

## Original prompt

# Test-mode representative outputs — Phase 1: design

Type: feature
Target: autofit
Repos:
- PyAutoFit
- PyAutoConf
Difficulty: small
Autonomy: supervised
Priority: normal
Status: formalised

Phase 1 of 4 of `draft/feature/autofit/test_mode_representative_outputs_size_realistic.md`
(the parent umbrella — read it first; its scoping notes were verified against source
2026-07-16). Design only — **no source edits**; the deliverable is a set of locked
decisions recorded on this phase's GitHub issue, which phase 2 implements verbatim.

## Decisions to lock

- **D1 — knob.** Confirm `PYAUTO_TEST_MODE_SAMPLES=N` (env var, default 4 = today's
  behaviour, so nothing changes for existing users/tests) and where it is read:
  accessor next to `test_mode_level()` in @PyAutoConf `autoconf/test_mode.py` vs
  reading it locally in @PyAutoFit. Decide whether PyAutoConf is touched at all.
- **D2 — synthesis scheme.** Exact vectorized recipe `_build_fake_samples` uses at
  large N: parameter scatter around the prior median (deterministic seed — where does
  the seed live?), monotone plausible log-likelihoods, valid normalized weights, and
  the samples.csv column layout/dtypes so row count *and byte size* match a production
  Nautilus SLaM stage (N ~ 10k–100k).
- **D3 — downstream contract.** Enumerate what must keep working on the synthetic set
  and how phase 2 tests each: `samples.summary()` quantiles, search chaining
  (`result.model` / `result.instance`), aggregator scrape, database load, and the
  existing 4-sample multi-batch structural guarantees at large N.
- **D4 — representativeness limits.** Record (not solve) the known deltas from a
  production resume: single bypass likelihood call leaves no realistically-sized
  search-internal state; adapt-image FITS values come from the prior-median model
  (size right, values wrong); test mode auto-skips latents.

## Exit criteria

D1–D4 posted on the issue as locked decisions; phase 2 unblocked with no open design
questions.
