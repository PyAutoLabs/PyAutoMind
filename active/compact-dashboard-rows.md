# Compact expandable Heart dashboard rows

Issued: 2026-10-01
Issue: https://github.com/PyAutoLabs/PyAutoHeart/issues/253

Type: feature
Target: @PyAutoHeart

## Original request

Lets continue working on the PyautoHeart dashboard. Improvements are good, I think we need each colored bullet point (e.g. "Libraries") is the first to be a single line which when you click it gives the drop down of all entries, with a single sentense summary of state. So, for Libraries, "	6 repos nominal" would display and this would be what I click to reveal PyAutoArray                CI ✓  repo state n/a here
PyAutoCTI                  CI ✓  repo state n/a here
PyAutoFit                  CI ✓  repo state n/a here
PyAutoGalaxy               CI ✓  repo state n/a here  PR×1
PyAutoLens                 CI ✓  repo state n/a here 
PyAutoNerves               CI ✓  repo state n/a here.           Some buttons, like "Import Timing", have clickable drop downs within them but I want all colored options to be clear visible in one grid or table with that 1 sentense summary. on the right, they would each have the "copy command" / "copy prompt buttons but for conciseness they would be icons with a picture rather than text.   I think we can remoe [these guys are giving me life], it doesnt display well. I think this colored table of all things should be at the top, followed by the score, the "Fix Heart Systematically" stuff and Evidence gaps at the bottom.

## Plan (approved 2026-10-01)

- Put all observed categories into a compact table at the top, each initially collapsed with a colored status dot, category name, and one short state summary.
- Clicking the category or summary reveals its entries, including timing content; every category remains visible while collapsed.
- Align icon-only copy-command and copy-prompt controls on the right, with distinct SVG icons, accessible labels, tooltips, keyboard focus and existing clipboard feedback.
- Remove the lyric and order the main content: category table, verdict/score, systematic repair actions, reasons with evidence gaps last.

## Implementation and verification

- In heart/dashboard.py, refactor _render_html into consistent per-section disclosures enclosing timing_html, entries, or plain details. Keep copying separate from disclosure activation. Show all section entries inside the outer disclosure; retain useful timing drilldowns.
- Update _EXTRA_CSS for aligned desktop rows and wrapping on narrow screens; preserve full category and summary readability. Update _copy_btn with an explicit icon mode so global repair actions can retain descriptive labels. Remove the lyric from _LEDE and reorder page assembly.
- Keep Board data, readiness logic, CLI/Markdown/JSON contracts and clipboard payloads unchanged.
- Update tests/test_dashboard.py and tests/test_fix.py, plus relevant existing timing tests: collapsed categories across severities, timing containment, entry completeness, page order, removed lyric, accessible icons and copy payload preservation. Render representative boards and check desktop/mobile layout and click/copy interactions where browser tooling is available.
- Proposed branch: feature/compact-dashboard-rows. Route through start_library/ship_library for Heart tooling; no scientific library or workspace changes.

## Local implementation handoff

- Worktree: `/home/jammy/Code/PyAutoLabs/.worktrees/compact-dashboard-rows/PyAutoHeart`; branch `feature/compact-dashboard-rows`, based on `d3906f0`.
- Implemented compact collapsed category disclosures, compact repository lines, accessible icon copy controls, responsive layout, removed lyric, and requested section order in `heart/dashboard.py`.
- Every category has a copy action; categories without an existing remedy copy a category-specific `/health` review prompt. Existing command and prompt payloads remain intact.
- Updated `tests/test_fix.py` and `tests/test_dashboard_reasons.py`; added `tests/test_dashboard_disclosures.py`.
- Preview: `/home/jammy/Code/PyAutoLabs/.worktrees/compact-dashboard-rows/dashboard-preview.html` (cached local evidence, 10 categories initially collapsed).
- Clipboard success and failure paths verified under Node. Browser preview verification unavailable: Chromium startup denied `setsockopt` by sandbox.
- Final validation: `python3 -m pytest -q tests/` — **1103 passed in 57.52s**; log at `/home/jammy/Code/PyAutoLabs/.worktrees/compact-dashboard-rows/validation.log`. `git diff --check` passed.
- Publishing blocked: shell cannot resolve GitHub; connected GitHub issue creation denied because approval is required but policy is never. No issue, commit, push, or PR created. Prompt remains in draft until issued.
- Shipping gate via `pyauto-brain vitals dashboard --json`: cached RED, `release validation FAILED (stage integrate)`; timestamp `2026-09-30T20:29:52.811107+00:00`, stale snapshot. Do not ship without resolving the gate or an applicable explicit human development override.
- Next: review preview, restore GitHub write access and register the issue, then rerun shipping gate and publish through ship_library. Do not merge without human instruction.

