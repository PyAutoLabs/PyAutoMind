# Simplify profiling results navigation and presentation

Type: feature
Difficulty: medium
Consequence: judge
Issued: 2026-10-07
Issue: https://github.com/PyAutoLabs/PyAutoPulse/issues/25

@PyAutoPulse

Implement the requested dashboard presentation changes without deleting captured results or changing measurement producers. Use the workspace development route. Plan approved by the user with “go”.

## Approved implementation plan

- Simplify the landing board and standardize all requested display names.
- Open each model in a dedicated browser tab with a stable, reloadable URL.
- Put Instrument, Device and Configuration selectors together; show Configuration details before measurement panels. Retain the lower measurement navigation and remove duplicate buttons and browse steps.
- Restrict normal dashboard choices to float64 and 1500 source pixels where source pixels apply, choosing explicit default variants for remaining settings. Preserve all raw captures. Missing matching results get an honest empty state, not a silent nonmatching fallback.
- Use compact bars sharing an appropriate timing scale, with the matching total likelihood as denominator where recorded. Keep incompatible units, batch semantics, hardware and configurations separate; never invent totals or join unrelated runs.
- Remove the specified redundant prose and sections, and split result links from script links.
- Verify rendering, filtering, navigation and bar scaling with Python and Chromium checks; regenerate the board from retained evidence.

Tier: judge — merge mode: human /prm

### Detailed implementation

Primary repo: PyAutoPulse. Classification: workspace/organ presentation (the Feature CLI classified this unknown organ as library; this task changes no scientific library or public API).
Suggested branch: feature/profiling-results-ui.
Branch survey: canonical PyAutoPulse is clean on main, only local branch main; conflict helper returned 0, no active claim. Mind clean on main before drafting.

1. `pulse/campaigns.py::render_html` and markdown: remove Fix Profiling Systematically and its check-in review line; rename evidence heading and remove its introduction. Retain underlying campaign state.
2. `pulse/board.py::render_html`: remove legacy capture disclosure; update navigation label. Reuse Brain shared theme without changing shared consumers.
3. `pulse/setup_browser.py::render`, `pulse/setup_browser.js` and browser CSS: central display-name mapping; model links with new-tab targets and URL state rendering a model detail page. Preserve setup identifiers and same-commit shard verification. Keep instrument control dimensions, arrange Device and Configuration beside it responsively.
4. Replace axis-dependent repeated browsing with direct configuration selection and measurement panels. Move configuration details first; remove overview cards, qualification/method and shared-findings sections; split evidence/script disclosures. Hide only requested presentation, preserving provenance in captured data and linked results.
5. Add explicit display eligibility/default selection for precision and source size based on recorded metadata; do not assume unknown precision is float64. Analytic models have no source-pixel restriction. Retain models/devices with an explicit missing-results state where no eligible evidence exists.
6. In `panels`, replace per-method singleton normalization with compatible common scales. Breakdown uses a recorded matching full-likelihood total when available; otherwise label an honest shared component scale. Runtime uses a common maximum only within comparable measurement semantics. Reduce row spacing and bar height, remove repeated captions and missing-statistic filler.
7. Update `tests/test_campaigns.py`, `test_board.py`, `test_setup_browser.py` and `browser_setup.cjs`: new-tab/reload navigation, selector behavior, default filtering, retained archived data, missing matches, bar proportions/units and responsive overflow. Run required Ruff, Python tests, Chromium checks and offline contract validation. Regenerate published artifacts via the owning CLI without new profiling runs.

### Planning evidence

Heart door: STALE, exit 1; development planning permitted. Memory consultation located the completed setup browser/redesign work. Inspection confirms singleton grouping in `panels` explains full-width bars. No source files edited before plan approval; issue/worktree setup follows approval through start-dev.

## Original user request (verbatim)

- Remove the "Fix Profiling Systematically thing and the Last check-in: 2026-10-04 · review date" underneath it.

- Remove lens · capture, qualification and legacy diagnostics which feels legacy.

- In profiling evidence remove "Choose a project, dataset and model. Qualification belongs to each recorded setup."

- Rename Profiling evidence to Profiling results.

- rename AutoLens to PyAutoLens

- I want us to adopt standard captilization and case for all things so:

delaunay matern -> Delaunay Matern
Delaunay natural neighbor -> DelaunayNN
knn -> KNN
mge mass -> MGE Mass
remove "pixelized"
sersic -> Sersic


Inside a thign remove "Browse recorded runs by measurement and device. Runs can have different settings and revisions; they are not a combined benchmark."

I think we should remove the 4 buttons Runtime / Breeakdown / Compilation / Memory, they duplicate the tabs below and the
tabs are more natural to navigate.


Top row should be instruemtn with drop down (same as it is now sizing is good) but then to the rigth should be Device and Confiruaiton (remove / evidence run.)

There are too many things under Configuration that currently I find it hard to navigate. I think for now we should just do
float64 for all devices with 1500 source pixels (and try choose the other most default options for other things)
and we build up. dfont lose other results but avoid them meeting dashboard for now.


