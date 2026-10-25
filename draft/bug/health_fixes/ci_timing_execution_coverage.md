# CI timing must compare equivalent executed job coverage

Type: bug
Target: PyAutoHeart
Themes:
- ci-smoke
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: formalised
Consequence: judge
Filed: 2026-10-25

## Original intent

Continue pre-release Heart and hygiene work. Do not lower thresholds, waive tests or change scoring weights. Diagnose before implementing.

## Finding and verified diagnosis

Reconcile existing Heart IDs `ci_timing:HowToLens/Smoke Tests:` and `ci_timing:coverage` (same cause). Board timestamp 2026-10-25T09:34:29.845384+00:00 reports median 304s versus historical baseline 63s, ratio 4.83, 15 successful runs since 2026-10-08T08:37:08Z.

All 15 runs were read from GitHub along with individual jobs. Six success workflows only execute the changes classifier and SKIP smoke (38,43,43,50,59,105s). Nine execute both Python 3.12/3.13 smoke legs successfully (300,304,314,323,324,332,351,501,606s). Mixed median 304s matches Heart exactly; full-execution median 324s; classifier-only median 46.5s. Earlier main run 37192387461 has the exact 63s duration but skipped smoke too; this is NOT proof that it alone supplied Heart baseline. Authoritative historical baseline samples are unavailable here.

Recent full main runs: Oct8 323s; Oct11 314s; Oct22 324s; Oct24 351s. Oct24 versus Oct8 is 1.087x, not 4.83x; these four samples alone do not rule out individual script regressions. Collector `heart/checks/ci_timing.py:time_workflow` appends every successful workflow duration without examining executed-job coverage. It therefore cannot establish a like-for-like performance regression when workflow coverage changes.

## Reproduction and Brain routing

The existing Heart time_workflow function was run read-only on the captured 15 successful run records: asserts passed for mixed 304s/15, full 324s/9, skipped 46.5s/6. No collector or published state was modified. Brain BugDecision recommends investigate-first with low-confidence unresolved owner; direct source inspection locates the missing coverage distinction in PyAutoHeart/heart/checks/ci_timing.py and its run collector. Reproduction is established; implementation remains unstarted and must use start-dev.

## Proposed repair and acceptance criteria

1. Inspect existing collectors and job API budgets; attach bounded execution-coverage evidence, distinguishing full, classifier-only/skipped, partial and unknown.
2. Compare compatible coverage cohorts. Historical coverage missing means insufficient comparable evidence; never silently call it green or inflate/reset a baseline.
3. Preserve thresholds, cancellation/error classifications and required skipped-job policy. Workflow success is not proof smoke ran.
4. Add a failing regression test reproducing mixed 15-run data; include all-skipped, unknown job evidence, partial matrix and true full-run slowdown cases. Old threshold behavior must remain for equivalent work.
5. Refresh authoritative Heart collector with comparable history and reconcile the same two IDs. This advisory timing defect does not repair either release RED reason.

## Evidence

Skipped example https://github.com/PyAutoLabs/HowToLens/actions/runs/39951551703
Full examples https://github.com/PyAutoLabs/HowToLens/actions/runs/39850351606 and https://github.com/PyAutoLabs/HowToLens/actions/runs/40092843981
Complete job inventory retained in the health review report. No source change or active claim created for this repair. Check latest claims and route through start-dev before implementing.
