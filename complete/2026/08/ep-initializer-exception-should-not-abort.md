An `InitializerException` in one EP factor no longer kills the whole graph fit —
it degrades to that factor's previous message and the sweep continues, with the
failure recorded. Defect 2 of PyAutoFit#1405 ("do first").

- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1405 (umbrella — stays
  **open**; follow-up 2, the scale-collapse basin, is untouched). No separate
  issue was cut: the release-leg failure that started this was folded in rather
  than filed as a fourth EP issue.
- pr: PyAutoFit#1454 (`f02ea7e`) — merged; unittest 3.12/3.13 + docs green.
  Also HowToFit `claude/ep-nan-likelihood-bug-ugkj79` (no_run NEEDS_FIX entry).
- shipped: `InitializerException` added to `factor_step`'s caught tuple;
  `max_consecutive_failures` (default 3, a `run` kwarg so it reaches the
  declarative layer via `optimise(**kwargs)`) stops sweeping a factor that
  raises every time; a `STALE FACTORS` warning names any factor that raised and
  never once updated, logged **and** written into `ep_diagnostics.results`.

## Traps — the expensive part, worth reading before touching EP again

- **The `nan` in that exception is a red herring.** The message lists "always
  returning `nan`" as a possible cause; it is not a possible one. The guard is
  `np.allclose` over the figures of merit, which is `False` for `nan`, and
  `figure_of_metric` discards `nan` draws before the check anyway. The
  condition detected is all-*equal, finite* likelihoods. That wording sent the
  original triage hunting a nan that could not exist — the prompt was filed as
  an all-`nan` bug. Message corrected and de-duplicated across both raise sites.
- **`Status`'s third positional parameter is `updated`, not `flag`.** Both
  `Status(...)` calls in `factor_step` (and one in `stochastic.py`) passed the
  flag positionally, so it landed in `updated` and `flag` stayed at its
  `SUCCESS` default: every errored factor step was written to `ep_history.csv`
  as a **success**. Any "EP looks healthy" read off those CSVs pre-2026-08 is
  suspect.
- **A returned `StatusFlag.FAILURE` is normal and must not be counted.** The
  Laplace optimiser returns one whenever its line search fails, and EP absorbs
  it by design. Restoring the flag and then counting failures cut
  `test_full_hierachical` and `test_other_priors` short. Raises now carry a
  distinct `StatusFlag.EXCEPTION`; only those count.
- **A consecutive-failure counter cannot detect the case it was written for.**
  #1405 asked for "abort after N consecutive failures". When enough factors
  raise, *nothing* in the mean field changes, so the KL step is zero —
  indistinguishable from convergence — and `EPHistory` ends the run before any
  count matters (sweep 2, count 2, threshold 3 on `ep.py`). The check has to be
  "did this factor ever update", asked at the end, not a per-sweep tally.
