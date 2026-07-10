# Active Tasks

## stpsf-tier2b
- issue: https://github.com/PyAutoLabs/PyAutoReduce/issues/29
- session: claude --resume 4bf88e6b-682d-4590-906f-77b68d059b26
- status: library-dev — STPSF tier-2b fallback for JWST frame PSFs (user-directed "lift PSF coverage"; 3/6 -> 6/6 target on F115W)
- autonomy: supervised effective (--auto chain 2026-07-10; plan on issue); parks at ship sign-off
- heart-ack: same 6-reason set as prior entries this chain; any new reason parks
- note: env needs stpsf + reference data install (not in venv yet); validation reruns frames packaging on cached F115W _crf files
- worktree: ~/Code/PyAutoLabs-wt/stpsf-tier2b
- repos:
  - PyAutoReduce: feature/stpsf-tier2b

## markdown-example-renderings
- issue: https://github.com/PyAutoLabs/PyAutoBuild/issues/134
- status: library-dev — build generate_markdown.py (execute curated scripts → nbconvert md + PNGs) in PyAutoBuild, then autolens pilot (root start_here + imaging five + guides trio); phase 2 (other dataset types/workspaces/HowTo) files as a new prompt at ship
- autonomy: safe effective (--auto launched 2026-07-10; docs ≤ medium after phasing; plan on issue; NO heart-ack given — any Heart YELLOW at ship parks)
- note: execution never TEST_MODE; modeling images via completed-run resume cache (first build pays one real sampling run); images committed — verify .gitignore doesn't swallow markdown/ outputs
- worktree: ~/Code/PyAutoLabs-wt/markdown-example-renderings
- repos:
  - PyAutoBuild: feature/markdown-example-renderings
  - autolens_workspace: feature/markdown-example-renderings

## preopt-breakdown-dashboard
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/59
- status: workspace-dev — imaging leg DONE 5/5 clean; HEADLINE: real >=~1.8x library slowdown on mesh cells since May (identical cell configs; confirmed vs phase-3 quiet-machine runtime; F-matrix ~50% everywhere); alma_high cells on retry (root cause = missing dataset + auto-simulate OOM; seeded 234MB from phase-3 wt); laptop numbers = ambient-load fallback tier; A100 leg dispatch-ready (15 submits, 3bb613a) but RAL GPU nodes DOWN
- campaign: driver scratchpad/breakdown_campaign.sh (session a66a757a), logs scratchpad/breakdown_logs/; interruption-safe — each cell's JSON persists to results/breakdown/ on completion; cold-resume = rerun remaining cells' commands from the driver (skip cells whose v-current JSON exists)
- autonomy: supervised effective (--auto launched 2026-07-10; header supervised binds over maintenance cap safe; plan on issue; no heart-ack given — any Heart YELLOW at ship parks)
- claim-override: human-directed 2026-07-10 — proceeds alongside profiling-preopt-campaign's autolens_profiling claim ("i dont see a clash"); phase 4 works likelihood_breakdown/ + README, phase 3 works likelihood_runtime/ — distinct paths; coordinate merge order at ship (README/build tooling may touch both — rebase on campaign branch if needed)
- note: dashboard deliverable depends on phase-3 PreOptimizationTimes runtime baseline (not yet tagged); breakdown runs (deliverable 1) proceed independently; HPC CPU/A100 legs gated on RAL availability
- worktree: ~/Code/PyAutoLabs-wt/preopt-breakdown-dashboard
- repos:
  - autolens_profiling: feature/preopt-breakdown-dashboard

## pj011646-wfc3-parity
- issue: https://github.com/PyAutoLabs/PyAutoReduce/issues/25
- session: claude --resume cc79d958-a1aa-45cb-b088-bd6cae94aa86
- status: workspace-dev — phases 0-2 done (target=14653 F160W 5exp; DQ-512 blob hole -> bits-dial bug filed bug/pyautoreduce/wfc3_ir_dq_bits_dial.md, final_bits=512 workaround in script; orientation id-71.1deg corr 0.997; data ratio 1.016; noise x4.9 decomposed = R 2.39 x ours-conservative 1.58 x aris-underpredicts 1.3, aris map = 0.62x his own sky scatter; PSF 0.259 vs 0.202); phase 3 fits QUEUED behind free memory (watcher armed; laptop at 12/15GB from other sessions)
- autonomy: safe effective (--auto launched 2026-07-10; plan human-approved in-session pre-launch; no heart-ack given)
- note: keck-ao/slacs1430 pattern — analysis on PyAutoReduce main, NO worktree claim (jwst-frame-feasibility holds it); ship gated on claim release or human direction; autolens_assistant driver-only (in-place branch belongs to assistant-ref-mechanics — scratch writes only); model-parity fits SERIAL on quiet machine (~5.5GB)
- worktree: none (analysis on PyAutoReduce main; branch feature/pj011646-wfc3-parity only at ship)
- repos:

