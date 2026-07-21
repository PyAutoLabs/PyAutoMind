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
Status: resolved-by-fold (2026-07-21)

RESOLUTION (2026-07-21): The bug was already fixed by library evolution — the
2026-04-10 "silent failure" was `Convolver.from_gaussian` / `convolved_image_from`
API drift, since resolved by the PyAutoArray convolver consolidation (#360/#361).
Verified green on clean main via the build's own `execute_script` runner:
autogalaxy_workspace PASSED 8.6s, autolens_workspace PASSED 14.0s
(`has_failures=False`; runs headless, no GUI dependency — NOT a gui/* reclassify).
The only work was removing the 4 NEEDS_FIX markers. All 4 no_run.yaml files were
claimed by two active tasks editing those same files, so the removals were FOLDED
into the owners rather than opened as a competing branch:
  - autogalaxy_workspace + HowToGalaxy → pix-inversion-not-positive-definite (#140):
    markers removed on branch (commits 9258bf0c, b2b53fc); ships with that PR.
  - autolens_workspace + HowToLens → slam-adapt-inversion-cascade (#300): tracked
    as a TODO on that task (its worktree was absent from disk); note on #300.
HowToGalaxy + HowToLens markers were orphaned (no such script in those repos).
Drop this prompt once both owning tasks merge.

The SAME script fails "silently" (no traceback captured) across all four imaging repos — one root
cause, one fix propagates to 4 markers. Parked 2026-04-10.

Affected `imaging/data_preparation/manual/mask_irregular` in: autogalaxy_workspace, autolens_workspace,
HowToGalaxy, HowToLens (remove each NEEDS_FIX from config/build/no_run.yaml once green).

First step: run autogalaxy_workspace/scripts/imaging/data_preparation/manual/mask_irregular.py directly
on clean main (no build harness) and capture the real error — "silent" means the build's timeout/exit
masked it. Likely a GUI/interactive dependency or an API drift in the irregular-mask drawing helper.
If it is genuinely GUI-only (cannot run headless), reclassify to a no_run "GUI scripts cannot be run"
marker instead of NEEDS_FIX (see the gui/* precedents).
