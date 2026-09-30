## Summary

A PyAutoMind draft was counted as an open critique of every instance whose repo name appeared in its text, so the cti `render.yml blocked` draft (which cites `autofit_visualization` as the working precedent) showed under both `fit` and `cti`: 8 critiques for 7 drafts on the PyAutoEyes dashboard and in `state.json`. `find_critiques()` now attributes a draft to the one instance its light header names (`Target:`, else the first `Repos:` bullet matching a registered instance's repo or name); text mention remains the fallback only for drafts whose header names no registered instance. The registry is threaded through `gather()` and the board CLI. Witness: the new attribution test was red against the unfixed function and is green after; 77 tests pass; regenerated dashboard shows lens 3, galaxy 2, fit 1, cti 1.

## Notes

- Follow-up from PyAutoEyes phase 5 (PyAutoEyes#6, record `complete/2026/09/eyes-retire-duplicates-surfaces.md`).
- Heart YELLOW at ship (HowToGalaxy / HowToLens open PRs and the reasons already acknowledged on #6); PR CI (lint) green; merged under the human's "go".

## Original prompt

# Eyes dashboard counts one Mind draft as a critique of two instances when it mentions both

Type: bug
Target: PyAutoEyes
Repos:
- PyAutoEyes
Themes:
- visualization
Difficulty: small
Autonomy: safe
Priority: low
Epic: pyautoeyes-birth
Consequence: notify
Witness: a hermetic test in `tests/test_context.py` (or `test_board.py`) with two registered instances and one Mind draft whose body names both repos, asserting the draft is attributed to exactly one instance (its `Target:`/primary repo) — red on main, green after the fix.
Filed: 2026-09-30
Issued: 2026-09-30

`eyes.context.gather` collects "open critiques" as the PyAutoMind drafts that
mention an instance by text. The draft
`draft/bug/autocti_visualization/render_yml_blocked_until_pyautocti_release.md`
mentions both `autofit_visualization` (as the working precedent) and
`autocti_visualization`, so the dashboard and the new `state.json` feed count
it once for `fit` and once for `cti` (phase 5 regen: 8 critiques for 7
drafts). Attribute a draft by its `Target:` / first `Repos:` entry, falling
back to text mention only when neither names a registered instance.

Found while regenerating the dashboard in PyAutoEyes phase 5 (PyAutoEyes#6, PR #7).