## rectangular-kernel-cdf-mesh
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/373
- library-pr: https://github.com/PyAutoLabs/PyAutoArray/pull/374
- status: shipped, awaiting-merge — SUCCESS CRITERION MET: strict FD ALL params in every config (imaging os_pix=1 bw=0.1 + os_pix=4 + production shape; interferometer sparse production shape), eager-vs-JIT everywhere, parity beats/2.7e-5/6.3e-4/3.9e-5; PRs: PyAutoArray#374 + workspace_test#161 + workspace_developer#90 (all pending-release, library-first); rect-adapt #375 folded in by merge + verified visually+numerically (comment on #372) — merge order #375→#374→#161+#90, whichever library PR lands second is a no-op; batched sign-off question on #373 (os1 parity→no-degradation; G ≤1e-3 at 6.3e-4 floor; FD-step-sweep semantics)
- workspace-prs: https://github.com/PyAutoLabs/autolens_workspace_test/pull/161 + https://github.com/PyAutoLabs/autolens_workspace_developer/pull/90
- followups (unfiled, queue discipline): chunked kernel forward (O(M×N) mem, 60GB @ 15k px os4); solver branch-flip investigation (point-width <1e-15, ΔLL 1.6e-3–14, PDIP tie-break suspect); sampler trials (prompt-deferred, now unblocked)
- autonomy: supervised effective (--auto continued in-session 2026-07-10 after human plan approval + library-ship sign-off; human directed "continue --auto" → proceed to PR-open, merge stays human)
- heart-ack: in-session 2026-07-10 — exact set: workspace validation not passing (3 failed 2026-07-09T09-48-30Z); 58 stale parked scripts; autolens_assistant pinned BEHIND installed; PyAutoMind open PR 10d old; install verification not run; no release validation for current source. Binds to exactly this set; any new reason parks.
- claim-override: human-directed 2026-07-10 — proceeds alongside rect-adapt's PyAutoArray claim ("distinct hunks, they don't clash"); coordinate merge order at ship
- note: same-file adjacency with parked rect-adapt wt (#372, uncommitted, edges_transformed hunk only) — distinct hunks in mesh_geometry/rectangular.py, clean merge either order; workspace leg (autolens_workspace_test jax_grad + autolens_workspace_developer README row) follows library PR
- worktree: ~/Code/PyAutoLabs-wt/rectangular-kernel-cdf-mesh
- repos:
  - PyAutoArray: feature/rectangular-kernel-cdf-mesh
  - autolens_workspace_test: feature/rectangular-kernel-cdf-mesh
  - autolens_workspace_developer: feature/rectangular-kernel-cdf-mesh

## rect-adapt
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/372
- session: claude --resume 4bf88e6b-682d-4590-906f-77b68d059b26
- status: library-shipped, awaiting-merge — sign-off answered in-conversation (go --auto); suite 877 re-run at ship; PR MERGEABLE against advanced main; merge stays human per contract
- pr: https://github.com/PyAutoLabs/PyAutoArray/pull/375
- autonomy: supervised effective (--auto chain 2026-07-09; bug cap binds over safe header; ship sign-off will park with question per contract)
- heart-ack: same 6-reason set as the assistant-ref-mechanics entry (in-session 2026-07-09); binds to exactly that set, any new reason parks
- note: consumers of edges_transformed = plot/inversion.py pcolormesh + mesh_geometry/rectangular_rotated.py — both inherit the fix; mcmc-corner-smoke (nightly blocker) queued in planned.md on autofit_workspace/PyAutoFit claims
- worktree: ~/Code/PyAutoLabs-wt/rect-adapt
- repos:
  - PyAutoArray: feature/rect-adapt

## slacs1430-acs-parity
- issue: https://github.com/PyAutoLabs/PyAutoReduce/issues/17
- session: claude --resume cc79d958-a1aa-45cb-b088-bd6cae94aa86
- status: MERGED 2026-07-10 (0face12, squash; human-authorized in-session) — branches deleted; #17 stays OPEN for the parked model-parity leg only; entry retires to complete.md once that leg's verdict lands
- pr: https://github.com/PyAutoLabs/PyAutoReduce/pull/23
- resume(model-parity leg): `~/venv/PyAuto/bin/python prototypes/slacs1430_parity_fit.py autoreduce` then `... legacy` from PyAutoReduce root; compare fit_summary_*.json; verdict on #17
- note: acquire-dupe bug prompt RETIRED (fixed on main by #18's is_direct_product; my run disclosed on PR#23 as HAP-family); PJ011646 WFC3 follow-up prompt queued (methodology notes on #17)
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

## ep-priors-fable-reassess
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1330
- session: claude --resume 3589268b-e5c9-4b32-b655-d07f732ea300
- status: awaiting-input — phase 0 complete; decision hub PyAutoFit#1331 open for maintainer/contributor guidance (fix-batch + 5 decisions)
- question: https://github.com/PyAutoLabs/PyAutoFit/issues/1331
- worktree: none (read-only reassessment on PyAutoFit main @ 0f26ff2d8; verdicts land in PyAutoMind bug/priors)
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
