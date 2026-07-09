# Active Tasks

## weak-modeling
- issue: https://github.com/PyAutoLabs/PyAutoLens/issues/579
- session: claude --resume bf688af1-ea6f-4fcf-b475-ccf3989da853
- status: library-dev
- autonomy: supervised (--auto, launched 2026-07-09, no heart-ack)
- note: keystone of the weak home-straight (blocks series 5/7/8); workspace follow-up deferred — autolens_workspace claimed by lenstool-example; use the proven parallel-worktree pattern (scripts/weak/ zero overlap) if still claimed at workspace time
- worktree: /home/jammy/Code/PyAutoLabs-wt/weak-modeling
- repos:
  - PyAutoLens: feature/weak-modeling


## jwst-nircam-cosmos-web
- issue: https://github.com/PyAutoLabs/PyAutoReduce/issues/6
- session: claude --resume be7cb926-7874-4cc2-8c05-64c9644a64d9
- status: library-dev — implementation complete (75 tests; adapters+dispatch+ERR-noise+PSF lit synthesis); FOUR-BAND INTEGRATION RUNNING OVERNIGHT (scripts/output/overnight_all_bands.log; per-band validation_summary.json); morning: parity table -> review+heart -> park at sign-off (checkpoint comment: issues/6#issuecomment-4919235074)
- autonomy: supervised (--auto, launched 2026-07-08, no heart-ack)
- note: STACKED on feature/wfc3-reduction (PR #5 awaiting merge) — shares adapter/pipeline seams, rebases onto main after #5 merges; 7 local commits unpushed
- worktree: /home/jammy/Code/PyAutoLabs/PyAutoReduce (in-place)
- repos:
  - PyAutoReduce: feature/jwst-nircam

## wfc3-reduction
- issue: https://github.com/PyAutoLabs/PyAutoReduce/issues/4
- session: claude --resume be7cb926-7874-4cc2-8c05-64c9644a64d9
- status: library-shipped, awaiting-merge
- pr: https://github.com/PyAutoLabs/PyAutoReduce/pull/5
- autonomy: supervised (--auto, launched 2026-07-08, no heart-ack)
- note: stacked on feature/hst-acs-phase1 (PR #3 awaiting merge) — same repo, same session, deliberate
- worktree: /home/jammy/Code/PyAutoLabs/PyAutoReduce (in-place)
- repos:
  - PyAutoReduce: feature/wfc3-reduction

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

## morning-status-release-rehearsal
- issue: https://github.com/PyAutoLabs/PyAutoHeart/issues/39
- session: claude --resume ff9a8b2f-fda0-4bab-8962-1814843aa374
- status: awaiting-input — PRs all MERGED 2026-07-08; final leg blocked: PYAUTO_UPDATE_WEBHOOK_URL secret is malformed (curl exit 3; digest has failed daily at the same POST since 2026-05-17 = likely the original email bloat). User must re-set the secret, then re-dispatch morning_health.yml on Mind main
- prs: PyAutoBuild#119 + PyAutoHeart#40 + PyAutoMind#41 (independent; merge Mind last is tidiest — its morning_health reads the others)
- post-merge: dispatch morning_health.yml on Mind main (Slack POST leg); flip vars.RELEASE_MODE=live on PyAutoBuild when satisfied (human)
- autonomy: human-required effective (release cap; --auto launched 2026-07-08, plan approved in-session; ship sign-off + merge human)
- cleanup 2026-07-09: worktree removed + feature branches (local+remote) deleted via /repo_cleanup — all PRs were merged; remaining leg (webhook secret + morning_health.yml dispatch) is human-only and needs no repo claim

## lenstool-example
- issue: https://github.com/PyAutoLabs/autolens_workspace/issues/239
- session: claude --resume fa55f70e-2cea-4887-bf12-61f81cff042f
- status: workspace-shipped, awaiting-merge
- pr: https://github.com/PyAutoLabs/autolens_workspace/pull/240
- note: parity headline 0.068" median source-plane rms vs published 0.32" image-plane rms;
  next step after merge = beta-tester iteration loop
- autonomy: supervised (--auto, launched 2026-07-09; in-session authorization "merge PRs and
  then do 8_lenstool_user_example"; heart-ack carried per prior tasks)
- worktree: /home/jammy/Code/PyAutoLabs-wt/lenstool-example
- repos:
  - autolens_workspace: feature/lenstool-example

## health-sync-noise-filter
- issue: https://github.com/PyAutoLabs/PyAutoHeart/issues/41
- status: library-dev
- note: also carries the /repo_cleanup cadence leg (startup hygiene nudge off ~/.cache/pyauto/repo_cleanup_last_audit.json); Brain-skill stamp write is a follow-up (PyAutoBrain claimed by clone-mitosis-agent)
- worktree: /home/jammy/Code/PyAutoLabs-wt/health-sync-noise-filter
- repos:
  - PyAutoHeart: feature/health-sync-noise-filter
