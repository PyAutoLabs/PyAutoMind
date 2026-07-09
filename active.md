# Active Tasks

## delaunay-qhull-callback
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/367
- status: library-dev — phase 1: PyAutoArray qhull-only callback + JAX 2-ring point location; phase 2 (autolens_workspace_test parity suite) follows behind the library-first gate
- autonomy: supervised (--auto, launched 2026-07-09; refactor @ too-large, effective min(supervised, safe)=supervised; no heart-ack given)
- note: hard requirement — likelihood numerically unchanged (eager xp=np path is the reference and is untouched); PoC + saved outputs in autolens_profiling/scratch/delaunay_speedup/; do NOT touch fnnls/NNLS (separate follow-up)
- worktree: /home/jammy/Code/PyAutoLabs-wt/delaunay-qhull-callback
- repos:
  - PyAutoArray: feature/delaunay-qhull-callback
  - autolens_workspace_test: feature/delaunay-qhull-callback (phase 2)

## keck-ao-reduction
- issue: https://github.com/PyAutoLabs/PyAutoReduce/issues/11
- status: library-dev — implementing K1–K3 per the #9 design (drizzle backend + B1938+666 anchor user-adopted 2026-07-09)
- autonomy: supervised (--auto, launched 2026-07-09; feature @ large)
- note: carries the #9 write leg (docs/design/keck_ao.md); #9 closes when this merges. Built on post-refactor main 371721f (PR #10 merged human-directed this session)
- worktree: /home/jammy/Code/PyAutoLabs-wt/keck-ao-reduction
- repos:
  - PyAutoReduce: feature/keck-ao-reduction

## keck-ao-reduction-plan
- issue: https://github.com/PyAutoLabs/PyAutoReduce/issues/9
- status: resolved-pending-merge — batched decisions answered in-session 2026-07-09 (drizzle backend, B1938+666 anchor; sequencing resolved by #10 merge); the design-doc deliverable ships on keck-ao-reduction's branch; close #9 when PyAutoReduce#11's PR merges
- question: https://github.com/PyAutoLabs/PyAutoReduce/issues/9#issuecomment-4924402662 (answered)
- autonomy: supervised (--auto, launched 2026-07-09)
- worktree: none (read-only)
- repos:

## refactor-post-phase3
- issue: https://github.com/PyAutoLabs/PyAutoReduce/issues/8
- session: claude --resume be7cb926-7874-4cc2-8c05-64c9644a64d9
- status: MERGED 2026-07-09 (371721f, squash) — human-directed merge in the keck-ao session (user authorized in-conversation); main checkout returned to main; PyAutoReduce claim released. Entry ready to retire to complete.md by its owning session (branch deletion via repo_cleanup)
- pr: https://github.com/PyAutoLabs/PyAutoReduce/pull/10
- notes: witnesses byte-identical both paths; 2 disclosed fix riders (CPDIS fobj, ePSF window +20) caught by baseline capture
- autonomy: default present-and-wait (refactor cap safe; no --auto given)
- worktree: released (was in-place)
- repos:

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
- status: RESOLVED 2026-07-09 (by session 5d58ef6a) — user re-set BOTH May-17 secrets (webhook + CLAUDE_CODE_OAUTH_TOKEN); morning_health dispatched → Slack POST success; digest needed 3 more CI fixes on Mind main (checkout, show_full_output, allowedTools Write; 51e869e/d042289/0b78d5f) → fully green, delivered. Details: issues/39#issuecomment-4924031684. Entry ready to retire to complete.md by its owning session
- prs: PyAutoBuild#119 + PyAutoHeart#40 + PyAutoMind#41 (independent; merge Mind last is tidiest — its morning_health reads the others)
- post-merge: dispatch morning_health.yml on Mind main (Slack POST leg); flip vars.RELEASE_MODE=live on PyAutoBuild when satisfied (human)
- autonomy: human-required effective (release cap; --auto launched 2026-07-08, plan approved in-session; ship sign-off + merge human)
- cleanup 2026-07-09: worktree removed + feature branches (local+remote) deleted via /repo_cleanup — all PRs were merged; remaining leg (webhook secret + morning_health.yml dispatch) is human-only and needs no repo claim

## cluster-likelihood-breakdown
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/57
- session: claude --resume fa55f70e-2cea-4887-bf12-61f81cff042f
- status: workspace-shipped, awaiting-merge
- pr: https://github.com/PyAutoLabs/autolens_profiling/pull/58
- autonomy: supervised (--auto, launched 2026-07-09 "do the next task --auto"; heart-ack carried)
- note: parallel to profiling-preopt-campaign claim on autolens_profiling (active background
  campaign; its diff = likelihood_runtime/sweep.py + scripts/build_baseline.py) — new files in
  likelihood_breakdown/cluster/ are disjoint; re-verify at ship
- worktree: /home/jammy/Code/PyAutoLabs-wt/cluster-likelihood-breakdown
- repos:
  - autolens_profiling: feature/cluster-likelihood-breakdown

## point-pairing-policies
- issue: https://github.com/PyAutoLabs/PyAutoLens/issues/585
- session: claude --resume fa55f70e-2cea-4887-bf12-61f81cff042f
- status: library-shipped, awaiting-merge
- prs: PyAutoLens#586 (library) + autolens_workspace#248 (guide; library-first merge order)
- autonomy: supervised (--auto, "continue --auto" 2026-07-09; heart-ack carried; design defaults
  batched on the issue)
- note: parallel to weak-small-datasets (PyAutoLens; autolens/point/ vs autolens/weak/ disjoint)
  and weak-likelihood-function (autolens_workspace; scripts/guides/ vs scripts/weak/ disjoint);
  re-verify at ship
- worktree: /home/jammy/Code/PyAutoLabs-wt/point-pairing-policies
- repos:
  - PyAutoLens: feature/point-pairing-policies
  - autolens_workspace: feature/point-pairing-policies

## cluster-small-datasets
- issue: https://github.com/PyAutoLabs/autolens_workspace/issues/249
- session: claude --resume fa55f70e-2cea-4887-bf12-61f81cff042f
- status: workspace-shipped, awaiting-merge
- prs: autolens_workspace#250 + PyAutoBuild#123 (merge together)
- autonomy: supervised (--auto, "continue --auto" 2026-07-09; heart-ack carried)
- note: parallel to weak-strong-lensing + frozen point-pairing-policies claims on
  autolens_workspace (scripts/cluster/ disjoint); navigator-catalogue regen rebase needed by
  whichever open branch merges last; PyAutoBuild unclaimed
- worktree: /home/jammy/Code/PyAutoLabs-wt/cluster-small-datasets
- repos:
  - autolens_workspace: feature/cluster-small-datasets
  - PyAutoBuild: feature/cluster-small-datasets

## csv-api-lenstool
- issue: https://github.com/PyAutoLabs/PyAutoGalaxy/issues/490
- session: claude --resume fa55f70e-2cea-4887-bf12-61f81cff042f
- status: library-dev — stress-test phase
- autonomy: supervised (--auto, in-session directive 2026-07-09; heart-ack carried)
- note: parallel claims as per cluster-small-datasets entry (scripts/cluster/ disjoint);
  PyAutoGalaxy unclaimed post-merges
- worktree: /home/jammy/Code/PyAutoLabs-wt/csv-api-lenstool
- repos:
  - PyAutoGalaxy: feature/csv-api-lenstool
  - autolens_workspace: feature/csv-api-lenstool
