# Relax call-accounting CI timing threshold

Type: bug
Target: autolens_profiling
Repos:
- autolens_profiling
Status: draft

## Original request

> increase it a bit so merge goes through, only a smalla mount

## Failure evidence

PR #288's only CI failure is
`test_call_accounting_covers_a_real_likelihood_call`. The ABBA instrumentation
overhead was `1.030266` against the current `1.03` threshold. The same full
suite passed locally (665 passed, 5 skipped), so classify whether this is a
host-timing tolerance issue and make only the smallest justified adjustment.
