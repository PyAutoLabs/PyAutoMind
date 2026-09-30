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

`eyes.context.gather` collects "open critiques" as the PyAutoMind drafts that
mention an instance by text. The draft
`draft/bug/autocti_visualization/render_yml_blocked_until_pyautocti_release.md`
mentions both `autofit_visualization` (as the working precedent) and
`autocti_visualization`, so the dashboard and the new `state.json` feed count
it once for `fit` and once for `cti` (phase 5 regen: 8 critiques for 7
drafts). Attribute a draft by its `Target:` / first `Repos:` entry, falling
back to text mention only when neither names a registered instance.

Found while regenerating the dashboard in PyAutoEyes phase 5 (PyAutoEyes#6, PR #7).
