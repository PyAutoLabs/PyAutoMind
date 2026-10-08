# Community table readability

@PyAutoEars

Type: feature
Issued: 2026-10-08
Issue: https://github.com/PyAutoLabs/PyAutoEars/issues/23

## Original request (verbatim)

PyAutoEars: - Remove the "PyAutoLabs/.github - Discussion # 13" and other grey text under each issue, it doesnt help me diagnose anything and clutters the tables.
- When I drop box an issue and click on it:
        
Category: Announcements

Delivery: unknown

Delivery evidence missing, incomplete, reverted or not verified public; inspect source.

- Remove "Open Discussion" as we have a button to the right, and make the text a bit more readable (e.g. bold font on left)          
its currently clutttered and hard to read,           All things under "Needs your attention" and "Community Activity" should have a date column, either date issue created or date updated.     The "Reccuring feedback" dropdown can be removed or should be in the same format as the other 3.

## Scope

Remove conversation subtitles and redundant source links; format expanded metadata with bold labels and readable spacing. Add an Updated date column to both conversation tables, using source timestamps. Remove the recurring-feedback placeholder. Preserve collection, uncertainty semantics, and the right-hand GitHub action.

## Approved plan

- Remove grey repository/type/number subtitles beneath conversation titles.
- Remove duplicate Open discussion/issue/PR links from expanded rows; retain the right-hand source action.
- Format expanded metadata with bold labels and readable spacing, including delivery status and evidence gaps.
- Add an Updated column to both conversation tables, falling back to Created when only that source timestamp exists and explicitly marking unavailable dates in legacy snapshots.
- Remove the recurring-feedback placeholder.
- Validate rendered desktop/mobile layouts, tests, and the generated state feed.

Tier: undeclared — merge mode: human /prm.

## Detailed implementation

1. `ears/collect.py`: preserve optional nullable `created_at` and `updated_at` metadata from source records; extend snapshot validation compatibly for old snapshots. These dates are distinct from response waiting age and snapshot generation time.
2. `REFERENCE.md`: document the optional timestamp fields. Check Brain's Community adapter (`agents/conductors/community/_ears_feed.py`) accepts additive metadata; validate adoption without changing its response heuristics.
3. `ears/board.py::render_page`, nested `section`: remove topic-meta and duplicate source links, use labelled metadata markup, render readable dates with machine-readable time elements in both HTML tables and the Markdown companion, remove recurring-feedback placeholder. Preserve escaped source text and meaningful uncertainty/evidence details.
4. `ears/presentation.py::CSS`: replace obsolete subtitle styling, style bold detail labels and spacing, rebalance six columns and maintain accessible local scrolling on narrow screens using shared sizing conventions.
5. Update relevant existing collector/presentation fixtures and assertions for timestamps and backward compatibility. Run the Ears pytest suite, validate generated `state.json` through Brain's contract, and run the existing browser smoke at desktop/mobile sizes in light/dark modes with expanded rows inspected.

## Survey

- PyAutoEars canonical checkout: `/home/jammy/Code/PyAutoLabs/organs/PyAutoEars`, clean `main`, synced with origin at survey.
- Existing local `feature/community-board-readability` is an ancestor of main; no linked task worktree or active claim conflicts.
- Proposed branch: `feature/ears-table-readability`.
- Brain Feature Agent: small, direct task; `start_library` then `ship_library`; no relevant Memory matches.
- Heart entry: STALE; planning may proceed, shipping requires a fresh gate.
- Plan approved on 2026-10-08; implementation authorized.

## Implementation handoff — 2026-10-08

- PR: https://github.com/PyAutoLabs/PyAutoEars/pull/24; commit `eaf7cd3`.
- Worktree: `/home/jammy/Code/PyAutoLabs/.worktrees/ears-table-readability/PyAutoEars`; branch `feature/ears-table-readability`.
- Approved scope complete: simplified titles and details, dates in both tables, recurring placeholder removed.
- Modified `ears/board.py`, `ears/presentation.py`, `ears/collect.py`, `REFERENCE.md`, and relevant tests/browser harness.
- Validation: 106 Ears tests; 29 Brain adapter tests; identical adapter response decisions with/without optional dates; Chromium 390/1280px light/dark checks; generated state valid.
- Logs and preview screenshots: worktree `_site/pytest.log`, `_site/adapter-tests.log`, `_site/browser.log`, `_site/browser-fixture/`.
- Heart STALE: release validation incomplete: no rehearsal for current source. Development PR permitted, no release requested.
- No source work remains. Await human `/prm`; merge and deployment not performed.
