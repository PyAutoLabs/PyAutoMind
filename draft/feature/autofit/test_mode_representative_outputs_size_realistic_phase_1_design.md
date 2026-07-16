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