- **A warm `output/` hides this bug completely.** Searches resume from saved
  results and skip initialisation, so the exception can never fire. A 12-run
  loop of `ep.py` showed nothing until the output dir was cleared each run;
  with it cleared, 2 of 8 runs hit the degenerate state naturally (~25%,
  matching #1405's 23%) and all 8 completed on the fix. Clear `output/` before
  concluding anything about an intermittent search bug.
- **The release leg is the only place this can surface.** Smoke/CI run
  `PYAUTO_TEST_MODE=2`, which bypasses the sampler and therefore the
  initializer entirely.

## Posture change from the issue

#1405 asked for an abort. Shipped as a **loud warning that still returns**, on
maintainer decision: a partly-failed graph may hold good converged messages for
every factor that did work, and refusing to return discards those too. #1405's
bar — never *silently* reported as a confident answer — is met by the warning.

## Verification

- `test_autofit/graphical` 228 passed (219 baseline + 9 new); full suite 1654
  passed, 4 skipped. Behavioural tests confirmed failing against the unfixed
  loop. Regression tests use a **shared-variable, non-hierarchical** graph —
  the defect is not a `HierarchicalFactor` property, which the release-leg run
  proved (`ep.py` has no hierarchical factor and failed; `hierarchical.py`
  passed in the same shard).
- End-to-end on `autofit_workspace_test scripts/graphical/ep.py` under
  `profile_release.yaml`: 7/7 shard; transient raise absorbed; persistent raise
  completes with the warning. Pre-fix control on `origin/main`: dies, exit 1.
- `autofit_workspace` EP feature scripts pass; HowToFit chapter 3 passes.

## Fallout — a pre-existing bug found, not fixed

`HowToFit tutorial_5_expectation_propagation.py` dies at real sampling on
`main` and did so before this work: `LinearRegressionAnalysis.
log_likelihood_function` returns a constant `-1`, ignoring `instance`, so every
initial sample has an identical figure of merit. Invisible to CI (test-mode 2
bypasses the sampler). Parked as `NEEDS_FIX` in HowToFit's
`config/build/no_run.yaml` rather than fixed — a real likelihood for the m/c
regression over `fwhm_list` (computed there and never used) is tutorial
authoring, not a mechanical repair, and the script does not say what the
regression is meant to be against.

## Original prompt

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

### It is not hierarchical-specific (release-leg reproduction, 2026-08-03)

The toy that characterised this defect is a hierarchical graph, but the defect
is **not** a `HierarchicalFactor` property. The 2026-08-03 nightly release leg
reproduced the identical exception on a graph with *no* hierarchical factor at
all:

- PyAutoHeart run `30788224561`, job `91606145038`
  (`integrate / run_scripts (3.12, autofit_test, graphical)`).
- `autofit_workspace_test scripts/graphical/ep.py` — FAIL (11.4s) with the same
  `InitializerException` body. Its model is a **shared** `centre`
  (`af.GaussianPrior(mean=50.0, sigma=30.0)`) across two `AnalysisFactor`s, each
  with its own `DynestyStatic(nlive=300, maxcall=1000, maxiter=1000)`; there is
  no `HierarchicalFactor` in the script.
- **`scripts/graphical/hierarchical.py` PASSED in the same shard**, on the same
  wheels, in the same run — as did `ep_deterministic.py`, `ep_exact.py`,
  `ep_parity.py`, `shared_state.py` and `simultaneous.py`.

So the degenerate all-equal-FoM state is reachable through ordinary shared-prior
message passing. Scope the fix and its regression test to the **per-factor
update site in general**, not to hierarchical factors.

Two further properties from that run:

- **Intermittent, consistent with the ~23% rate.** The same shard passed the
  2026-08-04 night with no change to `ep.py`.
- **Release-profile-only.** The per-PR smoke gate runs `PYAUTO_TEST_MODE=2`,
  which bypasses the sampler and therefore the initializer entirely — this
  defect can only ever surface on the release leg (`PYAUTO_TEST_MODE=0`,
  `config/build/profile_release.yaml`). Do not expect a smoke run to show it.

### The `nan` in the exception text is a red herring — fix the message too

The exception body lists three possible causes, one of them
"The `log_likelihood_function` is always returning `nan` values." **That cause
is impossible for this check**, and the wording has already caused one
misdiagnosis (this failure was first filed as an all-`nan` likelihood bug).

The guard is:

```python
if total_points > 1 and np.allclose(a=figures_of_merit_list[0], b=figures_of_merit_list[1:]):
```

`np.allclose` defaults to `equal_nan=False`, so an all-`nan` figure-of-merit
list returns **False** and cannot raise this exception (verified:
`np.allclose(np.nan, [np.nan, np.nan]) is False` on numpy 2.4.6). The condition
detected is all-**equal**, finite likelihoods — exactly the degenerate state EP
drives a factor into. Reword the message accordingly as part of this fix.

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
- **Both raise sites.** The guard is duplicated in `initializer.py` at
  `samples_from_model` (line ~117/120) and `samples_jax` (line ~182/185). The
  release profile runs with `PYAUTO_DISABLE_JAX=0`, so the JAX path is live in
  the leg that caught this. Fix the handling *and* the message text at both, or
  factor the shared check into one helper.
- **Keep the release leg honest.** Degrading this crash to a skipped update
  turns a red release-leg script green while the underlying EP pathology is
  still there. That is acceptable only because the failure stays recorded —
  make sure whatever is written to `ep_history.csv` is something the nightly
  triage can actually see, so "ep.py passes now" never silently means "EP still
  degenerates every fourth run". This was the stated objection to fixing the
  release-leg failure via this prompt; it is answered by loudness, not by
  leaving the crash in place.
- **Test.** A regression test that drives a factor to an all-equal-FoM state
  and asserts the EP run completes with the failure recorded rather than
  raising. Cover a **non-hierarchical** shared-prior graph (the shape that
  failed on the release leg), not only a `HierarchicalFactor` one.
  `test_autofit/graphical/` is the home; numpy-only
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

Second, independent repro — the non-hierarchical release-leg shape, from the
`autofit_workspace_test` root (a smoke-profile run will **not** show it):

```bash
python3 <path>/PyAutoHands/autohands/run_python.py \
  autofit_test scripts/graphical \
  --env-config config/build/profile_release.yaml
```

Also intermittent, so loop it and count rather than reading one run.

## Relationship to the other defect

Independent of the COLLAPSE defect
(`draft/bug/autofit/ep_hierarchical_scale_collapse_moment_match.md`) and safe to
fix first — this one is a robustness fix with no statistical judgment in it,
whereas COLLAPSE needs a moment-match redesign. Fixing this one first also makes
the COLLAPSE work cheaper: 23% fewer wasted runs when gathering statistics over
repeated identical fits.

<!-- filed 2026-07-22 as the wrap-up follow-up of the ep-hierarchical-scale-collapse
task (report-only; PyAutoFit#1405). Origin: slope_hierarchy#1 goal 2.
2026-08-05: absorbed draft/bug/autofit/graphical_ep_nan_likelihood_release_leg.md
(the 2026-08-03 release-leg ep.py failure). That prompt read the exception's
"always returning nan" line as a nan diagnosis and scoped itself to finding the
nan source; the guard is np.allclose over the figures of merit, which cannot fire
on nan, so it is the same all-equal-FoM defect as this one on a non-hierarchical
graph. Folded rather than issued as a fourth EP issue. -->
