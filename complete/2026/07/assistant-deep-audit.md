## assistant-deep-audit
- issue: https://github.com/PyAutoLabs/autolens_assistant/issues/35 (closed)
- completed: 2026-07-08
- prs: #36 (46cde1b), #38 (ee40372), #37 (b0ff0f1), #39 (94c3c3e) — all squash-merged
- notes: |
    Deep audit of autolens_assistant, --auto supervised, four phased PRs.
    A: all 19 mature skills read + every recipe symbol introspected against
    the installed stack; 8 repaired (fabricated APIs in al_custom_profile/
    al_run_slam_pipeline, LensCalc move, Nautilus kwarg renames, the open
    PyAutoArray#332 Delaunay trap in al_chain_searches). B: gate/audit
    tooling — per-command PYAUTO_SKIP_API_GATE bypass now works, broken
    stack reported once as env problem (exit 3, hook fails open), grouped
    import walls; 39 tests. C: start-new-project data/ boundary fix, stale
    trailer, wiki sampler tables match dir(af). D: 40 stale-org URLs ->
    PyAutoLabs, cross-harness code-gate self-enforcement in AGENTS.md,
    refresh_api_docs scope parity. Calibration: A/B/C merged-unchanged,
    D amended (mechanical conflict resolution only). Follow-ups: version
    pin waits for release; skill-stub completion still in backlog.
