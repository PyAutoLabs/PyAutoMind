- shipped: 2026-09-01 — PyAutoFit main `c06f671a`, merged via
  https://github.com/PyAutoLabs/PyAutoFit/pull/1556 (closes PyAutoFit#1552).
- classification: bug (PyAutoFit) — batch 2026-08-31-pm member autofit-multistart-iterations;
  phase 1 (library) of the two-phase prompt.
- summary: `iterations_per_quick_update` / `live_visual_update` are now live for the
  MultiStart gradient family — driven from the host-Python step loop (one count per
  gradient step, deliberately, not per batched evaluation), with LiveDisplay /
  BackgroundQuickUpdate set up through the same Fitness path as every other search; the
  startup message states the unit honestly and the EXEMPT entry is removed from
  test_quick_update_wiring.py. Merged last of the shift's PyAutoFit trio: rebased over
  #1554/#1555 and flipped #1555's `quick_update_count == 0` inertness tripwire to `> 0`
  exactly as that tripwire's comment demanded (162 tests green locally, CI 4/4). The
  member parked at ship (supervised) on #1552; the PR was opened from the parked branch
  at the human's request and accepted in the review.
- lifecycle: dispatched 18:53Z as an unattended batch member; prompt retired from draft/
  (the park never advanced it); phase 2 (autolens_workspace prose retune + AST guard)
  split out to draft/docs/autolens_workspace/multistart_quick_update_workspace_leg.md;
  accepted 2026-09-01 15:13; recorded 2026-09-01.

## Original prompt

# MultiStartGradient searches ignore iterations_per_quick_update and live_visual_update while announcing the cadence…

Type: bug
Target: PyAutoFit
Repos:
- PyAutoFit
- autolens_workspace
Difficulty: large
Autonomy: supervised
Priority: normal
Status: formalised
Consequence: glance
Witness: a MultiStartProdigy fit run with a finite iterations_per_quick_update writes one fit.png per cadence boundary under the search output directory (counted by a test that drives the step loop and asserts the number of perform_quick_update calls), and multi_start_gradient/search.py is removed from the EXEMPT map in test_autofit/non_linear/search/test_quick_update_wiring.py rather than left in it; on the workspace side, an AST guard asserts no MultiStart* call site in scripts/ passes a kwarg the search does not honour.
Review-minutes: 3
Unattended: ready

MultiStartGradient searches ignore iterations_per_quick_update and live_visual_update while announcing the cadence in the startup log

Type: bug
Target: autofit
Difficulty: large
Autonomy: supervised
Priority: normal
Witness: a MultiStartProdigy fit run with a finite iterations_per_quick_update writes one fit.png per cadence boundary under the search output directory (counted by a test that drives the step loop and asserts the number of perform_quick_update calls), and multi_start_gradient/search.py is removed from the EXEMPT map in test_autofit/non_linear/search/test_quick_update_wiring.py rather than left in it; on the workspace side, an AST guard asserts no MultiStart* call site in scripts/ passes a kwarg the search does not honour.

## What was observed

Running autolens_workspace scripts/imaging/start_here.py logs:

    2026-08-31 11:50:25,370 - autofit.non_linear.search.abstract_search - INFO - On-the-fly updates of the maximum likelihood model every 50 iterations.

50 looks alarmingly frequent for a search whose whole budget is n_steps=300. It is not: nothing fires, so the cadence costs nothing. Raising it to 1000 would change nothing either.

## Why nothing fires

AbstractMultiStartGradient builds its Fitness (PyAutoFit autofit/non_linear/search/mle/multi_start_gradient/search.py:816) WITHOUT iterations_per_quick_update and WITHOUT live_visual_update, deliberately. fitness.call is traced inside jax.jit(jax.vmap(...)), so the Python-side counter in Fitness.manage_quick_update would run once at trace time and never again. The exemption is recorded in the EXEMPT map of test_autofit/non_linear/search/test_quick_update_wiring.py and in PyAutoFit#1433, which shipped iterations_per_log (default 10) as the replacement progress channel for these four searches.

Consequences for MultiStartProdigy / MultiStartAdam / MultiStartADABelief / MultiStartLion: no periodic fit.png, no live matplotlib window in script mode, no self-refreshing Jupyter cell, and no runtime cost from the setting.

## Defect 1 - the startup message is a false claim (PyAutoFit)

AbstractSearch emits the "On-the-fly updates ... every N iterations" line (autofit/non_linear/search/abstract_search.py:476-488) from the base class, unconditionally, whether or not the concrete search wires the cadence through to its Fitness. The wiring test's own comment already names this failure mode: "once the cadence is announced in the startup log, a missing forward turns a dead feature into a false claim in the CLI."

Two silent kwargs sit behind it: passing iterations_per_quick_update or live_visual_update to a MultiStart* search is accepted, stored, reported in the log, and then ignored.

## Defect 2 - the workspace documents behaviour that does not happen

Three scripts pass both dead kwargs to MultiStartProdigy:

- scripts/imaging/start_here.py (iterations_per_quick_update=50, live_visual_update=True)
- scripts/interferometer/start_here.py
- scripts/multi_galaxy/start_here.py

Each carries an __Iterations Per Update__ and a __Live Visual Update__ prose section describing a ~10 second update every 50 gradient steps, a matplotlib window that opens automatically in script mode, and a Jupyter cell that refreshes in place. None of that happens.

The prose is also wrong on the unit, even for the searches where the machinery IS live: Fitness.manage_quick_update increments quick_update_count by the batch size (fitness.py:607, total_updates = log_likelihood.shape[0]), not by one per step. With n_starts=48, iterations_per_quick_update=50 would fire roughly every SECOND gradient step, not every fiftieth.

The same __Live Visual Update__ prose appears in ~14 workspace scripts, but only the three above attach it to a MultiStart search - the rest use Nautilus, where the quick-update machinery is genuinely live and the prose is correct.

## Asked-for fix

Wire real quick updates into the multi-start searches rather than only removing the false claim. The step loop in AbstractMultiStartGradient._fit is plain host Python and already forces a device sync every step, so a counter there works where the traced one cannot - this is the same seam iterations_per_log already uses.

1. PyAutoFit - honour iterations_per_quick_update in AbstractMultiStartGradient's step loop: at each cadence boundary, build the instance from the current global-best parameters and call analysis.perform_quick_update, and support live_visual_update through the same LiveDisplay / BackgroundQuickUpdate path Fitness uses. Decide the unit deliberately and document it (a gradient step is the natural unit here, which differs from the batch-size counting Fitness does - the two must not silently disagree). Remove multi_start_gradient/search.py from the wiring test's EXEMPT map once it honours the kwarg.
2. PyAutoFit - make the startup message honest for any search that still does not wire the cadence, and warn when an ignored kwarg is passed, pointing at the channel that does work.
3. autolens_workspace - once the library honours it, re-tune the three scripts to a sane cadence in the new unit (50 gradient steps is reasonable if the unit is steps; it is far too frequent if the unit stays batch-counted) and rewrite the __Iterations Per Update__ and __Live Visual Update__ prose so it describes what the search actually does, including how it relates to iterations_per_log.

Expect a phase split: library first (quick-update wiring, then the honest-message / warning leg), workspace follow-up once the unit and the kwarg semantics are settled.

<!-- formalised by the Intake (Conception) Agent on 2026-08-31 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs-autolens-workspace/30583c25-85fe-4c6a-bd98-cd151efd1d41/scratchpad/intake_raw.md -->
