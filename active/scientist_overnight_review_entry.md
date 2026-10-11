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

## User clarification

I still dont really understand why brain is collatig over night work, or work for the past 24 hours? Cant scientist just determine thison the fly?

## Final bounded implementation

1. Remove the overnight section/navigation and scheduled workflow polling from Brain's dashboard. Keep the deprecated board.json overnight key empty for compatibility and stop generating overnight status items/verdicts. Retain explicit diagnostic helpers and actual owner workflows; no release/checking schedule changes.
2. Reuse Scientist's existing check-in, which already handles overnight/24-hour/custom-period summaries. Make on-demand querying explicit: consult dated owner records and relevant workflow runs covering the requested interval, account for pagination/access gaps, distinguish blocked/pending/failed/absent evidence. Do not add another panel, feed, scheduled digest or ledger.
3. Update owner instructions, REPORTING.md and regressions proving dashboard collection never calls the overnight API collector, retired observations cannot reappear on Brain, and its shared state schema remains valid. Test both boards and independently review.
4. Open coordinated judge-tier PRs. Human /prm, then publish both boards. This is a reporting ownership correction; independent starter acceptance and optional activation remain later.
