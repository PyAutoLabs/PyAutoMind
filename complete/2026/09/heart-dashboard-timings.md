# Heart dashboard timing clarity

Merged PyAutoHeart PR #250 on 2026-09-30 as `46d267f2e1a1d9731e17a523ddae4e0b10e3d1c4`, from head `984b1f60210af19469e4c816bb3608de755a68a6`. Issue #249 closed; all claimed commits proven ancestors of origin/main.

Timing cards now make current seconds prominent, label baseline/change and coverage, preserve unavailable and baseline-building imports, show suite Python legs independently with their three slowest tests and expandable remaining detail, and display CI median/max/count/window before accessible charts with missing-data gaps and text equivalents. Copy labels no longer truncate. Readiness and the performance consumer contract are unchanged.

Validation: 1099 Heart tests, 147 final presentation tests, 53 Brain consumer tests; four baseline comparisons of performance/verdict/score/blockers; Chromium light/dark at 375/390/1280px, keyboard disclosures, 200% text and copy labels. Exact-head CI run 36770498391 passed every step in Python 3.12 and 3.13.

After merge, dashboard publisher dispatched: https://github.com/PyAutoLabs/PyAutoHeart/actions/runs/36772075665 (completed successfully). Existing release integration failure is not repaired by this presentation work. No scientific release performed.

All three approved dashboard phases are merged (#246, #248, #250). The Fable-reviewed parent packet is retired separately as `complete/2026/09/heart-dashboard-clarity-plan.md`. Preview images and validation logs are retained locally under `tmp/heart-dashboard-timings-evidence/`.

## Original prompt

# Heart clarity PR C: readable import, unit-test and CI timings

Type: feature
Target: PyAutoHeart
Difficulty: medium
Autonomy: human-required
Status: active
Issued: 2026-09-30
Issue: https://github.com/PyAutoLabs/PyAutoHeart/issues/249
Priority: medium

@PyAutoHeart. Parent intent, findings, design and the Fable review with its numbered amendments: `draft/feature/pyautoheart/heart_dashboard_clarity.md` in Mind. Human approved the amended plan on 2026-09-30; PR B merged as #248; implementation is now unblocked.

Scope (parent detailed step 3, applicable step 5 validation):

- Import timing: package, bold current seconds, labelled baseline/change, source and coverage; preserve unavailable/failed imports and baseline-building states. Fix the false green at `heart/dashboard.py:774-781` (OK “0 imports within baseline” while 4 packages have no baseline and 1 is unavailable) with a regression test (amendment 6).
- Unit timing: suite wall-clock, Python leg, counts, top three bottlenecks by default, rest under disclosure; never sum parallel legs; separate absolute slowness from measured regression.
- CI: median, max, run count and window first; accessible labelled inline SVG with text fallback; keep `performance.gates[].spark` intact for the Brain; never present missing samples as zero.
- Fixtures: the local snapshot has empty timing slices, so validate against the published `board.json`, a `heart-health` artifact or fixtures (amendment 10).

Preserve verdict/score, the `performance` block's own schema and the Brain/hygiene reads of `performance`. Dispatch `heart-health.yml` after merge.

Proposed branch `feature/heart-dashboard-timings`. Follow start-dev → start-library → ship-library. Implementation approved on 2026-09-30; existing dependency and shipping gates still apply.

## Delivery (2026-09-30)

PR https://github.com/PyAutoLabs/PyAutoHeart/pull/250 is open at 984b1f6. Heart 1099 tests, final 147 display tests, Brain consumers 53 tests and responsive browser checks passed. Await human /prm; dispatch heart-health.yml after merge.
