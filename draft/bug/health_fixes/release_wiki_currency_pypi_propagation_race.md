# Release train: autolens wiki-currency check races PyPI index propagation

Type: bug
Target: PyAutoHands
Repos:
- PyAutoHands
- autolens_assistant
- autofit_assistant
- autogalaxy_assistant
- autocti_assistant
Themes:
- release
Difficulty: small
Autonomy: supervised
Priority: high
Status: formalised
Consequence: judge
Filed: 2026-11-08

## Original intent

Health review, 2026-11-08: understand the red `ci_status:PyAutoHands/workflows/PyAuto Release:`
finding. Diagnose before implementing; do not lower thresholds or waive checks.

## Finding and verified diagnosis

Heart ID `ci_status:PyAutoHands/workflows/PyAuto Release:` (red, board 2026-11-07T11:30Z)
points at run 42360648525. The two most recent **live** releases both ended in failure
after a complete, successful publish:

| Release | Run | Failed jobs |
|---|---|---|
| 2026.11.6.1 | 42201537352 | `wiki_currency_check / wiki-currency`, `wiki_drift_issue` |
| 2026.11.7.1 | 42360648525 | `wiki_currency_check / wiki-currency`, `wiki_drift_issue` |

The release did ship. All six wheels were on PyPI at 09:56Z on 11-07, tags exist on the
libraries and workspaces, release notes were published, and the Colab bump committed.

**Primary cause (timing race).** The step that fails is "Install the released stack" in
`autolens_assistant/.github/workflows/wiki-currency.yml`, which runs `pip install
"autolens==$VER"` once, with no retry. In run 42360648525 it ran at 10:00:05Z, about 3 minutes
after the autolens upload at 09:56:49Z. pip's version list ended at 2026.11.6.1, followed by
"No matching distribution found for autolens==2026.11.7.1". The 11-06 run failed the same way
on 2026.11.6.1. The autofit, autogalaxy and autocti assistants run an identical single-shot
`pip install` and passed both times, so the failure is intermittent: it depends on how fast
PyPI's simple index / CDN propagates, not on the docs.

**Secondary defect (misreporting).** `wiki_drift_issue` runs when the check fails. Its first
step, `actions/download-artifact` for `wiki-drift-report`, fails hard when no report was
uploaded, so the fallback body ("check failed but no drift-report artifact was found")
can never run. An infrastructure failure therefore shows up as a second red job and not
as a clear report. The `_autofit`, `_autogalaxy` and `_autocti` drift-issue jobs share
the same pattern.

## Proposed repair and acceptance criteria

1. Make the released-stack install tolerant of index propagation. Either:
   - a bounded wait-for-version loop before the wiki-currency jobs, in PyAutoHands (one
     place, covering all four assistants); or
   - a bounded retry with `--no-cache-dir` in each assistant's reusable workflow.

   An unavailable version must still FAIL after the bound. Never fall back to an
   unpinned or older install.
2. Make the drift-issue jobs' download step `continue-on-error: true`, so a missing
   artifact reaches the existing fallback body, and that body says the check could not
   install the stack (not that drift was found).
3. No change to wiki-currency rules, thresholds or what is graded.
4. Witness: the next live release's four `wiki_currency_check*` jobs succeed or report
   genuine drift. Or, simpler: a rehearsal-safe dry check of the wait loop against an
   already-published version, plus a deliberately missing version that fails after the bound.

## Evidence

- https://github.com/PyAutoLabs/PyAutoHands/actions/runs/42360648525 (job 128371996414, log lines 172-178)
- https://github.com/PyAutoLabs/PyAutoHands/actions/runs/42201537352 (job 127846883910)
- 2026-11-08: the failed jobs of 42360648525 were re-run (the check only, no code change)
  to confirm the propagation diagnosis against the now-indexed 2026.11.7.1.
