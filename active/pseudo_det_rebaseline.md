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
