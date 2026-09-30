# Heart dashboard PR A: readable status and systematic repair prompts

- issue: https://github.com/PyAutoLabs/PyAutoHeart/issues/245
- library-pr: https://github.com/PyAutoLabs/PyAutoHeart/pull/246
- completed: 2026-09-30
- merge: d9974f92a62195510cab3349add9c1b874d6f991

PR A of the Fable-reviewed, human-approved dashboard plan. Shipped larger prose text, neutral headings, the supplied lyric, native disclosure panels, all-tier HTML reasons, prominent evidence-refresh and systematic prompts, additive JSON fix_plan and `pyauto-heart fix all`. The pure prompt builder retains uncapped source observations and existing action routes. Clipboard controls have 44px targets, truthful success/failure feedback and selectable fallbacks. Existing verdict, score, blockers and performance contracts remain unchanged.

Validation: 1070 Heart tests, 53 Brain consumer tests, generated-payload consumer parity, Chromium at 375/390/1280px, 200% text, long names, keyboard and clipboard rejection/success checks. GitHub run 36765819699: both Python 3.12/3.13 jobs and tenant checks successful. Human prm authorized merge separately from the development-only RED override. Heart's integration-validation failure is not repaired by this UI.

Dashboard deployment dispatched on main: https://github.com/PyAutoLabs/PyAutoHeart/actions/runs/36766128623 (do not imply deployed until the workflow completes).

Remaining approved scope: `draft/feature/pyautoheart/heart_dashboard_clarity_p2.md` (PR B: structured reasons, remedies, score) now ready; `heart_dashboard_clarity_p3.md` (PR C: timing presentation and false-green fix) remains dependent on B. Parent review packet remains in draft as the design reference, not completed implementation scope.

Local evidence archived under `tmp/heart-dashboard-clarity-evidence/` before worktree removal. No scientific data products were produced. Heart is organ tooling, not a released scientific library; no pending library-release obligation was recorded.

## Original prompt

# Heart clarity PR A: readable layout, lyric header, all-tier actions and a v0 systematic prompt

Type: feature
Target: PyAutoHeart
Difficulty: medium
Autonomy: human-required
Status: active
Issued: 2026-09-30
Issue: https://github.com/PyAutoLabs/PyAutoHeart/issues/245
Priority: high

@PyAutoHeart. Parent intent, verbatim request, findings, design and the Fable review (2026-09-30) with its numbered amendments: `draft/feature/pyautoheart/heart_dashboard_clarity.md` in Mind. Human approved the amended plan on 2026-09-30, including neutral headings.

Scope (parent detailed step 2, the display half of step 1, the CLI half of step 4, applicable step 5 validation):

- Readability: primary text ≥1rem, non-monospace summaries, detail density reduced; structural bolding of durations where `_unit_import_details` / `_unit_suite_details` already build strings from fields (no prose parsing). Contrast already passes 4.5:1 — the target is size, typeface and density.
- Lyric header: the exact lyric *[these guys are giving me life]* in the hero `lede` (or one line directly under it), type-only styling with the existing family accent, no second palette (amendment 8).
- All applicable tiers shown in HTML and JSON (rewrite `tests/test_dashboard.py:1266-1276` deliberately); `--md-brief` stays one-tier (amendment 12).
- `<details>`/`<summary>` disclosures for passing inventories and diagnostics; summaries keep counts and status. Preserve the 34rem card layout and 375/390px overflow guards in `_EXTRA_CSS` (D:1839-1872) and add a test that long names in `<summary>` wrap (amendment 11).
- Prominent worded buttons on the first screen: “Refresh all missing evidence” (existing `build_stale_plan`) and “Fix Heart systematically” (v0, below). Heart-scoped `copyCmd` override with aria-live success/failure feedback, selectable `<pre>` fallback for both prompts, 44px targets, worded faces “copy prompt” / “copy command” (amendment 7).
- v0 `fix all`: a pure prompt builder over payloads that exist today (`blockers`, `stale_plan`, `Section.action`, drift and timing actions), read uncapped; additive JSON `fix_plan`; `pyauto-heart fix all` topic wired in `heart/fix.py:251-277`, the case list at `bin/pyauto-heart:388` and `help_fix` at `bin/pyauto-heart:367-379`; new `tests/test_fix.py` or an explicit extension of `test_dashboard.py` (amendments 3, 5). The prompt carries the five instructions from parent step 4. Nothing new enters `blockers`.

Preserve verdict/score, schema compatibility (additive only) and the Brain board's reads of `blockers`, `stale_plan` and `performance`. After merge, dispatch `heart-health.yml` so Pages reflects the change (amendment 13).

Use branch `feature/heart-dashboard-clarity`. Follow start-dev → start-library → ship-library for organ tooling. Recheck claims and sync before setup. Implementation approved on 2026-09-30; existing dependency and shipping gates still apply.

## Delivery (2026-09-30)

PR https://github.com/PyAutoLabs/PyAutoHeart/pull/246, commit ff05733; implementation complete, awaiting human merge. 1070 Heart tests, 53 Brain consumer tests, browser checks passed. Human task-specific RED override recorded on issue/PR, active.md and autonomy_log.md. Current RED is release integration failure; no claim this UI repairs it. Dispatch heart-health.yml after authorized merge, then resume PR B. Logs and visual previews are in the worktree root.
