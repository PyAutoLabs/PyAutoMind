# Profiling conductor compile drift compares one point against one point

Type: bug
Target: pyautobrain
Repos:
- PyAutoBrain
Themes:
- measurement-tools
Difficulty: small
Autonomy: supervised
Priority: medium
Consequence: judge
Status: draft
Filed: 2026-10-09
Related: https://github.com/PyAutoLabs/autolens_profiling/issues/362

## Context

The timing-noise audit of autolens_profiling (`results/notes/timing_noise_audit_2026_10.md`, #362)
found that the project dashboard's release drift badge (P7) compared single-sample endpoints, and
fixed it there (#405: within-band → `insufficient` unless both endpoints carry a repeat summary;
#408: compare like estimators only). The audit note records that the Brain profiling conductor's
`COMPILE_DRIFT_RATIO` rule (`agents/conductors/profiling/_profiling.py:88`, used at ~513) shares
P7's point-vs-point limitation, and that "a separate Brain task should decide whether compile drift
follows; this audit does not edit Brain".

## Decide

Whether the conductor's compile-drift check should (a) keep its generous 2x band as a gross flag
with an explicit "single-sample" caveat, as P7's `drifted`/`improved` now do, (b) require repeats or
an interval before reporting drift, or (c) stay as is with a documented reason. Keep compile and
execution costs separate. Synthetic witness required for any change.

## Original request (chat 2026-10-09)

"prm and then do 3b and leftovers fully wrap up --auto" — filed as the Brain hand-off named in the
audit note; not part of the #362 PRs.
