# Organ cockpit: Nerves board — browse every config file and option across the repos

Type: feature
Target: PyAutoNerves
Repos:
- PyAutoNerves
- PyAutoBrain
- pyautolabs.github.io
Difficulty: medium
Autonomy: safe
Priority: high
Status: formalised
Consequence: glance
Witness: the Nerves board workflow on main is green with the validate step logging state: ok; https://pyautolabs.github.io/PyAutoNerves/ lists every config file of the six libraries and four workspaces with expandable source; a search for 'positions' finds the point-source config keys; the cockpit's Nerves card populates.
Review-minutes: 3
Unattended: ready
Filed: 2026-09-26
Epic: organ-cockpit

The human's request (2026-09-26, verbatim): 'Now do the Nerves board, which should be a simply way for me to view all config file source code entries and options acrosss the repos (e.g their config folders). I'm not sure the dashboard necssarily needs me to put stuff yet, but thats fine well prob grow it as we go'.

This supersedes the 2026-09-26 'Nerves gets no board' decision recorded in the gut-board completion record: the Nerves board is a read-only browser of the configuration layer the Nerves own, not a to-do surface.

1. A Pages board rendered by a script in PyAutoNerves with the shared theme: for every config folder across the library repos (PyAutoNerves, PyAutoFit, PyAutoArray, PyAutoGalaxy, PyAutoLens, PyAutoCTI) and the workspaces that override them (autofit/autogalaxy/autolens/autocti workspace config folders), one section per repo listing each YAML config file with its top-level keys and, expanded on demand, the file's source with its comments (the comments are the option docs) and a link to the file on GitHub. Workspace files that override a library file of the same relative path are shown beside it with the differing keys highlighted. A client-side search box filters by file name or key. Rendered from sparse checkouts of the config folders at workflow time.
2. A state.json cockpit feed (contract PyAutoBrain board/state_schema.json): green when every file parses, yellow with one item per unparseable file or per workspace override whose keys do not exist in the library file, grey when nothing could be collected. Never red.
3. Board family wiring: nerves palette + mark in PyAutoBrain board/_theme.py, nerves: PyAutoNerves in config/policy.yaml boards, the cockpit ORGANS Nerves feed line in pyautolabs.github.io, a Pages publish workflow in PyAutoNerves (the Pages site itself is created once by a human token — the repo token cannot create it).

Out of scope: editing config from the board; a to-do or action surface (may grow later); config diffs across library versions.

Witness: the Nerves board workflow on main is green with the validate step logging state: ok; https://pyautolabs.github.io/PyAutoNerves/ lists every config file of the six libraries and four workspaces with expandable source; a search for 'positions' finds the point-source config keys; the cockpit's Nerves card populates.

<!-- formalised by the Intake (Conception) Agent on 2026-09-26 from user-intake -->
