# Relocate the Health Agent into PyAutoBrain

Follow-up to `feature/pyautobrain/health.md`. The first PyAutoBrain specialist
agent (the Health Agent) was implemented and **staged in PyAutoHeart** at
`health_agent/` because PyAutoBrain was not yet in scope. PyAutoBrain is now in
scope, so move the reasoning agent to its canonical home while preserving the
architectural boundary:

```
Mind (intent) -> Brain (reasoning) -> Heart (gate) -> Hands/Build (execute)
```

PyAutoHeart measures health; the Brain Health Agent only reasons over Heart's
outputs and emits a GREEN / YELLOW / RED decision. It performs no checks itself.

## Tasks

1. In `@PyAutoBrain`, create the canonical Health Agent from
   `health_agent/health_agent.md`, registered the way Brain discovers its specialist agents
   (`agents/<name>/AGENTS.md` + an entrypoint script). Keep each `.md` under 200
   lines. Preserve verbatim: adoption of `pyauto-heart readiness --json` as the
   authoritative verdict; reading PyAutoHeart's `capabilities.yaml` as an
   **abstract** provider manifest (do NOT vendor/copy it into Brain); the
   GREEN/YELLOW/RED output schema (Summary / Warnings / Recommendations /
   Blocking Issues); gate semantics; and the hard boundaries (read-and-reason
   only; never write repos, run builds, trigger releases, or implement a check).

2. In `@PyAutoHeart`, remove `health_agent/health_agent.md` and repoint
   `health_agent/README.md` at the new Brain location, but KEEP
   `capabilities.yaml`, `capabilities.md`, and `pyautobuild_boundary_audit.md`
   (Heart self-describing its capabilities belongs in Heart).

3. Update cross-references both ways (Heart README note <-> Brain agent).

4. Validate: PyAutoHeart `pytest tests/` stays green (105 passing); confirm the
   Brain agent can still run `pyauto-heart readiness --json` / `status --json`.
   Do not move or add any gating/check logic into Brain.

## Status: ADDRESSED (2026-06-29)

Completed directly (no PR opened, per request). See `complete.md`:
`health-agent-relocate-brain`.
