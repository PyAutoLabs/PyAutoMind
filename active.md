# Active Tasks

## frame-registration
- issue: https://github.com/PyAutoLabs/PyAutoReduce/issues/19
- session: claude --resume 4bf88e6b-682d-4590-906f-77b68d059b26
- status: library-dev — assessment DONE (relative registration 0.05-0.12 px empirical, FIT_REL_GSC242 group solution; findings on issue); implementing manifest registration block
- autonomy: supervised effective (--auto chain 2026-07-09/10); recommendation (fixed-vs-free shifts) + ship sign-off park as one batched question
- heart-ack: same 6-reason set as prior entries this chain; any new reason parks
- note: PSF follow-up queued as feature/pyautoreduce/per_frame_psf.md (user: "Then do the PSF work"); slacs1430 phase-4 ship also wants PyAutoReduce — this task ships small and releases fast; disjoint files (package/frames.py+docs vs scripts/+prototypes/)
- worktree: ~/Code/PyAutoLabs-wt/frame-registration
- repos:
  - PyAutoReduce: feature/frame-registration

## rectangular-kernel-cdf-mesh
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/373
- status: library-dev — kernel-density CDF transform (Enzi RTU) as opt-in mesh variant RectangularKernelAdapt{Density,Image}; success = strict FD on ALL params in jax_grad scripts (imaging os_pix=1+4, interferometer sparse) + eager-vs-JIT + FoM parity; sampler work OUT of scope; stash@{0} inspection preamble (retire parked.md rectangular-spline-cdf)
- autonomy: supervised (prompt header; no --auto — present-and-wait at ship gates)
- claim-override: human-directed 2026-07-10 — proceeds alongside rect-adapt's PyAutoArray claim ("distinct hunks, they don't clash"); coordinate merge order at ship
- note: same-file adjacency with parked rect-adapt wt (#372, uncommitted, edges_transformed hunk only) — distinct hunks in mesh_geometry/rectangular.py, clean merge either order; workspace leg (autolens_workspace_test jax_grad + autolens_workspace_developer README row) follows library PR
- worktree: ~/Code/PyAutoLabs-wt/rectangular-kernel-cdf-mesh
- repos:
  - PyAutoArray: feature/rectangular-kernel-cdf-mesh

## pyautoscientist-phase1
- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/65
- status: library-dev — Phase 1 only (licences MIT [Memory = MIT structure + CC-BY 4.0 content, human-decided], 5 organ README rewrites ~20-40 lines, Build to_do_list evacuation+gitignore, repos_sync check_tenant_firewall); phases 2/3 anchored by issued/pyautoscientist_generalisation.md
- autonomy: supervised (no --auto; present-and-wait at every checkpoint; one PR per repo, 5 PRs)
- note: Mind README is agent-load-bearing → schemas relocate verbatim to REFERENCE.md, agent pointers untouched; acceptance = zero diffs to skill bodies/AGENTS.md/hooks/runtime code except additive firewall check + Build gitignore; test_results/ already untracked (assessment claim stale)
- worktree: ~/Code/PyAutoLabs-wt/pyautoscientist-phase1
- repos:
  - PyAutoBrain: feature/pyautoscientist-phase1
  - PyAutoMind: feature/pyautoscientist-phase1
  - PyAutoHeart: feature/pyautoscientist-phase1
  - PyAutoMemory: feature/pyautoscientist-phase1
  - PyAutoBuild: feature/pyautoscientist-phase1

## psf-convolution-docstring
- issue: https://github.com/PyAutoLabs/autolens_workspace/issues/257
- status: workspace-dev — normalize __PSF Convolution__ section across 41 simulator.py (3 full-section reference files + 38 input-only) in autolens_workspace + autogalaxy_workspace
- autonomy: supervised (user said "go, all in one" — both workspaces this session)
- note: Tier A = imaging/simulator.py (both) + autolens group/simulator.py (full __PSF Convolution__ header+Contents+prose); Tier B = convolve_over_sample_size=1 on from_gaussian; 10 autogalaxy CRLF files edited CRLF-safe; interferometer/point-multiple/weak-base out of scope
- worktree: ~/Code/PyAutoLabs-wt/psf-convolution-docstring
- repos:
  - autolens_workspace: feature/psf-convolution-docstring
  - autogalaxy_workspace: feature/psf-convolution-docstring

## rect-adapt
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/372
- session: claude --resume 4bf88e6b-682d-4590-906f-77b68d059b26
- status: awaiting-input — implementation complete + full suite 877 pass (uncommitted in worktree per contract); parked at ship sign-off
- question: https://github.com/PyAutoLabs/PyAutoArray/issues/372#issuecomment-4932908179
- autonomy: supervised effective (--auto chain 2026-07-09; bug cap binds over safe header; ship sign-off will park with question per contract)
- heart-ack: same 6-reason set as the assistant-ref-mechanics entry (in-session 2026-07-09); binds to exactly that set, any new reason parks
- note: consumers of edges_transformed = plot/inversion.py pcolormesh + mesh_geometry/rectangular_rotated.py — both inherit the fix; mcmc-corner-smoke (nightly blocker) queued in planned.md on autofit_workspace/PyAutoFit claims
- worktree: ~/Code/PyAutoLabs-wt/rect-adapt
- repos:
  - PyAutoArray: feature/rect-adapt

## slacs1430-acs-parity
- issue: https://github.com/PyAutoLabs/PyAutoReduce/issues/17
- session: claude --resume cc79d958-a1aa-45cb-b088-bd6cae94aa86
- status: workspace-dev (resumed 2026-07-10) — phase 3 in flight, autoreduce fit resumed from checkpoint (legacy fit follows serially); phases 0-2 done (pixel parity: data ratio 1.04; legacy noise lacks R=1.364 while slacs0008 legacy had it; legacy frame is rot270 of north-up, no mirror; acquire duplicate-exposure bug filed bug/pyautoreduce/acquire_duplicate_exposure_families.md, workaround = cache-manifest surgery already applied); phase 3 fits checkpointed mid-sampling — OOM lesson: ~5.5GB each, run ONE at a time
- resume: from PyAutoReduce main run `~/venv/PyAuto/bin/python prototypes/slacs1430_parity_fit.py autoreduce` then `... legacy` SERIALLY (Nautilus auto-resumes from output/slacs1430_parity/<key> checkpoints, 15M/4.9M present); compare fit_summary_*.json (θ_E/q/PA/shear vs lit 1.52"/0.68/111.7°; expect autoreduce widths ~1.36x wider from noise-R); post phase-3 verdict on #17; phase 4 = ship scripts/reduce_slacs1430.py + prototypes/slacs1430_parity_fit.py on feature/slacs1430-acs-parity once frame-products PR#18 merge releases the claim (four-leg gate, append autonomy_log.md row); PJ011646 WFC3 prompt is the queued follow-up
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
