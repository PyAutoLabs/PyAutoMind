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

Also fold in (human-directed 2026-07-10): the RTD template-family
walkthrough — extend `PyAutoBrain/docs/adoption/guide.md` (and the
satellites page where apt) with the "Use this template" path: the
PyAutoProject family (public since 2026-07-10) + the spawned
Mind/Memory templates as the concrete steps 1-2 of adoption. Ships with
this task's PyAutoBrain PR so the docs land alongside the templates they
describe.
