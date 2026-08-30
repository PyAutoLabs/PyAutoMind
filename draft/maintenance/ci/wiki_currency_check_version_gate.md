# wiki-currency's --check-version gate rots on every library main merge

Type: maintenance
Target: autocti_assistant
Repos:
- @autocti_assistant
Themes:
- assistants
- ci-smoke
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: formalised
Consequence: judge
Review-minutes: 20
Unattended: ready
Filed: 2026-08-24

`wiki-currency` went red on `autocti_assistant` main and was fixed on 2026-08-24
by regenerating `wiki/core/api_audit_baseline.json` (autocti_assistant#24, PR
#23). That fix is correct but **temporary**: the same red will return, and the
reason is structural, not incidental.

## The structural problem

`--check-version` compares a hash of the **entire public API surface** of
`autonerves`, `autoarray`, `autofit`, `autocti` and `autocti.plot` against a
committed baseline. The assistant documents almost none of that surface.

Measured at the time of the fix — the drift that turned the repo red was:

```
autoarray  120 -> 121   + InterpolatorDelaunayNN, validate   - TransformerNUFFTPyNUFFT
autofit    149 -> 159   + AbstractClipper, AbstractScaler, ApproxUpdater,
                          ClipperNone, ClipperPriorBox, DynamicUpdater,
                          FactorUpdater, NSS, ScalerNone, ScalerPriorWidth,
                          SimplerUpdater
                        - database
```

**Not one of those 14 symbols is cited anywhere in `wiki/`, `skills/` or
`modes/`.** `--scope all` — which audits exactly the symbols the docs *do* cite
— reported "All cited symbols resolve cleanly. No drift detected." throughout.
`autonerves`, `autocti` and `autocti.plot` were byte-identical.

So a check whose job is "are the docs current?" went red because eleven unrelated
sampler-clipper classes were exported from autofit.

The workflow installs the stack from the libraries' **`main` source clones** (not
a release — see the note below), so the clock is every merge into autofit or
autoarray `main` that touches an `__init__` export. That is fast. The new
baseline should be expected to rot within weeks.

A check that goes red on a schedule nobody controls, for reasons that never
affect the thing it gates, trains reviewers to ignore it — and this repo's PRs
already opened red for over a month.

## The decision to make

Two coherent options; **this task is to choose one deliberately and implement
it**, not to guess:

1. **Gate `--check-version` on removals only.** A symbol *disappearing* can break
   a doc; a symbol *appearing* cannot. Report additions as informational, fail
   only on removals from the surface. Keeps a cheap tripwire for the case that
   actually matters. Note this still would not have caught the real risk here —
   `TransformerNUFFTPyNUFFT` and `database` were both removed and neither was
   cited, so even removals produce false reds; consider gating on
   *removals of cited symbols*, which is what `--scope all` already computes.
2. **Accept that `--scope all` subsumes it as a gate.** Demote `--check-version`
   to informational (still printed, still useful context in the report), and let
   `--scope all` be the thing that can fail the workflow. Simplest, and the
   check it leaves is the one with a direct causal link to doc correctness.

Option 2 is the leaner one and is probably right; option 1 is defensible if a
whole-surface tripwire is wanted for release-time invocations
(`workflow_call` with `stack_version` set), where the surface really is the
contract. Consider keeping the strict behaviour for the pinned-release path and
relaxing only the native PR/dispatch path.

Whichever is chosen, the baseline-regeneration story should be documented in
`skills/ac_audit_skill_apis.md` so the next person hitting a red knows whether
regenerating is the right response or a papering-over.

## Do not "fix" this by pinning to a released stack

Already considered and rejected on 2026-08-24: autocti's PyPI release is the
pre-resurrection `2024.11.13.2`, so pinning would grade today's docs against an
API that predates the work they describe — vacuously green, worse than noisily
red. The workflow's own install-step comment says as much.

## Context worth reading first

`PyAutoMind/complete/2026/08/wiki-currency-baseline-drift.md` — the full
investigation, including the fact that the drift report used to print
`stack_version: latest released` when the native path actually builds from
`main` source clones. That mislabel is fixed, and the report now records each
source tree's short SHA, so a future red is diagnosable from the artifact alone.
