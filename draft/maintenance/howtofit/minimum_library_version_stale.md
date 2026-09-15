# HowToFit's version floor is two months stale, so every reader gets a "pull the workspace" warning

Type: maintenance
Target: HowToFit
Repos:
- HowToFit
Themes:
- tutorials
- version-handshake
Difficulty: small
Autonomy: safe
Priority: normal
Status: formalised
Consequence: notify
Review-minutes: 5
Unattended: ready
Witness: on a fresh clone of HowToFit main with the current released `autofit`, `python3 -c "import autofit"` emits no workspace-version UserWarning.
Filed: 2026-09-15

`HowToFit/config/general.yaml:39` records
`version.minimum_library_version: 2026.7.9.1`. autonerves warns once the
installed library is more than `_STALENESS_WINDOW_DAYS = 30`
(`autonerves/workspace.py:18`) newer than that floor, so with any current
library the first `import autofit` prints:

    UserWarning: The workspace at .../HowToFit records library version
    2026.7.9.1, but the installed library is 2026.8.17.1 — more than 30 days
    newer. The workspace examples and configs may lag the installed API.
    Pull the latest workspace:
        cd .../HowToFit && git pull origin main

The advice is wrong for the reader it reaches: they are already on main. It is
the first thing a workshop attendee sees, before any tutorial output.

The floor is bumped deliberately and never by the release pipeline
(`PyAutoHands/docs/internals.md:63`), so it only moves when someone moves it.
Bump it to the release this ships with, and consider whether the same drift is
sitting in the sibling teaching repos (HowToGalaxy, HowToLens) and the
workspaces.
