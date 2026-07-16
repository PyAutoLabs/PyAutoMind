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
