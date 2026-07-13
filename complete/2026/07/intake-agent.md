## intake-agent
- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/21 (closed)
- completed: 2026-07-08
- library-pr: https://github.com/PyAutoLabs/PyAutoBrain/pull/22 (merged)
- notes: |
    Shipped the PyAutoBrain Intake (Conception) Agent — a new conductor that
    turns raw input (idea / bug report / ideas.md bullet) into a formal, headed
    PyAutoMind prompt under <work-type>/<target>/<name>.md. It files a prompt;
    never starts dev (the step before create_issue/start_dev). Conception ->
    Growth, pairing with the Feature Agent's Growth name.

    - Extracted the difficulty heuristic + prompt parsing into a shared read-only
      sizing faculty (agents/faculties/sizing/) consulted by both Intake and the
      Feature Agent, so a persisted Difficulty is the same number the Feature
      Agent trusts (no drift). Feature Agent library-path output regression-clean
      (-183 lines from _feature.py).
    - Organism repos (pyautomind/pyautobrain/pyautoheart/pyautobuild/pyautomemory)
      now resolve as first-class targets — fixes the Feature Agent mis-routing a
      pyautobrain target as "(none resolved) -> research-first".
    - Blessed Difficulty/Autonomy/Priority header keys in PyAutoMind README/AGENTS
      (no YAML; landed on main directly, commit 3322d49). /intake command wired.
    - Copilot review (4 findings, all fixed): implemented ideas.md bullet-marking,
      switched work-type classification to word-boundary _hits, Type: matches the
      destination folder on triage filings, idempotent ideas re-scan.

    Follow-up (deferred to a second PR): census / repair / dashboard — registry
    hygiene + a Mind *backlog* dashboard (distinct from Heart's /health status).
