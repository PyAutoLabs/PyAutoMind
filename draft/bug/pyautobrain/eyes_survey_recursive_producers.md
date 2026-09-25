# Eyes survey scans producers non-recursively, so nested visualization/ producers read as ORPHAN trees

Type: bug
Target: PyAutoBrain
Repos:
- PyAutoBrain
Themes:
- visualization
Difficulty: small
Autonomy: safe
Priority: normal
Epic: pyautoeyes-birth
Consequence: notify
Witness: a hermetic test in `tests/test_eyes_conductor.py` that fabricates the nested layout `scripts/<domain>/visualization/visualization.py` + `scripts/<domain>/images/visualization/*.png` and asserts the survey reports the producer as present (no ORPHAN-IMAGES flag, staleness computed) — red on main, green after the fix.
Filed: 2026-09-25

`agents/conductors/eyes/_eyes.py` finds producers with
`domain_dir.glob("*.py")` — a non-recursive scan of `scripts/<domain>/*.py`.
`autolens_workspace_test` keeps its producers one level deeper, at
`scripts/<domain>/visualization/visualization.py` (imaging, interferometer,
multi_dataset, point_source; only `cluster/visualization.py` is flat). Its
image trees under `scripts/<domain>/images/<stem>/` therefore have no matching
producer: the survey reports them as ORPHAN trees and never computes
staleness for them. The hermetic test fabricates the flat layout only, so it
does not see the mismatch.

Found while planning the `autolens_visualization` birth (PyAutoMind#436), which
sidesteps the bug by using the flat layout; `autolens_workspace_test` stays
affected as the secondary Eyes target.

Fix: scan recursively (or also glob `visualization/*.py` under each domain),
keying producers by stem as today; add the nested-layout test above.
`_eyes.py` must stay repo-name-free (tenant firewall).
