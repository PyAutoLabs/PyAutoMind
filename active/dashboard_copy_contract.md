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
