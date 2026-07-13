## health-api
- issue: https://github.com/PyAutoLabs/PyAutoBrain/pull/19
- completed: 2026-07-07
- repos: PyAutoMind (PR #35), PyAutoHeart (PR #31), PyAutoBrain (PR #19), all squash-merged; local ~/.bashrc
- branch: feature/health-shell-api (Mind), feature/health-full-mode (Heart+Brain)
- validation:
  - shell: sourcing health_{sync,release,audit}.sh + health.sh defines the `health` dispatcher; passthrough verified (bare/sync/release <dir>/audit/help/unknown)
  - installer: `/pyauto-status-full` pruned; `/health` sole health command; all legs reference-only
  - bashrc: PyAuto()/PyAutoGPU()/PyAutoNoJAX() call `health`; no `pyauto-status` refs remain
  - Copilot review: #31 + #19 clean; #35 → 2 findings (dispatcher shift fragility + OWNERSHIP table style), both fixed
- notes: |
    Adopted the health vocabulary across BOTH surfaces. Claude: /health spans
    check / status / full (folded in the last standalone command
    /pyauto-status-full). Shell: renamed pyauto_status/-full/-audit scripts +
    functions to a single `health` dispatcher (health = git-sync, health release,
    health audit; helpers health-report/json/triage). Door = PyAutoBrain,
    procedures = Heart references, shell tools = PyAutoMind/scripts. Completes the
    health-surface consolidation begun in health-one-door. No back-compat aliases.
