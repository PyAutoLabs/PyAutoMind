# EP: an `InitializerException` in one factor should degrade to a bad projection, not kill the fit

Type: bug
Target: autofit
Repos:
- PyAutoFit
Difficulty: small
Autonomy: safe
Priority: high
Status: formalised
Issue: (none yet — parent report is https://github.com/PyAutoLabs/PyAutoFit/issues/1405)

## The defect

Defect 2 of the two filed on PyAutoFit#1405, split out because it is small,
self-contained, and independently valuable — it is the *most frequent* of the
three EP outcomes after a clean recovery.

In **23% of 30 identical-problem EP runs** (7/30) on a known-answer CPU toy, the
fit **hard-aborts mid-EP** with an `InitializerException` ("initial samples all
have the same figure of merit", `autofit/non_linear/initializer.py:185`). EP
drives one factor into a degenerate all-equal-likelihood state that the
per-factor `DynestyStatic` cannot initialise, and the exception propagates out
of the EP loop and kills the whole graph fit. Everything already computed —
every other factor's converged message, the whole `ep_history` — is lost.

Crash frequency is flat across `max_steps ∈ {20,25,30,50,60}`, so it is not a
long-run accumulation effect; any EP fit can hit it at any sweep.

## The fix

Catch the exception at the per-factor update site inside the EP loop and record
it as a **flagged bad projection / skipped update** (the mechanism EP already
has for `BAD_PROJECTION`), so the sweep continues with that factor's previous
message and the failure is visible in `ep_history.csv` rather than fatal.

Design points to settle while implementing:

- **Which exception surface.** `InitializerException` is the observed one, but
  the general condition is "this factor's optimiser could not run this sweep".
  Decide whether to catch narrowly (`InitializerException`) or introduce a
  factor-update failure category. Prefer narrow first — a blanket
  `except Exception` here would silently swallow real bugs, which
  `feedback_no_silent_guards` says not to do. **This must stay loud**: flagged
  in `ep_history.csv` and surfaced by the diagnostics, never silent.
- **Repeat failures.** If the same factor fails to initialise every sweep, EP
  will converge on a stale message and report success. Add a threshold — N
  consecutive failed updates on one factor should abort *with a clear message
  naming the factor*, which is strictly better than today's raw traceback.
- **Test.** A regression test that drives a factor to an all-equal-FoM state
  and asserts the EP run completes with the failure recorded rather than
  raising. `test_autofit/graphical/` is the home; numpy-only
  (`feedback_no_jax_in_unit_tests`).

## Repro

`complete/2026/07/ep_scale_collapse_assets/ep_toy_diagnostic.py` (self-contained,
numpy-only, minutes on CPU; run from the `HowToFit` repo root). Roughly 1 run in
4 crashes, so loop it:

```bash
cd HowToFit
export NUMBA_CACHE_DIR=/tmp/numba_cache MPLCONFIGDIR=/tmp/matplotlib PYAUTO_SKIP_VISUALIZATION=1
for r in $(seq 1 10); do TOY_MAX_STEPS=20 TOY_JOINT=0 TOY_TAG=rep_$r \
  python3 <path>/ep_toy_diagnostic.py 2>/dev/null | grep OUTCOME; done
```

Full forensics: `complete/2026/07/ep_scale_collapse_assets/EP_TOY_FINDINGS.md`.

## Relationship to the other defect

Independent of the COLLAPSE defect
(`draft/bug/autofit/ep_hierarchical_scale_collapse_moment_match.md`) and safe to
fix first — this one is a robustness fix with no statistical judgment in it,
whereas COLLAPSE needs a moment-match redesign. Fixing this one first also makes
the COLLAPSE work cheaper: 23% fewer wasted runs when gathering statistics over
repeated identical fits.

<!-- filed 2026-07-22 as the wrap-up follow-up of the ep-hierarchical-scale-collapse
task (report-only; PyAutoFit#1405). Origin: slope_hierarchy#1 goal 2. -->
