## dna-cockpit-registration
- issue: https://github.com/PyAutoLabs/pyautolabs.github.io/issues/31
- completed: 2026-10-08
- library-pr: https://github.com/PyAutoLabs/pyautolabs.github.io/pull/32

Added DNA after Insight in the public cockpit registry, giving it the standard overview card, navigation and embedded board using its live state.json feed. Updated canonical-order guidance. Scientist's separately published dashboard was refreshed and verified to include DNA.

Validation: 10 existing Node tests passed; browser navigation and DNA iframe target passed at 390px and 1440px. No PR checks are configured; human explicitly authorized merge with “I authorize” after this was disclosed. PR32 merged as 8edcfdd4b449c18031d34388d4da006efef1a94f. Git ancestry confirms the complete feature branch landed. Pages deployment follows the main-branch merge. No scientific packages or environments changed.

## Original prompt

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
