# pseudo-det-rebaseline — Heart RED root cause: stale evidence pins after PyAutoArray#683

- issue: https://github.com/PyAutoLabs/PyAutoGalaxy/issues/700
- issue: https://github.com/PyAutoLabs/PyAutoLens/issues/822
- issue: https://github.com/PyAutoLabs/autolens_workspace_test/issues/360
- library-pr: https://github.com/PyAutoLabs/PyAutoGalaxy/pull/701
- library-pr: https://github.com/PyAutoLabs/PyAutoLens/pull/823
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace_test/pull/361
- completed: 2026-11-10
- corrective-red: "PyAutoGalaxy/Tests: failure"; "PyAutoLens/Tests: failure"; "Workspace validation: NOT ready — 1399p / 14f / 125s @ cloud#42607741369" (human-authorized Corrective-PR exception; records on each issue)

## What happened
- Culprit: PyAutoArray#683 (a589c35), the maintainer-approved pseudo-determinant for intrinsic regularization.
  It raises log evidence by +0.5*ln(1e8) = +9.21034 per intrinsic-regularized mapper. Bisect on the
  11 Galaxy failures: c020cc2 (#681) green, 6ae33d4 (#683) red, main with a589c35 reverted green.
- #683's companion autolens_workspace_test#358 re-pinned 12 jax_likelihood values but missed the downstream
  PyAutoGalaxy (12) and PyAutoLens (21) unit-test pins and 2 datacube scripts.
- Human chose option (b), re-baseline. Every pin was measured (c020cc2 vs main): +9.210340 per mapper, +18.420685 for
  two mappers, +9.5266 for Lens delaunay_split. The last is weak AdaptSplit with λ2(H0)=1.4e-9 < the 1e-8 jitter, so the
  grounded det is not the exact pdet there (deterministic, re-pinned as measured).
- 12 of the 14 Workspace Smoke failures (run 42607741369) came from a checkout before #358 merged. The 2 datacube pins
  were fixed in #361. The Hands Python Version Matrix failures were the same Galaxy/Lens unit tests.
- Gates: full suites on Array main (Galaxy 1461p/7s, Lens 1003p/1s/1xf); independent review CLEAN; exact-head CI green
  on all legs; Galaxy/Lens main CI green after merge.
- No release needed (test/script-only).

## Follow-ups (not filed)
- PyAutoArray#682 semantics: the pdet grounding is exact only for jitter << λ2(H0). Consider subtracting the jitter or
  using a scale-aware jitter for weakly regularized AdaptSplit.

## Original prompt

# Bug: PyAutoGalaxy/PyAutoLens evidence pins stale after PyAutoArray#683 pseudo-determinant

Consequence: judge
Autonomy: human-required

## Original request (2026-11-10, human, abridged verbatim)
"Heart is RED. The cause looks like one numerical regression in PyAutoArray main that broke
PyAutoGalaxy/PyAutoLens main CI … Find it, fix it (or re-baseline, if the change was deliberate and
correct), get Heart back to GREEN, then /prm PyAutoGalaxy#699. … This is a causal fix for the RED
reason, so use the AUTONOMY.md "Corrective-PR exception for Heart RED"."
Human chose option (b) re-baseline after the bisect evidence.

## Finding
Culprit: PyAutoArray#683 (a589c35), a deliberate, maintainer-approved likelihood change
(+0.5*ln(1e8) = +9.21034 nats per intrinsic-regularized mapper). #681 exonerated by bisect
(c020cc2 green, 6ae33d4 red; reverting a589c35 on main makes the tests green).
Downstream unit-test pins in PyAutoGalaxy (12) and PyAutoLens (21) were not updated.

## Fix
Test-only re-pin to measured values: PyAutoGalaxy#700, PyAutoLens#822.

## Follow-up (not filed)
- The pdet grounding is exact only for jitter << lambda_2(H0). Weak AdaptSplit (Lens delaunay_split
  test, lambda_2 = 1.4e-9 < 1e-8) gives a +9.53 shift, not +9.21. Possible follow-up on #682 semantics.
