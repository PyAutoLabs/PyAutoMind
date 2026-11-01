# Chapter 2 contents and source formatting repaired

- issue: https://github.com/PyAutoLabs/HowToLens/issues/116
- completed: 2026-11-01
- workspace-pr: https://github.com/PyAutoLabs/HowToLens/pull/117
- workspace-pr: https://github.com/PyAutoLabs/HowToGalaxy/pull/97
- summary: Restored descriptive contents for Lens lessons 1–4 and complete ordered contents for Galaxy lessons 1–6, corrected source layout/title underlines, and regenerated notebooks/catalogues.

The user reported the problem in Python scripts viewed in PyCharm. The Contents heading was present, but Lens descriptions had been stripped and Galaxy entries omitted or combined actual sections. Older descriptive Lens lists and the short Galaxy summary are retained. Lesson-body wording and executable ASTs are unchanged in all ten revised scripts.

Generation passed 44 Lens and 29 Galaxy targets. Contents-to-section ordering, navigation/banner, tutorial completeness and whitespace checks passed. Each final PR head passed all three workflows/eight jobs, including Python 3.12 and 3.13 smoke. Merge commits: Lens d2140844beb82368fa7348405893e8b839af53d0; Galaxy 1495b4fac964e5a92920a7d429ee766e7fae381b.

Both local canonical main checkouts are updated. No simulation or fit data was produced in this formatting worktree. Heart remained STALE (release validation incomplete: no rehearsal for current source); no release claim. The remaining Chapter 2 and Chapter 3 substantive reviews are separate and unchanged.

## Original prompt

# Chapter 2 contents and formatting repair
Issue: https://github.com/PyAutoLabs/HowToLens/issues/116
Issued: 2026-11-01

Original request: “I think the contents section of all chaper 2 examples is gone and theres formatting issues?”
View: Python scripts in PyCharm.

Restore descriptive contents in HowToLens and complete section-by-section contents in HowToGalaxy. Correct title underline lengths and wrapped list layout. Preserve the lesson body and executable behaviour. Regenerate notebooks/catalogues; compare executable ASTs and contents order, validate navigation and final-head CI. Continue the current Chapter2 PR/merge workflow. Heart STALE: release validation incomplete: no rehearsal for current source.
