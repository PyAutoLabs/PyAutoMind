# `data_preparation/manual/mask_irregular` silent failure — all 4 imaging repos (parked NEEDS_FIX)

Type: bug
Target: autogalaxy
Repos:
- PyAutoArray
- PyAutoGalaxy
- autogalaxy_workspace
- autolens_workspace
- HowToGalaxy
- HowToLens
Difficulty: small
Autonomy: supervised
Priority: normal
Status: formalised

The SAME script fails "silently" (no traceback captured) across all four imaging repos — one root
cause, one fix propagates to 4 markers. Parked 2026-04-10.

Affected `imaging/data_preparation/manual/mask_irregular` in: autogalaxy_workspace, autolens_workspace,
HowToGalaxy, HowToLens (remove each NEEDS_FIX from config/build/no_run.yaml once green).

First step: run autogalaxy_workspace/scripts/imaging/data_preparation/manual/mask_irregular.py directly
on clean main (no build harness) and capture the real error — "silent" means the build's timeout/exit
masked it. Likely a GUI/interactive dependency or an API drift in the irregular-mask drawing helper.
If it is genuinely GUI-only (cannot run headless), reclassify to a no_run "GUI scripts cannot be run"
marker instead of NEEDS_FIX (see the gui/* precedents).
