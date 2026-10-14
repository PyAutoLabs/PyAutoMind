# Compact Memory board and one-tap reading queue

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

## Proposed implementation (awaiting plan approval)

- Clear the content between the shared check-in panel and arXiv inbox. Move connection controls into the inbox toolbar and pending filings into a separate navigable section.
- Keep an always-available Catch up navigation tab with concise coverage-start / due dates (or unknown status) and a Copy catch-up prompt button. Remove lyric, raw command and explanatory prose from that panel; preserve underlying evidence/feed meanings.
- Reuse existing one-tap issue API transport. Improve token setup, expiry/permission errors, duplicate-click protection and truthful submitted/failed feedback. Scope the fine-grained token to PyAutoLabs/PyAutoMemory with Issues read/write. Do not infer token issue permission from repository permissions.push or expose tokens in generated files/logs.
- Default scope is one click per paper. Bulk select/add is optional pending user preference; do not silently expand to a new authentication service.

## Detailed plan and validation

In scripts/board.py, adjust render_html navigation/section placement, _catch_up_html and matching markdown rendering. Reuse Brain shared navigation/panel components without changing shared implementation. Update _EXTRA_JS one-tap controls to retain current issue labels/body contracts and handle repeated clicks, API denial and storage failure without reporting completion. Relocate token setup from the removed metadata strip to the inbox toolbar.

Extend tests/test_board.py for concise catch-up rendering in healthy/stale/unknown states, default inbox placement and preserved action URLs. Use existing browser/JS test facilities if present to exercise token errors, success and duplicate clicks. Check the issue workflow remains compatible and render mobile/desktop for layout review. No real queue mutation for testing without explicit authorization.

Current inspection: main checkout has existing bibliography and wiki edits; implementation must use an isolated worktree based on origin/main. Current one-tap code uses localStorage and creates the same issue behind the scenes. GitHub permissions.push check is not proof of Issues write permission.

Tier: undeclared — merge mode: human /prm.
