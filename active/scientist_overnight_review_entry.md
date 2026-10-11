# Move overnight review entry to Scientist

Type: feature
Issued: 2026-10-11
Issue: https://github.com/PyAutoLabs/PyAutoScientist/issues/69
Epic: scientist-adoption-pilot
Consequence: judge
Target: PyAutoScientist
Repos: PyAutoBrain, PyAutoScientist
Prerequisite: scientist-local-discovery merged (Brain#518)

## Original request

I also dont know whwy Brain has "Review oernight work" that is a Scientist task, it could be a brain agent I guess but put it there

## Plan

Move the Review overnight work user-facing board section/navigation from Brain to Scientist; retain Brain agent execution and authoritative source evidence. Read board/_board.py and Scientist organism_board.py contracts before selecting feed integration. Preserve exceptions, pending/missing runs and evidence dates; do not copy a competing ledger. Validate both boards. Brain#518 is merged; both repositories are unclaimed.

## Bounded implementation

1. Remove the overnight section and its navigation entry from Brain HTML/Markdown. Retain Brain collection, JSON, status feed and agent execution. Make missing-run observations explicit in the existing state feed and retain run creation timestamps as evidence text.
2. Add a native expandable Review overnight work section to Scientist, reading only overnight-ID items from its already validated connected Brain state feed. Keep pending, blocked, unreadable and absent runs distinguishable; show the source snapshot timestamp, evidence links and original reason. Empty feeds say only that no items were reported, not that overnight work succeeded. Render a selectable review prompt directing the existing workflow without running actions.
3. Reuse existing browser collection, identity validation and cache/freshness handling. Update only the section's evidence body during refresh, preserving disclosure and prompt state. Show no section for a Scientist with no Brain connection; do not add network endpoints or copied ledgers.
4. Verify server rendering and browser refresh, unavailable/stale feeds, escaping, empty independent profiles and Brain feed compatibility. Run targeted Brain tests and full Scientist Python/JS suites; independent review. Open coordinated PRs, judge-tier human /prm. Publish Brain before Scientist after merge.

This task is presentation/routing, not optional-organ activation or starter-harness acceptance.
