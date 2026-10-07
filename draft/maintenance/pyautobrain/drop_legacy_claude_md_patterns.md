# Drop the tolerated-legacy CLAUDE.md patterns in _clone.py and regroup_workspace.py

Type: maintenance
Target: pyautobrain
Repos:
- @PyAutoBrain
Difficulty: small
Autonomy: supervised
Consequence: judge
Priority: low
Status: draft — blocked-by: the PyAutoMind#482 `session_hook_propagate` removal wave (human-dispatched)
Filed: 2026-10-07

- Split out of `absorb-claude-notes-agents-md` at close-out — the rest shipped in
  `complete/2026/10/absorb-claude-notes-agents-md.md`
  (https://github.com/PyAutoLabs/PyAutoBrain/pull/493); this is what remains of
  its "no file in PyAutoBrain names CLAUDE.md" done-when.

## Scope

PyAutoBrain#493 kept `CLAUDE.md` as a tolerated-legacy file pattern in
`agents/conductors/clone/_clone.py` and `bin/regroup_workspace.py`, because the
assistants' `scripts/CLAUDE.md` pointers still exist and their
`clone-boundary.yml` CI would fail on unclassified files. Once the PyAutoMind#482
propagation wave (and the nested-pointer follow-up) has removed those files,
drop the legacy patterns and their tests.

## Done when

No file in PyAutoBrain names `CLAUDE.md` as a thing that exists; Brain suite
green; the assistants' `clone-boundary.yml` still passes.
