# Visualization-refactor asserts: dataset.png missing + tangential critical curve #1280 (parked)

Type: bug
Target: autolens
Repos:
- autolens_workspace_test
- PyAutoLens
- PyAutoFit
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: formalised

Two visualization/geometry assert failures the sweep surfaced:
- `imaging/visualization` — `AssertionError: dataset.png missing after visualization refactor`
  (autolens_workspace_test NEEDS_FIX): a subplot/output path renamed or dropped in a viz refactor.
- **#1280 tangential critical curve family** — the pre-tracked `zero_contour` / "no tangential
  critical curves recovered" asserts (self-documented "PyAutoFit #1280 family"), which also block
  cluster/visualization from fully passing.

First step: dataset.png is likely a quick assert/path update (check what the viz refactor renamed).
The #1280 family is the deeper one — confirm current status of PyAutoFit#1280 before investing;
the critical-curve recovery fails on small grids, so verify at full data first.
