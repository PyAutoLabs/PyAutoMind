# HowToFit advanced-chapter references

- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1699
- pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1700
- merged: 2026-10-17
- merge: 99d714c71d1eed3d17d718607da430be384af5f2

Updated the two stale chapter-3 references in PyAutoFit docstrings to the advanced chapter, retaining tutorial 4. No runtime changes.

Validation: exact-head Actions passed all five jobs: generated-search-docs, docs-build, unit tests on Python 3.12/3.13 and no-JAX. Local serial suite had 3698 passes and 115 skips; all 19 missing-dependency failures passed after installing declared Nautilus/Zeus dependencies. Parallel test collection has existing address-dependent IDs, so local validation used serial execution.

Human `Prm` authorized the merge; freeze clear, no review objections, unchanged authored head. Git ancestry proved head 73008021aecc1b90d9b6428116eccf38234e8570 is on origin/main. Issue closed as completed. No release performed. Flat checkout retained; no task worktree existed.

## Original prompt

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
Witness: `grep -rn "HowToFit chapter 3" PyAutoFit/` returns nothing; the two sites now read "the HowToFit advanced chapter" with "tutorial 4" kept.
Review-minutes: 0
Unattended: ready
Issued: 2026-10-17
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