Under breakdown this stuff is repetitive or redundant so remove:
Statistic not recorded · repetitions not recorded

Component observations · a100 · gpu · float64 · euclid-ral-gpu-2 · s

Also remove this:

Instrumented component costs are not the full compiled likelihood time. Bars compare values only within this setup and unit.

Component observations · a100 · gpu · float64 · euclid-ral-gpu-2 · s

The breakdown bars are good but they are not relative to the total time so they are all the same size (e.g. full)]
and they should be samller so I can get most on my screen without issue.


I dont think we need these "Browse Likelihood Runs" bottons, they are an unecesary click, all info should be after
we click the drop down but with the extra text remove and smaller bars they will be more visible on one poage.
Agian for likelihood run time all bars are full so we are not seeing sizes relative to some main run?



Cofiguration details, these details are important for all profiling inspection so should be the top option befpore likelihood runt ime.

Remove Qualification and measurement method.

Remove shared component and method findings

Split "Profiling evidence and scripts" in "Profiling Results" and "Profiling scripts".



I think when we click "Delaunay" (or any button under imaging or another thing) it should open a new tab with all the
above as a new page, theres a lot of info and we will ultimately want to compare run times across settings so want
new tabs in my browser anyway!

## Implementation handoff — 2026-10-07

Implementation and local validation are complete on `feature/profiling-results-ui`, at `/home/jammy/Code/PyAutoLabs/tmp/worktrees/profiling-results-ui/PyAutoPulse`. Source changes remain uncommitted because the current Heart shipping gate is RED.

193 Python tests, Chromium interactions/responsive checks, Ruff lint/format, offline contract validation, and `git diff --check` all passed. Full captured Delaunay/A100 preview verified with exact-commit shards. No raw results, captures or profiling producers changed. No independent review is claimed; this human-approved task does not require the autonomous review gate.

The prepared PR body is `../pr-body.md`; logs are `../pulse-tests.log`, `../browser.log`, `../offline.log`, `../ruff.log` and `../preview.log`. Screenshots are `tmp/browser/delaunay-a100.png`, `model.png` and `landing.png` in the worktree.

Heart RED reasons (verbatim):
- PyAutoFit: 2 commit(s) behind origin
- PyAutoArray: 2 commit(s) behind origin
- PyAutoGalaxy: 2 commit(s) behind origin
- PyAutoLens: 2 commit(s) behind origin

Next step: obtain the live human development-only shipping override required by Brain AUTONOMY.md, record it in all four required sinks, then commit/push/open the prepared PR. Merge remains a separate human action.

## PR opened

- PR: https://github.com/PyAutoLabs/PyAutoPulse/pull/26
- Commit: `868d929`, branch `feature/profiling-results-ui`.
- All 193 Python tests, Chromium interactions/responsive checks, Ruff lint/format, offline catalogue/dashboard checks and whitespace checks passed.
- Model detail pages, curated float64/1500 defaults, compact proportional bars and requested copy/navigation cleanup are implemented; captures unchanged.

User authorization: “I authorize, maybe we should get those repos up to date first?” Verified PyAutoFit, PyAutoArray, PyAutoGalaxy and PyAutoLens clean on main and equal to fetched origin/main. No pulls were necessary. Refreshed Heart cleared all four previous RED reasons before source commit/push/PR; no RED override was exercised.

Current Heart is YELLOW: `manifest drift: workspace checkouts (manifest ↔ disk) — 2 mismatch(es) vs PyAutoMind/repos.yaml`. Stale evidence: `release validation incomplete: no rehearsal for current source`.

Next step: human `/prm` after all required checks pass. No merge or deployment performed.

## CI reload-race repair — 2026-10-07

User requested “fix the bug” after `/prm` stopped on PR #26's Chromium failure. Resumed the existing approved task/branch; no scope expansion or second issue.

Root cause: panel opening was immediate, but URL persistence waited for the asynchronous native `toggle` event. A reload before event delivery restored Runtime. A same-task activation regression reproduced the failure deterministically (`open: true`, `axis: runtime` instead of `breakdown`). The fix persists selection synchronously from summary click activation, including native keyboard activation; closing retains native behavior. No sleeps or weakened assertions.

Commit: `f3a34c5`, pushed to PR https://github.com/PyAutoLabs/PyAutoPulse/pull/26.
Validation: 193 Python tests, Chromium including deterministic activation/reload and keyboard checks, Ruff lint/format, offline contract and whitespace checks PASS. Dashboard regenerated. Heart remains YELLOW for the previously recorded manifest mismatch; no new RED reason. Logs: task bundle `bug-repro.log`, `bug-browser.log`, `bug-pytest.log`, `bug-offline.log`, `bug-readiness.json`.

Lesson: native details toggle events are queued; persist route state during activation when reload/share correctness requires synchronous state. GitHub CI on the new head is the remaining merge gate. Merge still requires `/prm`.

CI confirmation: f3a34c5 — lint/Chromium run 37629490960 PASS (53s); Dashboard Refresh run 37629490950 PASS (12s). Ready for human /prm.
