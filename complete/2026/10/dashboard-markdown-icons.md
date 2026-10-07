# Right-aligned dashboard Markdown icons

Markdown-version links now appear as small document icons at the right of their section heading or utility row. Original destinations remain unchanged. Icons include tooltips, accessible names, visible keyboard focus and 44px click targets; activating them does not toggle a disclosure.

- Issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/498
- Shared layout: https://github.com/PyAutoLabs/PyAutoBrain/pull/499
- Generated Mind page: https://github.com/PyAutoLabs/PyAutoMind/pull/490
- Validation: 271 focused renderer checks and 40 browser cases across five widths and light/dark. Full suites passed 1270 Brain and 695 Mind tests; remaining environment-sensitive fixture checks passed with worktree overrides removed (4/4 and 7/7).
- Brain CI: Python 3.12, Python 3.13 and documentation jobs passed.
- Mind CI: freshness and privacy checks passed; template-drift publication job is intentionally excluded from pull_request events.
- Heart: the human acknowledged workspace-manifest drift (3 mismatches) and incomplete release rehearsal on 2026-10-07. No library release required.
- Evidence retained locally: tmp/dashboard-markdown-icons-evidence/ in the PyAutoLabs workspace.

Other shared-theme boards receive the icon presentation on their next regeneration. No scientific API or workspace script changes.

## Reconciliation

No sibling prompts were retired. The scoped reconcile flagged `batch_slice.md`, `board_without_gh_phase2_legs.md`, and `brain_board_follow_ups.md` under `draft/feature/pyautobrain/`; these are outside the icon change and remain filed. Follow-up: `/intake reconcile draft/feature/pyautobrain`.

## Original prompt

# Right-aligned dashboard Markdown icons

Issued: 2026-10-07

## Original request

Common for "markdown version" text to be a URL next to dashboard items (e.g. on PyAutoMind) can you make this an icon
and to the right of each, so its more outt he way but still clickable.

## Scope

@PyAutoBrain shared board presentation; @PyAutoMind is the reference dashboard.
Replace visible Markdown-version text links with discreet document icons at the right of their section or header row. Preserve destinations, accessible labels, tooltips, keyboard focus and independent disclosure behavior. Implement centrally where possible and validate affected board consumers; regenerate owned dashboard output through its normal renderer.

## Proposed implementation

Inspect shared board/_theme.py section_layout and the owner renderers. Add a reusable source-link presentation, keeping domain destinations owner-defined. Validate desktop/mobile layout, links and disclosure interactions with existing renderer checks and browser inspection. No scientific or task-lifecycle behavior changes.

Tier: undeclared; human merge.
