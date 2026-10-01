# Refresh the public organ table from the body map
Issue: https://github.com/PyAutoLabs/.github/issues/24
Issued: 2026-10-01
Type: docs
Difficulty: small
Autonomy: human-required

## Original request
> check and continue I authorize anything if it needs it

Continuation after the exact proposed diff was presented:
> continue

## Scope
@.github profile/README.md has the only current Heart manifest warning. Regenerate only its marked organ table from PyAutoMind/repos.yaml. PyAutoEyes moves into manifest order and receives the current public_role. Preserve all surrounding prose and every other checkout. No release, deletion, threshold adjustment or unrelated generated changes.

## Plan
1. Confirm claims and isolate the documentation branch from current origin/main.
2. Apply the canonical generator only to the organ table in profile/README.md.
3. Check exact generator equality and whitespace; review the two-row diff.
4. Ship a documentation PR and record validation in Mind.

## Detailed implementation
Target PyAutoLabs/.github, branch feature/heart-front-door-sync. Canonical checkout is clean on feature/pyautoeyes-birth-organ-row; that branch was merged in PR22. Use an isolated worktree. Use repos_sync.organ_public_table with bold=True and replace_block with ORGANS markers, without running the global --write propagation. Validate exact table equality plus git diff --check; no runtime tests are warranted for generated Markdown.

## Approval
The user authorized continued health remediation, reviewed the proposed correction linked in chat, and said continue. This is a normal human-approved task, not --auto.
