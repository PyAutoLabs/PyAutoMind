# Active Tasks

## version-check-compat-floor
- issue: https://github.com/PyAutoLabs/PyAutoConf/issues/118
- session: claude --resume 5d58ef6a-dde4-4f02-be05-0c80c0be0302
- status: library-dev
- autonomy: supervised (--auto, launched 2026-07-08, no heart-ack)
- note: R2 of PyAutoBuild#118 design review; R3 (PyAutoBuild refactor) follows once this nears shipping
- worktree: /home/jammy/Code/PyAutoLabs-wt/version-check-compat-floor
- repos:
  - PyAutoConf: feature/version-check-compat-floor

## wfc3-reduction
- issue: https://github.com/PyAutoLabs/PyAutoReduce/issues/4
- session: claude --resume be7cb926-7874-4cc2-8c05-64c9644a64d9
- status: library-dev
- autonomy: supervised (--auto, launched 2026-07-08, no heart-ack)
- note: stacked on feature/hst-acs-phase1 (PR #3 awaiting merge) — same repo, same session, deliberate
- worktree: /home/jammy/Code/PyAutoLabs/PyAutoReduce (in-place)
- repos:
  - PyAutoReduce: feature/wfc3-reduction

## version-pinning-design-review
- issue: https://github.com/PyAutoLabs/PyAutoBuild/issues/118
- session: claude --resume 5d58ef6a-dde4-4f02-be05-0c80c0be0302
- status: follow-ups-in-flight — hold lifted 2026-07-08 (PyAutoHeart#39 shipped: rehearsal crons live, R4 done bar run_number residue); R2 → version-check-compat-floor (PyAutoConf#118); R3 files when R2 nears shipping; R1 PyPI-side = batched question to maintainer on the issue
- decision: https://github.com/PyAutoLabs/PyAutoBuild/issues/118#issuecomment-4918433908
- autonomy: supervised (--auto, launched 2026-07-08, no heart-ack)
- worktree: none (read-only research)
- repos:

## kxs-core
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/362
- session: claude --resume 4bcb5c3c-c067-4955-8bcd-8a7d93128ca7
- status: library-shipped, awaiting-merge + phase-4 fork
- prs: PyAutoArray#363 -> PyAutoGalaxy#486 -> autolens_workspace#236
- question: simulator-adoption fork (a/b/c) on the issue; phase 3 blocked by dpie-lenstool-param (autolens_workspace_test)
- autonomy: supervised (--auto, launched 2026-07-08, no heart-ack)
- worktree: /home/jammy/Code/PyAutoLabs-wt/kxs-core
- repos:
  - PyAutoArray: feature/kxs-core
  - PyAutoGalaxy: feature/kxs-core
  - autolens_workspace: feature/kxs-core

## hst-acs-phase1
- issue: https://github.com/PyAutoLabs/PyAutoReduce/issues/2
- session: claude --resume be7cb926-7874-4cc2-8c05-64c9644a64d9
- status: library-shipped, awaiting-merge
- pr: https://github.com/PyAutoLabs/PyAutoReduce/pull/3
- autonomy: supervised (--auto, launched 2026-07-08; heart YELLOW reason set acked by maintainer at sign-off)
- worktree: /home/jammy/Code/PyAutoLabs/PyAutoReduce (in-place — single new repo, no parallel claims)
- repos:
  - PyAutoReduce: feature/hst-acs-phase1

## ep-analytic-updates-scope
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1337
- session: claude --resume 3589268b-e5c9-4b32-b655-d07f732ea300
- status: complete-pending-pickup — phase 6 done; implementation plan for all 4 WPs on #1338 (plan-only, human-directed no-implement); backlog anchor feature/autofit/ep_analytic_updates.md
- plan: https://github.com/PyAutoLabs/PyAutoFit/issues/1338
- autonomy: supervised (--auto, launched 2026-07-08)
- worktree: none (read-only)
- repos:

## ep-deterministic-reconcile
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1336
- session: claude --resume 3589268b-e5c9-4b32-b655-d07f732ea300
- status: awaiting-input — phase 5 complete; recommendation A (keep both, document trade-off, resurrect #1153 test) on #1336 pending decision
- question: https://github.com/PyAutoLabs/PyAutoFit/issues/1336#issuecomment-4917522033
- autonomy: supervised (--auto, launched 2026-07-08)
- worktree: none (read-only)
- repos:

## ep-diagnostics
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1335
- session: claude --resume 3589268b-e5c9-4b32-b655-d07f732ea300
- status: awaiting-input — implementation complete (diagnostics module + wiring + F3 fix; full suite 1429 pass/14 skip; uncommitted); parked at ship sign-off incl. Heart YELLOW ack
- question: https://github.com/PyAutoLabs/PyAutoFit/issues/1335#issuecomment-4917484045
- autonomy: supervised (--auto, launched 2026-07-08, no heart-ack yet)
- note: parallel to ep-graphical-docs claim on PyAutoFit (PR #1334, docs-only) — disjointness re-verified at sign-off: zero file overlap
- worktree: /home/jammy/Code/PyAutoLabs-wt/ep-diagnostics
- repos:
  - PyAutoFit: feature/ep-diagnostics

## ep-examples-tests
- issue: https://github.com/PyAutoLabs/autofit_workspace/issues/81
- session: claude --resume 3589268b-e5c9-4b32-b655-d07f732ea300
- status: awaiting-input — implementation complete + validated (tutorial converges 49.96±0.12; 3 integration scripts PASS; uncommitted); parked at ship sign-off incl. Heart YELLOW ack
- question: https://github.com/PyAutoLabs/autofit_workspace/issues/81#issuecomment-4917307451
- autonomy: supervised (--auto, launched 2026-07-08, plan approved in-session, no heart-ack yet)
- worktree: /home/jammy/Code/PyAutoLabs-wt/ep-examples-tests
- repos:
  - autofit_workspace: feature/ep-examples-tests
  - autofit_workspace_test: feature/ep-examples-tests

## ep-graphical-docs
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1333
- session: claude --resume 3589268b-e5c9-4b32-b655-d07f732ea300
- status: library-shipped, awaiting-merge (extended 2026-07-08: seam contract — README §8 lowering table, AGENTS.md seam rule, 4 seam tests replacing the dead #1153 test; suite 1425 pass)
- pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1334
- autonomy: supervised (--auto, launched 2026-07-08; heart YELLOW acked in-session at ship)
- worktree: /home/jammy/Code/PyAutoLabs-wt/ep-graphical-docs
- repos:
  - PyAutoFit: feature/ep-graphical-docs

## ep-priors-fable-reassess
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1330
- session: claude --resume 3589268b-e5c9-4b32-b655-d07f732ea300
- status: awaiting-input — phase 0 complete; decision hub PyAutoFit#1331 open for maintainer/contributor guidance (fix-batch + 5 decisions)
- question: https://github.com/PyAutoLabs/PyAutoFit/issues/1331
- worktree: none (read-only reassessment on PyAutoFit main @ 0f26ff2d8; verdicts land in PyAutoMind bug/priors)
- repos:

## ep-statistics-audit
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1332
- session: claude --resume 3589268b-e5c9-4b32-b655-d07f732ea300
- status: phase-1-complete — F1–F9 verdict table on #1332; EP wiki page shipped (PyAutoMemory methods_wiki); EP fix batch (F1+F2+F3+F4+F8) pends #1331 guidance; Phase 2 (docs) ready to start
- worktree: none (read-only audit on PyAutoFit main; findings land in PyAutoMind + issue #1332)
- repos:










## profiling-preopt-campaign
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/56
- status: workspace-dev
- autonomy: supervised (--auto, launched 2026-07-08; local-CPU leg, RAL down)
- campaign: local-CPU matrix in flight (background); interruption-safe — resume with
  sweep.py --skip-gpu --skip-existing (dense, then --sparse imaging pass), then
  aggregate.py; full cold-resume steps on the issue (comment of 2026-07-08 evening)
- worktree: /home/jammy/Code/PyAutoLabs-wt/profiling-preopt-campaign
- repos:
  - autolens_profiling: feature/profiling-preopt-campaign

## clone-mitosis-agent
- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/57
- status: awaiting-input (design complete; parked at ship sign-off)
- question: https://github.com/PyAutoLabs/PyAutoBrain/issues/57 (sign-off comment)
- autonomy: supervised (--auto, launched 2026-07-08)
- worktree: /home/jammy/Code/PyAutoLabs/PyAutoBrain (in-place)
- repos:
  - PyAutoBrain: feature/clone-mitosis-agent

## dpie-lenstool-param
- issue: https://github.com/PyAutoLabs/PyAutoGalaxy/issues/485
- session: claude --resume fa55f70e-2cea-4887-bf12-61f81cff042f
- status: awaiting-input — implementation complete + validated (from_lenstool constructors,
  analytic pi05 potential replacing 15%-wrong MGE, _ellip min-clamp; PyAutoGalaxy 952 pass,
  downstream PyAutoLens 336 pass, parity script 6/6; uncommitted); parked at ship sign-off
  incl. Heart YELLOW ack
- question: https://github.com/PyAutoLabs/PyAutoGalaxy/issues/485 (sign-off comment)
- autonomy: supervised (--auto, launched 2026-07-08, no heart-ack)
- note: psf-oversample-refactor's PyAutoGalaxy PR #484 observed merged at worktree creation
  (HEAD 6fd900a4) — the parallel-claim concern resolved itself; its active.md entry is stale
- worktree: /home/jammy/Code/PyAutoLabs-wt/dpie-lenstool-param
- repos:
  - PyAutoGalaxy: feature/dpie-lenstool-param
  - autolens_workspace_test: feature/dpie-lenstool-param

## morning-status-release-rehearsal
- issue: https://github.com/PyAutoLabs/PyAutoHeart/issues/39
- session: claude --resume ff9a8b2f-fda0-4bab-8962-1814843aa374
- status: awaiting-input — PRs all MERGED 2026-07-08; final leg blocked: PYAUTO_UPDATE_WEBHOOK_URL secret is malformed (curl exit 3; digest has failed daily at the same POST since 2026-05-17 = likely the original email bloat). User must re-set the secret, then re-dispatch morning_health.yml on Mind main
- prs: PyAutoBuild#119 + PyAutoHeart#40 + PyAutoMind#41 (independent; merge Mind last is tidiest — its morning_health reads the others)
- post-merge: dispatch morning_health.yml on Mind main (Slack POST leg); flip vars.RELEASE_MODE=live on PyAutoBuild when satisfied (human)
- autonomy: human-required effective (release cap; --auto launched 2026-07-08, plan approved in-session; ship sign-off + merge human)
- worktree: /home/jammy/Code/PyAutoLabs-wt/morning-status-release-rehearsal
- repos:
  - PyAutoHeart: feature/morning-status-release-rehearsal
  - PyAutoBuild: feature/morning-status-release-rehearsal
  - PyAutoMind: feature/morning-status-release-rehearsal
