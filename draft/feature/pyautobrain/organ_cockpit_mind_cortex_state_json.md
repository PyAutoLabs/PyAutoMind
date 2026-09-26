# Organ cockpit: Mind and Cortex dashboards emit state.json via their Brain renderers

Type: feature
Target: PyAutoBrain
Repos:
- PyAutoBrain
- PyAutoMind
- PyAutoCortex
Difficulty: medium
Autonomy: safe
Priority: high
Status: formalised
Consequence: notify
Witness: pyauto-brain intake dashboard --check reports current with state.json tracked in PyAutoMind; both pages_dashboard.yml runs green with 'state: ok'; curl https://pyautolabs.github.io/PyAutoMind/state.json and /PyAutoCortex/state.json pass the validator.
Review-minutes: 0
Unattended: ready
Epic: organ-cockpit

Phase 1 (PyAutoBrain#416, shipped 2026-09-26) defined the per-organ state.json v1 cockpit feed (board/state_schema.json, board/_state.py). The Mind task dashboard and the Cortex science dashboard are not rendered in their own repos: PyAutoBrain's intake conductor writes PyAutoMind/dashboard.md + dashboard.html (pyauto-brain intake --apply dashboard) and the cortex conductor writes PyAutoCortex's dashboard, and each repo's pages_dashboard.yml only copies dashboard.html into _site. So the emit lives in the Brain renderers and the publish/validate lives in the two workflows.

1. PyAutoBrain intake dashboard renderer: --apply also writes PyAutoMind/state.json (organ mind, repo PyAutoMind, status from the dashboard's own headline logic — red if any task is blocked/awaiting-input, yellow if picks are waiting, green otherwise; headline = the picks/in-flight count line; items = in-flight tasks awaiting a human (awaiting-merge, awaiting-input, human review) each with its issue/PR link and the existing /start_dev or /prm copy payload as prompt). Validate through board/_state.validate_state before writing. The dashboard --check must also compare state.json.
2. PyAutoBrain cortex conductor: the same for PyAutoCortex/state.json (organ cortex: red if any project ledger reports a failed run, yellow if runs are pending pull/checkin, green otherwise; items = projects needing the human with links).
3. PyAutoMind and PyAutoCortex pages_dashboard.yml: cp state.json _site/state.json and a validate step; both jobs must check out PyAutoBrain (like knowledge_board.yml does) to run python3 PyAutoBrain/board/_state.py _site/state.json. dashboard_refresh.yml self-heal must regenerate state.json with the html.
4. Brain tests: both renderers produce a feed that validates on the hermetic dashboard fixtures; Mind/Cortex commit guards accept the new tracked file.

Witness: pyauto-brain intake dashboard --check reports current with state.json tracked in PyAutoMind; both pages_dashboard.yml runs green with 'state: ok'; curl https://pyautolabs.github.io/PyAutoMind/state.json and /PyAutoCortex/state.json pass the validator.

<!-- formalised by the Intake (Conception) Agent on 2026-09-26 from user-intake -->
