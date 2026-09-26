- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/418 (closed)
- completed: 2026-09-26
- library-pr: https://github.com/PyAutoLabs/PyAutoMind/pull/440, https://github.com/PyAutoLabs/PyAutoCortex/pull/45, https://github.com/PyAutoLabs/PyAutoBrain/pull/420 (all MERGED, in that order)
- epic: organ-cockpit (contract PyAutoBrain#416; siblings Hands#289, Memory#104)
- heart-red-override: "Heart RED `release validation FAILED (stage integrate)`; live human 'override and continue' 2026-09-26 — development shipping + merge on green checks; recorded on the issue, all three PR bodies, active.md, autonomy_log.md"
- witness: both dashboard_refresh.yml self-heals committed state.json to main and dispatched Pages; both pages_dashboard.yml runs green with `state: ok`; https://pyautolabs.github.io/PyAutoMind/state.json (yellow | 24 picks · 6 in flight | 20 items) and /PyAutoCortex/state.json (yellow | 7 active · 7 running | 8 items) validate.
- gotchas: Mind/Cortex dashboards are rendered by Brain conductors, so the emit lives in the Brain and the two repos only admit/copy/validate the file — merge order Mind → Cortex → Brain with every workflow step guarded `[ -f state.json ]`; the intake `_mind_home` regex had been broken since the grouped-checkouts layout (repos.yaml `path:` precedes `github:`), leaving the live Mind dashboard without its Pages pointer / absolute links — fixed in #420, self-heal committed a large dashboard.html link diff; `--check` covers state.json with `updated` normalised out (`_state_body`/`page_body`); the Cortex feed carries a 3 h check-in staleness rule so its `--check` drifts once a check-in ages (nightly heal re-commits; PRs touching projects/** >3 h after a render need a re-render); canonical PyAutoCortex sat on claude/checkin-2026-09-19 (dirty, unpushed science check-in) and was left untouched; env-only test failures when activate.sh exports PYAUTO_MIND/PYAUTO_ROOT (Brain test_grouped_organ_consumers, Mind test_repos_sync_root_default).
- follow-ups (not filed): Eyes/Gut/Nerves feeds (no board yet); PWA cockpit page; start_dev Heart-RED gate; tray dot; status line; consider making Cortex check-in staleness idempotent for --check.
- summary: Mind and Cortex dashboards emit the organ-cockpit state.json v1 feed via the Brain intake + cortex conductors (`render_state`, check/apply/checkin), with the Mind/Cortex spawn + ledger-merge guards and Pages workflows admitting, staging, copying and validating the file. Brain 196 targeted / 1037 full, Mind 586, Cortex 64.

## Original prompt

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
Issued: 2026-09-26
Issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/418
Filed: 2026-09-26
Epic: organ-cockpit

Phase 1 (PyAutoBrain#416, shipped 2026-09-26) defined the per-organ state.json v1 cockpit feed (board/state_schema.json, board/_state.py). The Mind task dashboard and the Cortex science dashboard are not rendered in their own repos: PyAutoBrain's intake conductor writes PyAutoMind/dashboard.md + dashboard.html (pyauto-brain intake --apply dashboard) and the cortex conductor writes PyAutoCortex's dashboard, and each repo's pages_dashboard.yml only copies dashboard.html into _site. So the emit lives in the Brain renderers and the publish/validate lives in the two workflows.

1. PyAutoBrain intake dashboard renderer: --apply also writes PyAutoMind/state.json (organ mind, repo PyAutoMind, status from the dashboard's own headline logic — red if any task is blocked/awaiting-input, yellow if picks are waiting, green otherwise; headline = the picks/in-flight count line; items = in-flight tasks awaiting a human (awaiting-merge, awaiting-input, human review) each with its issue/PR link and the existing /start_dev or /prm copy payload as prompt). Validate through board/_state.validate_state before writing. The dashboard --check must also compare state.json.
2. PyAutoBrain cortex conductor: the same for PyAutoCortex/state.json (organ cortex: red if any project ledger reports a failed run, yellow if runs are pending pull/checkin, green otherwise; items = projects needing the human with links).
3. PyAutoMind and PyAutoCortex pages_dashboard.yml: cp state.json _site/state.json and a validate step; both jobs must check out PyAutoBrain (like knowledge_board.yml does) to run python3 PyAutoBrain/board/_state.py _site/state.json. dashboard_refresh.yml self-heal must regenerate state.json with the html.
4. Brain tests: both renderers produce a feed that validates on the hermetic dashboard fixtures; Mind/Cortex commit guards accept the new tracked file.

Witness: pyauto-brain intake dashboard --check reports current with state.json tracked in PyAutoMind; both pages_dashboard.yml runs green with 'state: ok'; curl https://pyautolabs.github.io/PyAutoMind/state.json and /PyAutoCortex/state.json pass the validator.

<!-- formalised by the Intake (Conception) Agent on 2026-09-26 from user-intake -->
