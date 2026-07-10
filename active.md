# Active Tasks

## benchmark-calibration
- issue: https://github.com/PyAutoLabs/autolens_assistant/issues/59
- status: workspace-dev — first calibration campaign: teacher × {sonnet, haiku} + easy × {sonnet} via claude-code-subagent harness, serial (memory); records → benchmarks/runs/, RESULTS.md regen, rubric verdict on issue; PR at end
- autonomy: supervised effective (human-directed launch 2026-07-10 in-conversation, continuing #57 --auto chain; heart-ack: same set as #58 ship, in-session)
- note: judge = claude-fable-5 (this session) for judged rows; operator replies honest/minimal via SendMessage; failures recorded
- worktree: none (in-place: autolens_assistant on feature/benchmark-calibration)
- repos:
  - autolens_assistant: feature/benchmark-calibration

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
- status: workspace-dev — RECONCILED: XLA flag = autoconf LIBRARY POLICY (jax_wrapper.py sets it; venv export = the recommendation, KEEP); measured flag effect 1.54x single-JIT, vmap INSENSITIVE (0.110s both ways); original 2.5-5.3x-vs-May = mostly CONTENTION (loaded laptop); FINAL baseline run in flight (policy env explicit + quiet machine, load 0.6); phase-3 matrix = canonical env, NO rerun needed (good news on #56); A100 submits now carry explicit XLA_FLAGS export (cbb8b43); alma_high cells = GPU-only tier (2x 2h NUFFT timeouts); RAL GPU nodes DOWN; check_pinned vmap-array crash on main = already fixed on campaign branch e2578ae (rebase note)
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
- status: awaiting-input — parked at ship sign-off (gate: tests 202 pass / smoke n-a / review CLEAN / Heart YELLOW 6-reason set UNACKED); branch feature/pj011646-wfc3-parity committed locally bd9806b, NOT pushed; phases 0-2 verdicts on #25; model-parity fits parked (2 OOMs at n_live=100, laptop contended)
- autonomy: safe effective (--auto launched 2026-07-10; plan human-approved in-session pre-launch; no heart-ack given)
- note: keck-ao/slacs1430 pattern — analysis on PyAutoReduce main, NO worktree claim (jwst-frame-feasibility holds it); ship gated on claim release or human direction; autolens_assistant driver-only (in-place branch belongs to assistant-ref-mechanics — scratch writes only); model-parity fits SERIAL on quiet machine (~5.5GB)
- question: https://github.com/PyAutoLabs/PyAutoReduce/issues/25#issuecomment-4936211921
- worktree: none (analysis on PyAutoReduce main; branch feature/pj011646-wfc3-parity only at ship)
- repos:

## rect-adapt
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/372
- session: claude --resume 4bf88e6b-682d-4590-906f-77b68d059b26
- status: MERGED 2026-07-10 (human-directed via kernel-cdf session, coordinated order #375→#374; issue #372 closed with verification upthread) — entry ready to retire to complete.md by its owning session
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

## autofit-assistant-birth
- issue: https://github.com/PyAutoLabs/autofit_assistant/issues/1
- session: (this CLI session, 2026-07-10)
- status: complete-pending-merge — ALL 4 PHASES DONE: Phase 0 on main; Phases 1-3 = PR#2; Phase 4 (benchmarks+hpc+llms.txt+wiki-currency CI) = PR#3 stacked on #2 (retarget after #2 merges); newborn checklist legs 1-3 green, leg 4 (chat-surface smoke) human post-merge; follow-ups to file: PyAutoBuild release wiring, deferred skill tranche (chain/custom_analysis/simulate/plot_fit/debug) (d388ce1 tooling+9 skills 50/50 tests; afa0ffa 16-page wiki provenance-stamped; 6e1426c domain-adaptation skills + demos validated: Gaussian recovers truth, SNe Om=0.344 H0=73.1 vs Brout22); ALL parked behind one ship sign-off; Phase 4 (benchmarks/hpc/llms.txt/CI) deliberately queued until sign-off (cards bind to reviewable README/demos)
- pr: https://github.com/PyAutoLabs/autofit_assistant/pull/2 (phases 1-3, awaiting human merge)
- autonomy: supervised effective (--auto launched 2026-07-10; header supervised = feature too-large cap; NO heart-ack given — any Heart YELLOW at ship parks)
- launch-gates: answered in-session 2026-07-10 — repo PUBLIC at birth (dedicated repo-creation question); Phase 0 HAND-AUTHORED (clone-v1 plan as file-inventory checklist only); demos = 1D Gaussian + SNe cosmology distance-modulus fit
- note: Feature-Agent research re-home OVERRULED at launch (scoping done at intake; design in prompt); absorbs research/autofit_assistant/autofit_assistant_planning.md (retire at ship); PyAutoMemory never referenced in public output (Phase 2 pages are generalised rewrites)
- worktree: none (in-place: ~/Code/PyAutoLabs/autofit_assistant, new clone)
- repos:
  - autofit_assistant: main (phase 0), then feature/afa-phase-<n>
