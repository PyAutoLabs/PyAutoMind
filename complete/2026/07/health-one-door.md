## health-one-door
- issue: https://github.com/PyAutoLabs/PyAutoBrain/pull/17
- completed: 2026-07-07
- repos: PyAutoBrain (PR #17, squash-merged), PyAutoHeart (PR #30, squash-merged); PyAutoMind (README refs), local .bashrc + .claude
- branch: feature/health-one-door
- validation:
  - installer: `/pyauto-status.md` + `/health_check` pruned; only `/health` remains; both legs (`health_sweep/`, `pyauto-status/`) install as reference-only, not commands
  - Copilot review: #17 clean; #30 → 4 findings on the adopted sweep doc, all fixed (workspace scope reconciled to /smoke_test)
  - line-count guard: all primary skill files ≤200 lines
- notes: |
    Consolidated the health surface behind a single /health door (delivering the
    brain-agent-commands follow-up). Modes: /health (Brain conductor loop),
    /health check (green-light sweep, was /health_check), /health status
    (active-work dashboard, was /pyauto-status). Door lives in PyAutoBrain;
    procedures are Heart references (health_sweep/, pyauto-status/). Retired
    /pyauto-status + /health_check as top-level commands; adopted the orphaned
    untracked health_check sweep into PyAutoHeart. Separately fixed ~/.bashrc:
    the pyauto-status/-full/-audit shell helpers were sourced from the dead
    PyAutoPrompt/scripts/ path (silent [ -f ] guard) → repointed to
    PyAutoMind/scripts/ with a loud warning on miss. Left alone: /pyauto-status-full
    (separate axis; flagged) and the shell pyauto-status function.
