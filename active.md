# Active Tasks

## docs-theming-hub
- issue: https://github.com/PyAutoLabs/pyautolabs.github.io/issues/1
- session: claude --resume 3b933eca-2c18-4b0a-9360-b2818f9e4bc6
- status: shipped, awaiting-merge — hub LIVE at pyautolabs.github.io (Pages, main); theming PRs open: Fit#1343 + Galaxy#496 + Lens#598 (pending-release; suites 1424/962/373; review CLEAN; Heart YELLOW = same set as tonight's ack, treated launch-acked, disclosed on PRs); morning checklist on pyautolabs.github.io#1
- autonomy: supervised effective (--auto chain from 2026-07-09 launch; human directed "do everything else you can now then stop for the night" — PRs end at PR-open, batched ack question for morning)
- note: zero-cost (pyautolabs.github.io default domain; RETROFIT.md documents paid-domain flip); shared pyauto.css accents Fit #e0700e / Galaxy #0d9488 / Lens #7c4dff; Fit .gitignore docs/_static must be lifted
- worktree: ~/Code/PyAutoLabs-wt/docs-theming-hub
- repos:
  - PyAutoFit: feature/docs-theming-hub
  - PyAutoGalaxy: feature/docs-theming-hub
  - PyAutoLens: feature/docs-theming-hub

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
- status: code-complete, awaiting-human-legs — all 4 PRs MERGED 2026-07-09 (Heart#48, Galaxy#495, Lens#597, Fit#1342; human-authorized in-session; docs CI live, baselines 105/134/67 held in CI); worktree removed, branches deleted, claims released
- remaining: RTD dashboard legs (human, 2026-07-10): reconnect pyautofit → PyAutoLabs/PyAutoFit (site dead since 2026-05-06), repoint galaxy/lens URLs; verify via addons API, then retire to complete.md
- autonomy: supervised effective (--auto 2026-07-09); Heart YELLOW acked in-session at ship; Fit claim override human-directed ("they don't clash")
- worktree: released
- repos:

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