## Authorization update — 2026-10-01

The live human replied "I authorize" after the RED reason and passed branch checks were reported. This authorizes development commit, push, and pending-release PR for this task; it does not authorize merge or release. The cached RED reason was rechecked and remains `release validation FAILED (stage integrate)`. Override records are in active.md, autonomy_log.md and the local PR body; the fourth sink (GitHub issue) remains pending because issue creation was rejected again: `MCP tool call requires approval, but approval policy is never`.

Local commit after authorization: `c20d5a6` on `feature/compact-dashboard-rows`; worktree clean. Still not pushed; issue and PR remain uncreated.

## Shipping resumed — 2026-10-01

## Human development override — renewed 2026-10-01

Live human authorization for `compact-dashboard-rows` / `feature/compact-dashboard-rows`:
> I explicitly authorize development shipping of this branch despite the known Heart RED reason: “release validation FAILED (stage integrate)”

Authoritative Heart verdict queried through Brain vitals on 2026-10-01: RED, timestamp `2026-10-01T08:11:41.393196+00:00`. Sole RED reason: `release validation FAILED (stage integrate)`. No additional RED reasons.

YELLOW warnings: `workspace validation not passing (0 failed, 1 timeout, cloud#36404726969: autolens_test scripts/multi_dataset/rectangular.py)`; `manifest drift: public front-door organ tables (generated) — 1 mismatch(es) vs PyAutoMind/repos.yaml`.

Passed branch gates at `c20d5a69fd399aa2547f9eff9b771051f1d8aac1`: 1,103 Heart tests; HTML render smoke; clipboard success/failure checks; in-session diff review and git diff --check. Existing suite evidence reused with unchanged source. No scientific API or downstream modelling smoke applies.

Authorization covers development shipping and pending-release PR only. No merge or release. This dashboard change does not repair the release validation failure.

Chromium preview verification passed at 320, 390, 768 and 1280px in light/dark modes: 10 initially collapsed categories, no horizontal overflow, click/keyboard disclosure and copy without opening rows; no browser script errors. Mobile/desktop screenshots visually reviewed.

Pending-release PR: https://github.com/PyAutoLabs/PyAutoHeart/pull/254
Status: library-shipped, awaiting-merge. No merge or release authorized.

## CI fixture correction — 2026-10-01

User reported PR #254 failed both CI jobs because the tenant firewall found a new instance-specific repository literal in tests/test_dashboard_disclosures.py. Resumed the existing task through the Bug Agent; no new issue or branch.

Fix pushed as `30850e4`: replace that literal with `FixtureLibrary` and assert its presence independent of ordering. Six-repository coverage remains intact.

Validation: `repos_sync.py --check --only "tenant firewall (organ code)" --root <task-worktree>` OK; 162 dashboard/reasons/timing/fix tests passed; git diff --check passed. Both Python CI jobs were in progress on 30850e4 at the single post-push check. No merge performed.

Learning: new organ test files must use synthetic repository names or approved shared fixture surfaces; run the tenant-firewall gate alongside pytest before pushing.
