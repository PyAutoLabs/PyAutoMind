
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

## direct-conv-symmetric
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/635
- issued: 2026-10-16
- prompt: active/direct_conv_symmetric_row_restriction.md
- status: library-dev
- session: Claude Code CLI (Opus 5.5); session 13efb443
- worktree: ~/Code/PyAutoLabs-wt/direct-conv-symmetric
- repos:
  - PyAutoArray: feature/direct-conv-symmetric
- classification: feature (PyAutoArray primary; write-up phase autolens_profiling + PyAutoPulse after library), Consequence glance, Autonomy supervised; serial numba only (human: Nautilus-level parallelism); campaign PyAutoPulse#62
