
## direct-conv-symmetric
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/635
- issued: 2026-10-16
- prompt: active/direct_conv_symmetric_row_restriction.md
- status: library-dev — PAUSED 2026-10-16 by the human; uncommitted v2 (+v3 in flight: ymin ordering, gate 0.7, human-approved). Resume from the checkpoint comment https://github.com/PyAutoLabs/PyAutoArray/issues/635#issuecomment-6219325769 ; next = RAL real-data witness (staged /mnt/ral/jnightin/scratch/aris_l2_20261016), ship, then write-up phase (autolens_profiling note + Pulse Knowledge/decision)
- session: Claude Code CLI (Opus 5.5); session 13efb443
- worktree: ~/Code/PyAutoLabs-wt/direct-conv-symmetric (scripts/patches/logs in l2_scratch/, outside git)
- repos:
  - PyAutoArray: feature/direct-conv-symmetric
- classification: feature (PyAutoArray primary; write-up phase autolens_profiling + PyAutoPulse after library), Consequence glance, Autonomy supervised; serial numba only (human: Nautilus-level parallelism); campaign PyAutoPulse#62

## hst-mge-pilot-qualification
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/417
- issued: 2026-10-13
- session: Codex; session ID unavailable
- status: workspace-shipped, awaiting-merge
- workspace-pr: https://github.com/PyAutoLabs/autolens_profiling/pull/418
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/hst-mge-pilot-qualification
- next: Review and merge #418; independently validated witness implementation, coefficient tolerances and production collection remain separate pending work.
- repos:
  - autolens_profiling: feature/hst-mge-pilot-qualification

## custom-runner-relevance
- issue: https://github.com/PyAutoLabs/PyAutoHeart/issues/298
- issued: 2026-10-16
- prompt: active/reusable_smoke_workflow_relevance_gate_skips_custom_runner_tests.md
- status: awaiting-input — draft PR #299; live pipeline witness missing
- workspace-pr: https://github.com/PyAutoLabs/PyAutoHeart/pull/299
- validation: 1252 Heart tests passed; independent code review CLEAN; live witness unresolved
- next: review draft and obtain pipeline unit/slow witness; preserve Heart claim until lifecycle close-out
- session: Codex Work; session ID unavailable
- location: /workspace/scratch/fcfb1c6d3e0b/PyAutoHeart (clone)
- authorization: human approved the four-task smoke-reliability batch with “Go” on 2026-10-16; sequential execution; no release authorization
- repos:
  - PyAutoHeart: feature/custom-runner-relevance

## python-matrix-harness
- issue: https://github.com/PyAutoLabs/PyAutoHands/issues/312
- issued: 2026-10-16
- prompt: active/python_matrix_smoke_bypasses_harness.md
- status: workspace-dev
- session: Codex Work; session ID unavailable
- location: /workspace/scratch/fcfb1c6d3e0b/PyAutoHands (clone)
- authorization: approved four-task batch, “Go” on 2026-10-16; independent step while Heart #298 awaits its witness
- repos:
  - PyAutoHands: feature/python-matrix-harness
