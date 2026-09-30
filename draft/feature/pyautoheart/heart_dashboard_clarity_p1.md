# Heart clarity PR A: readable layout, lyric header, all-tier actions and a v0 systematic prompt

Type: feature
Target: PyAutoHeart
Difficulty: medium
Autonomy: human-required
Status: draft
Priority: high

@PyAutoHeart. Parent intent, verbatim request, findings, design and the Fable review (2026-09-30) with its numbered amendments: `heart_dashboard_clarity.md` in this directory. Human approved the amended plan on 2026-09-30, including neutral headings.

Scope (parent detailed step 2, the display half of step 1, the CLI half of step 4, applicable step 5 validation):

- Readability: primary text ≥1rem, non-monospace summaries, detail density reduced; structural bolding of durations where `_unit_import_details` / `_unit_suite_details` already build strings from fields (no prose parsing). Contrast already passes 4.5:1 — the target is size, typeface and density.
- Lyric header: the exact lyric *[these guys are giving me life]* in the hero `lede` (or one line directly under it), type-only styling with the existing family accent, no second palette (amendment 8).
- All applicable tiers shown in HTML and JSON (rewrite `tests/test_dashboard.py:1266-1276` deliberately); `--md-brief` stays one-tier (amendment 12).
- `<details>`/`<summary>` disclosures for passing inventories and diagnostics; summaries keep counts and status. Preserve the 34rem card layout and 375/390px overflow guards in `_EXTRA_CSS` (D:1839-1872) and add a test that long names in `<summary>` wrap (amendment 11).
- Prominent worded buttons on the first screen: “Refresh all missing evidence” (existing `build_stale_plan`) and “Fix Heart systematically” (v0, below). Heart-scoped `copyCmd` override with aria-live success/failure feedback, selectable `<pre>` fallback for both prompts, 44px targets, worded faces “copy prompt” / “copy command” (amendment 7).
- v0 `fix all`: a pure prompt builder over payloads that exist today (`blockers`, `stale_plan`, `Section.action`, drift and timing actions), read uncapped; additive JSON `fix_plan`; `pyauto-heart fix all` topic wired in `heart/fix.py:251-277`, the case list at `bin/pyauto-heart:388` and `help_fix` at `bin/pyauto-heart:367-379`; new `tests/test_fix.py` or an explicit extension of `test_dashboard.py` (amendments 3, 5). The prompt carries the five instructions from parent step 4. Nothing new enters `blockers`.

Preserve verdict/score, schema compatibility (additive only) and the Brain board's reads of `blockers`, `stale_plan` and `performance`. After merge, dispatch `heart-health.yml` so Pages reflects the change (amendment 13).

Use branch `feature/heart-dashboard-clarity`. Follow start-dev → start-library → ship-library for organ tooling. Recheck claims and sync before setup. Implementation approved on 2026-09-30; existing dependency and shipping gates still apply.
