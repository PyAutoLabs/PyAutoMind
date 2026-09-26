- issue: https://github.com/PyAutoLabs/PyAutoNerves/issues/172 (closed)
- completed: 2026-09-26
- library-pr: https://github.com/PyAutoLabs/PyAutoBrain/pull/422, https://github.com/PyAutoLabs/PyAutoNerves/pull/173 (MERGED)
- workspace-pr: https://github.com/PyAutoLabs/pyautolabs.github.io/pull/15 (MERGED)
- epic: organ-cockpit (human request 2026-09-26: "a simply way for me to view all config file source code entries and options acrosss the repos"; supersedes the same-day "Nerves gets no board" decision)
- heart-ack: "Heart YELLOW (score 85): three pre-existing manifest-drift reasons; live human 'ack and merge' 2026-09-26"
- witness: nerves_board.yml run 36264844580 green with `state: ok`; https://pyautolabs.github.io/PyAutoNerves/ live (332 files / 9 sources / 173 overrides / 14 files with orphan keys / 0 parse errors); search index resolves `positions`; cockpit Nerves card populated. Page layout not checked by eye (no browser in the session).
- decisions: read-only browser (no actions) — grows later; overrides resolved against the whole library stack in autonerves import order (lens → galaxy → array → fit; cti for the cti workspace), prior files compared per Class.param; `build/*.yaml` = workspace tooling group; env-var panel = PYAUTO_* names from autonerves modules with the comment or docstring paragraph; feed yellow on parse errors or orphan workspace keys, never red; Pages site pre-created with the human token (repo token cannot create one).
- drift found (not fixed): 79 orphan keys in 14 workspace files (hpc.live_visual_update, test.check_preloads, version.*, removed subplot_shape.*, label.label.*, delaunay.areas_factor, an autocti visualize/plots.yaml block); typo `fit_imaging {}:` at autogalaxy_workspace/config/visualize/plots.yaml:30.
- follow-ups: "not in use anymore" flag (library YAML keys no library code reads; scan conf.instance[...] lookups) — filed 2026-09-26 as draft/feature/autonerves/organ_cockpit_nerves_unused_keys.md; the orphan-key cleanup per workspace; Eyes feed (last grey card); the sibling-repo reach for the Gut void button.
- summary: Nerves board — read-only Pages browser of every config file and option across 5 libraries + 4 workspaces (index with counts, override map, env-var panel, key search over 4558 entries; one page per repo with line-numbered commented source and prior tables) + state.json feed; scripts/board.py (1137 lines, not packaged), nerves_board.yml sparse-clones the config dirs. Brain 33 + 223 tests, Nerves 201 (16 new).

## Original prompt

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
Issued: 2026-09-26
Issue: https://github.com/PyAutoLabs/PyAutoNerves/issues/172
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
