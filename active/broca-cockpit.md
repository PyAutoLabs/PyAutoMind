# Complete Broca cockpit registration
Type: bug
Target: pyautolabs.github.io
Consequence: judge

## Original request
I dont see broca on cockpit?

## Context and approved scope
Complete the already approved Broca dashboard integration. Broca is public and its Actions Pages dashboard is live, but @pyautolabs.github.io has a separate cockpit ORGANS registry that omitted Broca.

## Plan
- Register Broca after Cortex in cockpit/index.html, using feed: null because Broca does not publish state.json.
- Update the documented canonical order; preserve standard overview and iframe routing.
- Run existing Node checks and verify navigation at mobile and desktop widths.
- Ship the narrow fix using existing Heart YELLOW acknowledgement and all-merges authorization, subject to the prm no-checks gate.

Tier: judge — merge mode: human /prm (already requested for Broca integration).

Issue: https://github.com/PyAutoLabs/pyautolabs.github.io/issues/33
Issued: 2026-10-08
