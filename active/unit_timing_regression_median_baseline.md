# Heart unit-timing regression detector: rolling-median baseline and run-speed normalisation (false 3× NSS / EP flags)

Type: bug
Target: pyautoheart
Repos:
- PyAutoHeart
Difficulty: medium
Autonomy: supervised
Priority: medium
Status: formalised
Consequence: glance
Witness: Replaying `timings/unit/PyAutoFit.jsonl` through the detector no longer flags `test_nss_fit_with_assertions_runs_under_jit` (5.45 s vs its ~6 s median) nor the 10-16 3.12 graphical/EP set, while a synthetic 4× slowdown of one test in an otherwise-normal run is still flagged red. Thresholds (1.5× / 3×) unchanged.
Filed: 2026-10-16

## Finding (health session 2026-10-16, read-only diagnosis)

The 3.56× "regression" compares against a single fast-runner sample: the NSS test (added 10-08, aeadaae48) ran 7.29/6.24/6.97/6.15/5.65/6.37/4.86 s; the 1.532 s baseline appears once (10-15 3.13, 9c78451e). Locally it takes 5.7–6.1 s. Graphical/EP tests move together ~2.1× with the runner (10-15 vs 10-16 3.12; same jax 0.11.2/blackjax 1.7.1/numpy 2.5.4, same runner image) — runner noise, no code or dependency change.

## Proposed fix

Baseline = rolling median over the last N comparable runs (not latest/fastest single run), and normalise each test by a run-speed factor (e.g. median ratio across the suite, or a fixed reference test) before applying the unchanged 1.5×/3× thresholds. This is a detector correctness fix, not a threshold change.

Issued: 2026-10-17
Issue: https://github.com/PyAutoLabs/PyAutoHeart/issues/304
