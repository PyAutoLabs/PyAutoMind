# Complete DNA cockpit registration
Type: bug
Target: pyautolabs.github.io
Consequence: judge

## Original request
I dont see it on cockpit?

## Context and approved scope
Follow-up to PyAutoBrain#509: DNA organ and Scientist integration are merged and DNA Pages is live, but the separate public cockpit ORGANS registry omitted DNA. Complete the already approved dashboard integration, preserving all other organ entries.

## Plan
- Add DNA after Insight in cockpit/index.html ORGANS with its published state.json feed.
- Preserve standard cockpit rendering and routing; inspect shell caching for delivery.
- Run existing node tests and a browser check for DNA navigation/feed.
- Refresh Scientist's already merged page using its existing workflow.
- Ship a review PR under the existing acknowledged Heart YELLOW reason set.

Tier: judge — merge mode: human /prm.

Issue: https://github.com/PyAutoLabs/pyautolabs.github.io/issues/31
Issued: 2026-10-08
