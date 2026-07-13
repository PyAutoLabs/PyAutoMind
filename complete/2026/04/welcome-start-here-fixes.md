## welcome-start-here-fixes
- issue: https://github.com/PyAutoLabs/autolens_workspace/issues/108
- completed: 2026-04-30
- workspace-pr:
  - https://github.com/PyAutoLabs/autolens_workspace/pull/109
  - https://github.com/PyAutoLabs/autogalaxy_workspace/pull/49
  - https://github.com/PyAutoLabs/autofit_workspace/pull/45
  - https://github.com/PyAutoLabs/HowToLens/pull/4
- notes: Fixed welcome.py bugs across four workspaces. The reported `aa.Array2D` NameError in autolens_workspace was the visible symptom; auditing every workspace's welcome.py + start_here.py surfaced three more independent bugs — `aplt.LightProfile` removed in autogalaxy.plot, autofit_workspace loading a gitignored dataset path, and HowToLens pinned to a non-existent library release `2026.4.21.0`. autofit_workspace switched to synthesising the demo gaussian inline rather than loading from disk, matching the in-memory pattern used by autolens/autogalaxy welcome scripts. HowToLens version pin bumped down to 2026.4.13.6 to match the installed library and the rest of the workspaces — not a release rollback, the 2026.4.21.0 pin in the bootstrap commit was aspirational and never released. HowToLens shipped without the `pending-release` label because the label isn't registered in that repo yet (admin gap, not a blocker). Pre-existing PyAutoFit `xp` API drift in `example/analysis.py` surfaced via overview_1_the_basics.py smoke fail — reproduces on canonical main, deferred to its own task.
