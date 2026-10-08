Shipped in PR #34 (merge 6ea549506d1a24df782d635130f5a3fd87468600). Broca is registered after Cortex with standard navigation, overview and dashboard embedding. Uses the supported no-feed state until a producer feed exists.

Validation: 10 Node tests and Chromium mobile/desktop (390px, 1440px) navigation, overview and deep-link reload checks passed. No PR CI is configured; the user explicitly invoked prm after the exception was disclosed and approval requested. Feature ancestry confirms the entire branch merged. Pages deployment runs from main.

## Original prompt

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
