## health-agent-relocate-brain
- issued: issued/health_agent_migrate_to_brain.md
- completed: 2026-06-29
- repos: PyAutoBrain, PyAutoHeart, PyAutoMind
- branch: claude/health-agent-relocate-brain-qh84mk (each repo; no PRs opened)
- validation:
  - PyAutoHeart `pytest tests/` (`105 passed`)
  - `pyauto-brain help health` renders the relocated definition
- notes: |
    Relocated the Health Agent (first PyAutoBrain specialist) from its staging
    home in PyAutoHeart `health_agent/` to its canonical home in PyAutoBrain
    `agents/health/`. Brain's `agents/health/AGENTS.md` is now the canonical
    definition (entrypoint `health.sh` unchanged), preserving verbatim the
    `pyauto-heart readiness --json` adoption, the abstract-provider manifest
    reading, the GREEN/YELLOW/RED output schema (Summary / Warnings /
    Recommendations / Blocking Issues), gate semantics, and hard boundaries.
    Removed `health_agent/health_agent.md` from PyAutoHeart and repointed its README at the
    Brain location; kept `capabilities.yaml` / `capabilities.md` /
    `pyautobuild_boundary_audit.md` in Heart (Heart self-describing its
    capabilities). The manifest is read abstractly from Heart, never vendored
    into Brain. No gating/check logic moved into Brain.
