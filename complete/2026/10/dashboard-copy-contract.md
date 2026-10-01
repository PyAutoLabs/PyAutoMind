# Shared dashboard copy-payload regression contract

Completed: 2026-10-01
Issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/437

## Delivered
Added shared `board/copy_contract.py` assertion over rendered HTML copy buttons. It checks data-cmd/data-copy values, decodes HTML entities, rejects leading slash skills independently of a command registry, and rejects fixtures with no copy buttons. Shell snippets, absolute executable paths and explicit terminal chips remain allowed.

Integrated into Brain, Mind, Cortex and Heart HTML renderer tests. No production rendering changes.

## Validation
315 relevant local tests passed; Ruff and whitespace checks passed. Brain CI passed both Python 3.12 and 3.13. Heart initially failed because the checker was not yet on Brain main; after Brain merged, the user-authorized second attempt passed both Python versions. All configured runs/jobs passed before merge. Both branch heads proven ancestors of origin/main.

## PRs
- https://github.com/PyAutoLabs/PyAutoBrain/pull/438 — merge 332aa1c0510265a8156c39fc64501ad8b5966760
- https://github.com/PyAutoLabs/PyAutoHeart/pull/260 — merge 8921ed0b582022cca64acfdcb2c6c8ab31195f47

## Authorization and preservation
Development-only RED override: user "yes I authorie" after Galaxy CI feed reason; direct shipping verdict `release validation FAILED (stage integrate)` also reported. Subsequent prm/try again/merge authorized dependency retry and green merges. No release or check bypass. No irreplaceable data found in the task worktrees; only reproducible Python/test caches. No background monitoring armed.

## Original prompt

# Reject assistant-specific commands in copied dashboard prompts

Type: test
Issued: 2026-10-01
Issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/437
Autonomy: safe

## Original request

ok yeah do that quickly

Approved context: add a shared regression check that rejects assistant-specific slash commands in dashboard copy payloads while allowing real shell commands.

## Plan

@PyAutoBrain @PyAutoHeart: add a shared HTML copy-payload assertion in Brain's board package. Detect leading slash commands in data-cmd/data-copy button values (including HTML entities and leading whitespace), exempt explicit terminal buttons and absolute executable paths. Use it in Brain, Mind, Cortex and Heart rendered-dashboard tests. Cover unknown skill names, malformed/empty pages, and safe shell payloads. No production rendering or publishing change.

User approved development-only Heart RED override with "yes I authorie", after the exact reason `PyAutoGalaxy: CI failure — https://api.github.com/repos/PyAutoLabs/PyAutoGalaxy/actions/runs/24007765443` was surfaced. No merge/release authorization for this new task.
