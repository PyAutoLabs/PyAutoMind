# Compact Memory board and one-tap reading queue

Issued: 2026-10-14
Issue: https://github.com/PyAutoLabs/PyAutoMemory/issues/130
Work-type: feature
Difficulty: medium

Target: @PyAutoMemory

## Original request (verbatim)

PyAutoMemory: Remove all stuff between the copy check in prompt box and "arxiv Inbox", its not useful.

I think we should still keep a "catch up" button and tab, but its just concisely the finroamtion on when the catch 
up is needed from and a clickable prompt button.

This is doable but looks likwe e need to sort GitHub token management:
- Having to put a github issue up to put something on the to read list is too much time, I want to put like 5
papers with 1 day left there today but it should be a single click and done, is that possible?

## Approved scope

User approved: "do it, we will sort token stuff in a bit".

- Clear the space between the check-in panel and arXiv inbox.
- Keep Catch up as an always-visible tab with a concise date/status and copy-prompt button.
- Move pending filings to their own section and metadata links to the footer. Relocate existing one-tap control beside inbox actions without changing token behavior.
- Token management and batch-selection changes are deferred.

## Detailed implementation plan

In scripts/board.py, update _catch_up_html and _catch_up_md to display the coverage start and due date, with honest unknown status and the existing prompt action. Keep the underlying catch-up model and feed semantics unchanged. In _render_html, make Catch up navigation unconditional, place the inbox directly after the orchestration panel, and place Catch up and pending filings after reading content. Preserve the shared theme/navigation components. Update tests/test_board.py for healthy/stale/unknown summaries, section order, existing prompt and action preservation. Run targeted and full repository checks and inspect rendered output.

Branch survey: PyAutoMemory main has existing bibliography/wiki edits; no conflicting active claim. Recent branches: main, chore/session-start-hook-regen. Use isolated .worktrees/compact-memory-board/PyAutoMemory from origin/main.

Suggested branch: feature/compact-memory-board
Tier: undeclared — merge mode: human /prm.
