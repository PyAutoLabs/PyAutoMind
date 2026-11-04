# MultiStartResumeNaNCounters.py creeps past the 300s smoke cap (per-update plotting cost)

Type: bug
Target: health_fixes
Themes:
- ci-smoke
- autofit
Difficulty: small
Autonomy: supervised
Priority: high
Status: formalised
Consequence: judge
Filed: 2026-11-04 (from the /health dashboard review)

## Finding

Heart `release:361c87850b823009` (the only release-readiness finding, verdict YELLOW):
workspace validation not passing — 0 failed, 1 timeout, PyAutoHeart Workspace Smoke
run 41432188469 (2026-11-02): `autofit_test scripts/searches/MultiStartResumeNaNCounters.py`
`TIMEOUT (304s)`. Every other script in the `autofit_test, searches` shard passed.

## Diagnosis so far (2026-11-04)

- **Not a hang, not a flake: a steady creep.** Same script in the weekly Workspace Smoke:
  164.2s (run 38964028250, 2026-10-16) → 225.3s (run 40381428052, 2026-10-26) →
  TIMEOUT at the 300s cap (run 41432188469, 2026-11-02).
- **Reproduces locally** on PyAutoFit main dbf05d793 (laptop, Py3.13): >400s, killed
  before even the uninterrupted reference arm finished.
- **Where the time goes.** The script runs `af.MultiStartAdam(n_starts=12, n_steps=400,
  iterations_per_full_update=2, resurrect=False)` in ~2.5 child searches (reference,
  killed, resumed). `iterations_per_full_update=2` is there so checkpoints are written
  mid-run (the kill needs something to resume from). Each full update costs ~2.5–5s on a
  1D Gaussian, almost entirely matplotlib: it writes 9 PNGs every update
  (`image/search/{figure_of_merit_vs_iteration, log_likelihood_vs_iteration{,_last_50_percent,_log_y},
  subplot_parameters{,_last_50_percent,_log_y}}.png`, plus `image/data.png`,
  `image/model_fit.png`). 400/2 = 200 updates ≈ 8+ min per child. cProfile of 54s:
  ~13s tick layout, ~7s PNG encode, JAX/likelihood negligible. (The plotting runs on a
  thread, so cProfile shows no autofit caller frames.)
- Coupling to fix: the script needs *checkpoint* cadence, not *visualization* cadence.
  Today one knob (`iterations_per_full_update`) drives both.

## Fix-locus question for the Bug Agent

Prefer a library fix. Candidates (decide, don't do all):
1. **Library:** decouple checkpoint cadence from the full-update visualization cadence for
   MultiStartGradient (or throttle the search-progress plots, e.g. only re-render them
   every N full updates / at the end), so a test that needs frequent checkpoints does not
   pay 9 PNG renders per 2 steps. This is a real user cost too: any user setting a small
   `iterations_per_full_update` for safety pays it.
2. **Test config:** autofit_workspace_test is a test workspace (not user-facing
   documentation); disabling search plots for this script, or a smaller `n_steps`,
   would be legitimate only if (1) is judged out of scope — never raise the cap, never
   add a `no_run`/SLOW entry to make the verdict green.

## Validation

- Script passes well under 300s locally and in a dispatched Workspace Smoke
  (`autofit_test, searches` shard), with the same equality assertion still meaningful
  (non-zero NaN counters at kill, resumed == reference).
- Then refresh Heart (tick + publish) and confirm `release:361c87850b823009` clears.

## 2026-11-04 — human re-scope: the cadence of 2 is the defect (script-only fix)

Human: "the actual problem is the script shouldn't be using a value of 2 … can we have the
intended behaviour and test run for a normal value." Measured locally (PyAutoFit main dbf05d793):
`iterations_per_full_update=100` → PASS 34.5s, killed at step 100 with value-NaN 201 / grad-NaN 1
(both non-zero), resumed == uninterrupted (142 steps, 403/9). 50 → PASS 53.7s but grad-NaN 0 at the
kill. Fix = script change 2 → 100; the library `checkpoint_interval` idea (candidate 1) is DROPPED
as unnecessary. Issue: https://github.com/PyAutoLabs/autofit_workspace_test/issues/117
