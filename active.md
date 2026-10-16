
## decision-matrix-gate-wording
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/421
- issued: 2026-10-16
- prompt: active/decision_matrix_note_gate_wording.md
- status: PR-open 2026-10-16 (Heart RED override → merge via human /prm)
- workspace-pr: https://github.com/PyAutoLabs/autolens_profiling/pull/422
- session: Claude Code CLI (Opus 5.5); session 13efb443
- worktree: ~/Code/PyAutoLabs-wt/decision-matrix-gate-wording
- repos:
  - autolens_profiling: feature/decision-matrix-gate-wording
- classification: docs (autolens_profiling), Consequence notify, Autonomy safe; follow-up F3 of autolens_profiling#419; campaign PyAutoPulse#62
- heart-red-override:
  - date: 2026-10-16
  - authorized-by: live human in session 13efb443, AskUserQuestion answer 'Override, PR-open only (Recommended)'
  - reasons: "PyAutoFit: 1 commit(s) behind origin"; "PyAutoGalaxy: 1 commit(s) behind origin"; "PyAutoLens: 1 commit(s) behind origin"; "release validation incomplete: no rehearsal for current source"
  - passed: check_wiki, build_readme, build_catalogue, build_dashboard, check_results_layout (exit 0); docs-only, no smoke scope
  - permitted: commit, push, PR-open; merge separate

## profiling-lint-634-drift
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/423
- issued: 2026-10-16
- prompt: active/profiling_lint_pyautoarray_634_drift.md
- status: PR-open 2026-10-16 (Heart RED override; human merge command given for this turn)
- workspace-pr: https://github.com/PyAutoLabs/autolens_profiling/pull/424
- session: Claude Code CLI (Opus 5.5); session 13efb443
- worktree: ~/Code/PyAutoLabs-wt/profiling-lint-634-drift
- repos:
  - autolens_profiling: feature/profiling-lint-634-drift
- classification: bug (autolens_profiling), Consequence notify, Autonomy safe; blocks PR #422 (decision-matrix-gate-wording, same session; files disjoint); cause PyAutoArray#634
- heart-red-override:
  - date: 2026-10-16
  - authorized-by: live human in session 13efb443, AskUserQuestion answer 'Override, then merge both (Recommended)'
  - reasons: "PyAutoFit: 1 commit(s) behind origin"; "PyAutoGalaxy: 1 commit(s) behind origin"; "PyAutoLens: 1 commit(s) behind origin"; "release validation incomplete: no rehearsal for current source"
  - passed: pytest scripts/misc/test/ 1457 passed/0 failed; ruff check + format clean
  - permitted: commit, push, PR-open; merge on all-green this turn (#424 then #422)

## search-ext-b5c2a-freeze
- issue: https://github.com/PyAutoLabs/autofit_inference/issues/17
- issued: 2026-10-16
- prompt: active/search_ext_b5c2a_pilot_judge_freeze.md
- status: workspace-dev
- session: Claude Code CLI (Fable 5.1); plan approved in-chat 2026-10-16 (two phases, 2a now; present-and-wait, not --auto); execution delegated to an Opus worker
- worktree: ~/Code/PyAutoLabs-wt/search-ext-b5c2a-freeze
- repos:
  - autofit_inference: feature/search-ext-b5c2a-freeze
  - PyAutoInsight: feature/search-ext-b5c2a-freeze
  - PyAutoCortex: feature/search-ext-b5c2a-freeze
- classification: research (autofit_inference primary; PyAutoCortex ledger, PyAutoInsight task row), Consequence judge, Autonomy supervised; Feature Agent: split-into-phases — 2a judge+calibrate+A2+freeze (no compute), 2b `draft/research/autofit_inference/search_ext_b5c2b_scored_wave_submit.md` (realisations 2–3 + submit)
- suggested-branch: feature/search-ext-b5c2a-freeze
- epic: search-extensibility
- heart-at-door: STALE 2026-10-16 (Release STALE; monitoring RED 28/100) — continue per start_dev 0a; no override needed
