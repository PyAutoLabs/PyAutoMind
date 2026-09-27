# Register the profiling run-time dashboard on the Brain board

- Work type: feature
- Target: @PyAutoBrain (board/)
- Epic: profiling-research-wiki (dashboard leg, item 4)
- Autonomy: safe
- Filed: 2026-09-27
- Status: split out of `profiling-runtime-dashboard` (autolens_profiling#345) at ship — PyAutoBrain
  was claimed by `eyes-organ-order`, so the board registration could not ride that PR.

## Original prompt

The run-time-over-time dashboard ships in autolens_profiling#345: `dashboard/index.html` at
<https://pyautolabs.github.io/autolens_profiling/>, with `state.json` beside it as the organ
cockpit feed (`board/state_schema.json` v1, organ key `profiling`, repo `autolens_profiling`,
validated by `board/_state.py` in the repo's `pages_dashboard.yml`). Item 4 of the dashboard
scope is "register the dashboard URL on the Brain board".

## Scope

1. Add the profiling dashboard to the board family the Brain board renders (`board/_board.py`
   `boards`, the family footer in `board/_theme.py`, and the cockpit's organ list if it reads a
   fixed set) so the cockpit shows the `profiling` feed's status and headline beside the organs.
2. The feed's `pages_url` is the dashboard page; its `items` are drift badges with a
   `/profiling triage …` prompt — wire that prompt to the profiling conductor's `triage` verb.
3. `board/AGENTS.md`: one line naming the profiling feed among the sibling boards.

## Out of scope

Organ birth (the dashboard spans one profiling repo today); `repos.yaml`; anything in
autolens_profiling.
