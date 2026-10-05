# Remove remaining dashboard-owned introductory prose

Type: feature
Target: PyAutoHands
Repos:
- PyAutoHands
- PyAutoEyes
- PyAutoInsight
Consequence: judge
Difficulty: small
Autonomy: supervised
Issued: 2026-10-05
Issue: https://github.com/PyAutoLabs/PyAutoHands/issues/300

## Plan
Continuation of the approved dashboard-minimal-text work: remove custom dashboard-purpose/usage prose missed by shared hero changes. A live scan covered all 13 boards; seven older dashboards were refreshed to consume the merged theme. Quoted Heart/Hands/Nerves introductions are now absent live. Remaining custom copy: Eyes lede; Hands explanation of its relationship to Heart; Insight check-in tutorial and campaign/ledger explanations. Keep links, concise headings, real observations and exact prompts. No workflow or data changes.

Files: autohands/board.py; eyes/board.py; insight/campaigns.py. Remove static HTML and equivalent Markdown introductions; preserve GitHub/ledger/Heart links with concise labels. Run existing full suites, required lint/format/offline checks and render output. Human /prm; source changes in isolated feature/dashboard-prose-followup worktrees. Parent initiative: draft/feature/pyautobrain/standardize_dashboard_orchestration_prompt_panel.md.

## Original user request
On Heart, the text "Is it safe to release? See what needs attention, then copy a prompt to work through it in your coding chat."
is unecessarily, another example of somehtin gI already know. Remove it. Scan this problem for all dashboards
Hands has same issue "What the Hands shipped — a record of execution, newest first. Tap 📋 to put a command on your clipboard for an AI assistant chat."
same for Nerves "Every config file and option across the libraries and the workspaces that override them — read-only." someone using a dashboard knows what it does.
