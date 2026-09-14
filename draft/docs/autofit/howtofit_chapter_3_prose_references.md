# PyAutoFit — two stale "HowToFit chapter 3" references after the chapter_advanced rename

Type: docs
Target: PyAutoFit
Repos:
- PyAutoFit
Themes:
- docs-hub
- autofit
Difficulty: trivial
Autonomy: safe
Priority: low
Status: formalised
Consequence: notify
Review-minutes: 5
Unattended: ready
Filed: 2026-09-14

Split out of `active/colab_visibility_and_chapter_advanced_rename.md`
(HowToFit#53), which renames `HowToFit/scripts/chapter_3_graphical_models/` to
`scripts/chapter_advanced/`. Two PyAutoFit files name that chapter in prose:

- `autofit/messages/truncated_normal.py:328` — "built on ``af.TruncatedGaussianPrior`` (e.g. HowToFit chapter 3)."
- `test_autofit/graph_spec/graphical_doubles.py:81` — "whose own ``mean`` and ``sigma`` are free (HowToFit chapter 3, tutorial 4)."

Neither is a URL, so nothing breaks — they just name a chapter that no longer
exists. Reword to "the HowToFit advanced chapter" (tutorial numbers within the
chapter are unchanged, so "tutorial 4" still resolves).

Deliberately **not** folded into HowToFit#53: PyAutoFit is a library, so
including two lines of prose there would have pulled a library PR and the
library-first merge gate into a workspace-only task (human decision,
2026-09-14). It is safe to ship this at any time — before or after #53 — since
the strings are wrong either way only in the window between the rename merging
and this landing.

Verify: `grep -rn "HowToFit chapter 3" PyAutoFit/` returns nothing.
