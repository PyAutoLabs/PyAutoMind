# Pulse campaign control room and task migration

Type: feature
Target: PyAutoPulse
Repos:
- PyAutoPulse
- PyAutoMind
Status: awaiting-merge
Issue: https://github.com/PyAutoLabs/PyAutoPulse/issues/6
Issued: 2026-10-03
Filed: 2026-10-03

## Original request

I have not looked at the PyAutoPulse dashboard yet but basically I want it to mirror PyAutoCortex was a table of active campaigns (profilijg specifci) a single copyable prompt at the top to get all updates which will mean all profiling work is managed in a single chat from now on. I also want all profiling tasks in PyAutoMind to move to PyAutoPulse as active tasks listed under the table. Then all the profiling info itself further down. For that initial prompt, it should be I can add to it if I want to direct a specific campaign suggest a specific idea albeit like Cortex I could just tell a prompt at the start.

## Plan

- Add a single editable check-in prompt above a campaign table.
- Give Pulse a validated campaign/task ledger and migrate profiling prompts with provenance.
- Preserve existing task gates and retain the detailed measurement dashboard below.
- Document one-chat check-ins, task updates and bounded development handoffs.
- Validate renderer, task links, migration coverage and repository checks.

Tier: undeclared — merge mode: human /prm.

Implementation: `PyAutoPulse/pulse/campaigns.py`, `campaigns.yaml`, `tasks/`,
`CHECKIN.md`, board/CLI integration and regression tests. Mind's migration record
and routing link replace duplicate queued work; historical completion records remain.
Project measurement producers and scientific acceptance criteria stay authoritative.
