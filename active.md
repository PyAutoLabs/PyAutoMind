
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

## grouped-smoke-install
- issue: https://github.com/PyAutoLabs/PyAutoHeart/issues/300
- issued: 2026-10-16
- prompt: active/smoke_install_flat_pip_chain_breaks_local_env_creation.md
- status: workspace-shipped, awaiting-ci
- workspace-pr: https://github.com/PyAutoLabs/PyAutoHeart/pull/301
- head: 4899eb992e0d5b32c29cb18a5ee8e65b61852ab9
- validation: 1257 tests passed; independent review CLEAN; fresh grouped AutoLens prepare-only exited 0 and passed preflight; existing flat CI both legs passed for fit/galaxy/lens and October8 CTI baseline
- next: CI run38969404218 pending (3.12 passed, 3.13 running); tier judge: human /prm when green
- session: Codex Work
- location: /workspace/scratch/fcfb1c6d3e0b/heart-grouped
- authorization: approved four-task batch; human resumed remaining tasks 2026-10-16
- heart: STALE — Release STALE; monitoring RED; snapshot 11h old
- repos:
  - PyAutoHeart: feature/grouped-smoke-install

## smoke-sampler-imports
- issue: https://github.com/PyAutoLabs/PyAutoHands/issues/313
- issued: 2026-10-16
- prompt: active/smoke_profile_cannot_see_a_missing_sampler.md
- status: workspace-shipped, awaiting-ci
- workspace-pr: https://github.com/PyAutoLabs/PyAutoHands/pull/316
- head: bfb48879e627d44d93b1b0c45d66a47023108f61
- validation: targeted20passed; independent review CLEAN after corner API fix; actual HowToFit tutorial6 failed0.3s without blackjax and passed14.8s after installation; full suite501passed9skipped1known baseline reaping failure; tenant firewall OK
- next: CI run38969557427 all3legs pending; tier notify permits merge on green, no waiter
- session: Codex Work
- location: /workspace/scratch/fcfb1c6d3e0b/hands-sampler
- authorization: approved four-task batch; human resumed remaining tasks 2026-10-16
- heart: STALE — Release STALE; monitoring RED; snapshot 11h old
- repos:
  - PyAutoHands: feature/smoke-sampler-imports
