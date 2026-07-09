# Active Tasks

## assistant-ref-mechanics
- issue: https://github.com/PyAutoLabs/autolens_assistant/issues/43
- session: claude --resume 4bf88e6b-682d-4590-906f-77b68d059b26
- status: library-shipped, awaiting-merge — 4-leg gate passed (tests 39 + audits / smoke n/a / review CLEAN / heart YELLOW⊆ack); run ended at PR-open per contract
- pr: https://github.com/PyAutoLabs/autolens_assistant/pull/44
- autonomy: safe effective (--auto launched 2026-07-09 post frame-products merge; header safe, feature/small cap safe; plan on the issue per contract)
- heart-ack: workspace validation not passing (3 failed, 2026-07-09T09-48-30Z); 58 stale parked script(s); autolens_assistant pinned BEHIND installed; PyAutoMind open PR 10d old; install verification not run; no release validation for current source — acked in-session 2026-07-09 (frame-products ship stretch); binds to exactly this set, any new reason parks
- note: prompt audit at start_dev: resolution order/env var/assistant_ref already shipped in skills/start-new-project.md — task narrowed to the mismatch-warning mechanics + generated-AGENTS.md mirror; Brain pick 1 (point_source_light) queued on rtd-hygiene's PyAutoGalaxy claim
- worktree: none (autolens_assistant develops in-place; branch feature/assistant-ref-mechanics)
- repos:
  - autolens_assistant: feature/assistant-ref-mechanics

## rtd-hygiene
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1341
- session: claude --resume 3b933eca-2c18-4b0a-9360-b2818f9e4bc6
- status: merging — Heart#48 + Galaxy#495 + Lens#597 MERGED 2026-07-09 (human-authorized in-session; Galaxy/Lens docs checks passed in CI, baselines 105/134 held); PyAutoFit leg unblocked by human claim override ("they don't clash", disjointness verified vs both EP diffs) → PR#1342 open, checks running, merge on green authorized; RTD dashboard human legs still open (user walked through, awaiting confirmation)
- prs: https://github.com/PyAutoLabs/PyAutoHeart/pull/48 + https://github.com/PyAutoLabs/PyAutoGalaxy/pull/495 + https://github.com/PyAutoLabs/PyAutoLens/pull/597
- ship-note: after Heart#48 merges re-trigger Galaxy/Lens docs checks; if CI warning count differs from local baselines (105/134) recalibrate docs/sphinx_warning_baseline.txt once with justification; scope riders disclosed on issue
- autonomy: supervised effective (--auto launched 2026-07-09; docs/medium caps safe, header supervised binds; plan human-approved in-session pre-launch; no heart-ack given)
- note: phase A of docs middle path; phases B+C parked in docs/libraries/docs_theming_and_hub.md (do NOT issue until this ships); RTD-dashboard human legs (reconnect pyautofit RTD → PyAutoLabs, repoint galaxy/lens URLs) are claim-independent and can run any time
- worktree: ~/Code/PyAutoLabs-wt/rtd-hygiene
- repos:
  - PyAutoFit: feature/rtd-hygiene

## slacs1430-acs-parity
- issue: https://github.com/PyAutoLabs/PyAutoReduce/issues/17
- session: claude --resume cc79d958-a1aa-45cb-b088-bd6cae94aa86
- status: workspace-dev — phases 0-2 done (pixel parity: data ratio 1.04; legacy noise lacks R=1.364; legacy frame is rot270 of north-up; acquire duplicate-exposure bug filed bug/pyautoreduce/); phase 3: both Nautilus parity fits sampling in background (resume: prototypes/slacs1430_parity_fit.py legacy|autoreduce, Nautilus auto-resumes)
- autonomy: safe effective (--auto launched 2026-07-09; plan human-approved in-session pre-launch; no heart-ack given)
- note: keck-ao pattern — analysis on PyAutoReduce main, NO worktree claim (frame-products holds it); outputs gitignored scripts/output/; script commit + PR gated until claim releases; autolens_assistant is driver-only (public template, no commits, scratch only)
- worktree: none (analysis on PyAutoReduce main; branch feature/slacs1430-acs-parity only at ship)
- repos:

## keck-ao-acceptance-checks
- issue: https://github.com/PyAutoLabs/PyAutoReduce/issues/13
- status: parked-resumable (laptop reset) — check 3 done: plate-scale finding (adapter 9.942 wrong; 9.952 pre-2015/9.971 post; fix gated); check 4 fit CHECKPOINTED ~1h in (94MB checkpoint.hdf5); resume command on the issue's interim comment
- resume: re-run prototypes/b1938_lens_fit.py (Nautilus auto-resumes from output/b1938_keck_acceptance identity path); then report θ_E vs 0.45" on #13; then propose keck_ao.md parity appendix + epoch-aware native_scale adapter fix (present-and-wait)
- autonomy: default present-and-wait (no --auto); analysis read-only in prototypes/, doc/adapter edits gated on user review
- worktree: none (analysis on PyAutoReduce main; branch only if an edit is approved)
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

## morning-status-release-rehearsal
- issue: https://github.com/PyAutoLabs/PyAutoHeart/issues/39
- session: claude --resume ff9a8b2f-fda0-4bab-8962-1814843aa374
- status: RESOLVED 2026-07-09 (by session 5d58ef6a) — user re-set BOTH May-17 secrets (webhook + CLAUDE_CODE_OAUTH_TOKEN); morning_health dispatched → Slack POST success; digest needed 3 more CI fixes on Mind main (checkout, show_full_output, allowedTools Write; 51e869e/d042289/0b78d5f) → fully green, delivered. Details: issues/39#issuecomment-4924031684. Entry ready to retire to complete.md by its owning session
- prs: PyAutoBuild#119 + PyAutoHeart#40 + PyAutoMind#41 (independent; merge Mind last is tidiest — its morning_health reads the others)
- post-merge: dispatch morning_health.yml on Mind main (Slack POST leg); flip vars.RELEASE_MODE=live on PyAutoBuild when satisfied (human)
- autonomy: human-required effective (release cap; --auto launched 2026-07-08, plan approved in-session; ship sign-off + merge human)
- cleanup 2026-07-09: worktree removed + feature branches (local+remote) deleted via /repo_cleanup — all PRs were merged; remaining leg (webhook secret + morning_health.yml dispatch) is human-only and needs no repo claim

## nnls-solver-optimization
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/369
- session: claude --resume a67dda1e-835b-43c6-b90f-a2190e349ad0
- status: info-shipped, implementation PARKED (user decision 2026-07-09) — findings + ledger on the issue; validated knob implementation preserved on pushed branch feature/nnls-solver-optimization (d8a1c84a), NOT for merge
- worktree: ~/Code/PyAutoLabs-wt/nnls-solver-optimization
- repos:
  - PyAutoArray: feature/nnls-solver-optimization
- note: awaiting A100 addendum only — RAL job 330046 queued (euclid-ral-gpu-[1-2] down); when it runs, rsync scratch/nnls_speedup results back, post addendum to #369, then offer issue closure + worktree cleanup. Scratch harness + real systems in autolens_profiling/scratch/nnls_speedup/ (canonical checkout, untracked) are the shared testbed for the BPP/ADMM follow-up

## nnls-bpp-admm-experiment
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/370
- session: claude --resume a67dda1e-835b-43c6-b90f-a2190e349ad0
- status: workspace-dev (scratch prototyping)
- worktree: (none — untracked scratch/nnls_speedup in canonical autolens_profiling; no repo claims)
- repos:
- note: BPP phase 1 first, then ADMM, then gate decision; promotion into PyAutoArray needs fresh plan+approval and is blocked-by nnls-solver-optimization's parked PyAutoArray claim until that resolves; baselines + testbed shared with #369
