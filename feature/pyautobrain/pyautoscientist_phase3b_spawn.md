# PyAutoScientist 3b-1: implement spawn (fresh-slate generator)

Type: feature
Target: PyAutoMind
Repos:
- PyAutoMind
- PyAutoMemory
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: draft — issue when phase3a ships

Implement `PyAutoMind/scripts/spawn.py` against
`docs/pyautobrain/spawn_spec.md` (the settled partition rules — follow
them mechanically, no re-litigating). Outputs: PyAutoMind-template and
PyAutoMemory-template repos + the template family's stamped mechanical
layers. Add a CI drift job (re-run spawn, fail on diff — the repos_sync
pattern). A `/spawn` skill wraps it (dry-run default, --apply gated).
