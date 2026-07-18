# Tenant-firewall drift: hardcoded instance facts in Brain organ code

Type: maintenance
Target: pyautobrain
Difficulty: medium
Autonomy: supervised
Priority: normal

Filed by the organism docs sweep (PyAutoMind#84, WS5). The
`repos_sync.py` tenant-firewall check is **red**: instance facts (satellite
repo names, GitHub owners, the local workspace home) are hardcoded in Brain
organ code outside the declared config surfaces (`FIREWALL_ALLOWLIST`). The
sweep did **not** fix these — the remedy is either to *allowlist* each as a
legitimate branded fact (add the file→token baseline in
`PyAutoMind/scripts/repos_sync.py`) or to *refactor* the fact out to a config
surface / the body map. That judgment is per-file and belongs in its own task.

## Findings (from `python3 PyAutoMind/scripts/repos_sync.py`, 2026-07-18)

Pre-existing (present before the sweep):

- `agents/conductors/community/_community.py` — `Jammy2211`, `PyAutoLabs`
  (unlisted file).
- `agents/conductors/workspace/_workspace.py` — `HowToFit`, `HowToGalaxy`,
  `HowToLens`, `PyAutoLabs`, `PyAutoReduce`, `autofit_workspace`,
  `autogalaxy_workspace`, `autolens_workspace` (unlisted file).
- `agents/conductors/clone/_clone.py` — `autofit_assistant` (a *new* token in an
  already-allowlisted file — extend that file's baseline).
- `tests/test_clone_conductor.py` — `autofit_assistant`, `autolens_assistant`.
- `tests/test_community_conductor.py` — `Jammy2211`, `PyAutoFit`, `PyAutoLabs`,
  `PyAutoLens`, `admin_jammy`.
- `tests/test_mind_commit_guard.py` — `/home/jammy`, `PyAutoFit`, `PyAutoLabs`.
- `tests/test_workspace_conductor.py` — `HowToGalaxy`, `HowToLens`,
  `autolens_workspace`.

Introduced by promoting PyAutoScientist to a `category: project` body-map row
(so its name became a hunted token):

- `PyAutoBrain/docs/conf.py` — `PyAutoScientist` (Sphinx `project`/title — a
  legitimate branded fact; allowlist it).
- `PyAutoBuild/autobuild/generate_release_notes.py` — `PyAutoScientist`
  (per PyAutoMind#84; not verifiable in the sweep environment, which had only
  the `jonathanfrawley/PyAutoBuild` fork checked out, not the Hands organ).

Related gap:

- `admin_jammy` has no `AGENTS.md` (reported by `repos_sync` as a
  needs-human-guidance note, not firewall drift).

## Notes

- Promoting PyAutoConf to `category: organ` (WS1) **removed** `PyAutoConf` as a
  hunted token — it can only reduce findings, never add them.
- The conductor-code hits (`community`, `workspace`) are the substantive ones:
  decide allowlist-vs-refactor per the tenant-firewall design (framework organs
  stay adoptable as a config-diff fork). The test hits are lower-risk (test
  fixtures) but still need a baseline entry or a genericisation pass.
