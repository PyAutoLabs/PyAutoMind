# autolens_profiling: cockpit feed stops claiming `organ: profiling`

Type: feature
Target: autolens_profiling
Repos:
- autolens_profiling
Themes:
- profiling
Difficulty: small
Autonomy: supervised
Priority: normal
Status: draft
Consequence: notify
Witness: `dashboard/state.json` validates with `PyAutoBrain/board/_state.py`; its `organ` is no longer `profiling`; `scripts/misc/test/test_build_dashboard.py` green; the project's own Pages badge still renders
Review-minutes: 3
Unattended: ready
Filed: 2026-10-02
Epic: profiling-organ-birth
Blocked-by: evaluation-grid-cap-field (claims autolens_profiling)

Split out of phase 3 (`complete/…/pyautopulse-brain-board-cockpit` once shipped; PyAutoBrain#450) on
2026-10-02 because `autolens_profiling` was claimed by another task. The organ **PyAutoPulse**
(key `pulse`) now owns the cockpit card and feed (`PyAutoPulse/state.json`); the Brain board never
read the project feed, so nothing on the Brain side transitions.

## Task

`scripts/misc/tooling/build_dashboard.py` `build_state()` (~:410-447): the project feed stops
claiming to be an organ. `board/_state.py` accepts any non-empty `organ` string, so write
`organ: "autolens_profiling"` (a project label; `repo` unchanged), keep `pages_url`, keep the
drift items and their `/profiling triage …` prompts for the project's own Pages badge. Update
`scripts/misc/test/test_build_dashboard.py:226,372` (`["organ"] == "profiling"`) and the contract
test at :166-185 accordingly. `dashboard/README.md:13` and `AGENTS.md:44-46`: say the feed is the
project's own badge feed and that the Brain/cockpit read the PyAutoPulse organ feed. Record the
choice in `PyAutoPulse/REFERENCE.md` is NOT needed here (the organ doc covers it in phase 3).

## Out of scope

Any change to `summary.json` (the `profiling-summary@1` contract); the `pulse-refresh` dispatch
sender (separate prompt).
