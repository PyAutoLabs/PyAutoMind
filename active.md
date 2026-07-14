# Active Tasks


## corrective-pr-heart-red
- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/112
- status: library-dev — human-authorized corrective-PR exception for Heart RED. Plan approved in-session (present-and-wait, no --auto). Design decisions: human-only path (never under --auto; "Heart RED never acknowledged autonomously" stays verbatim) + name-one-of-several RED reasons (PR scopes which reason it clears; siblings remain, release blocked until all clear).
- worktree: ~/Code/PyAutoLabs-wt/corrective-pr-heart-red
- autonomy: supervised (feature cap; no --auto — present-and-wait; hard-invariant doctrine change)
- repos:
  - PyAutoBrain: feature/corrective-pr-heart-red
  - PyAutoMind: feature/corrective-pr-heart-red


## database-latent-wheel-load
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1367
- status: blocked — implementation + tests complete locally; ship gate is Heart RED (`release validation FAILED (stage integrate)`)
- worktree: ~/Code/PyAutoLabs-wt/database-latent-wheel-load
- autonomy: supervised (--auto launched 2026-07-14; plan approved in-session; no heart-ack)
- blocker: https://github.com/PyAutoLabs/PyAutoFit/issues/1367#issuecomment-4967286690
- resume: re-run `/ship_library` after Heart is no longer RED; no commit/push/PR exists
- repos:
  - PyAutoFit: feature/database-latent-wheel-load


## release-validation-tail-burndown
- issue: https://github.com/PyAutoLabs/PyAutoHeart/issues/72
- status: in-progress (supervised --auto) — ROOT CAUSE = jax 0.9.2(dev)→0.10.2(release) numerical drift on pixelized JAX inversions (isolated: only jax varied; rectangular Δ2.6e-4, mge Δ1.8e-3 rel). Human approved strategy (ii) loosen golden + keep round-trip, AND "match dev to release". DONE: (1) bumped ~/venv/PyAuto jax→0.10.2 (whole tail now reproducible in dev); (2) cluster A fixed+validated (autolens_workspace_test multi/rectangular.py+rectangular_mge.py: golden→gross-guard rtol=1e-2, exact check=vmap==jit round-trip). Committed d1d3cfe LOCAL (not pushed). Flagged to user: mge 1.8e-3 (7×) as possible (iv)-investigate.
- worktree: ~/Code/PyAutoLabs-wt/release-validation-tail-burndown (autolens_workspace_test on feature/release-validation-tail-burndown)
- resume: MULTI-ROOT-CAUSE (refined #72 comment-4966946018). DONE THIS SESSION: (A) jax-drift FIXED d1d3cfe (autolens_workspace_test multi/rectangular* golden→gross-guard 1e-2 + round-trip); (timeout) PyAutoHeart c19c948 BUILD_SCRIPT_TIMEOUT=1800 on mode=release step only (jax_grad completes 6:38 within it) — stopgap, speedup prompt filed draft/feature/profiling/profiling_agent_jax_compile_time_scope.md; (intake) profiling-scope prompt filed. TWO REAL BUGS uncovered (need own tasks): (B) jax_grad/imaging_pixelization param-idx-9 autodiff-vs-FD mismatch ad=1.5e5 vs fd=-5.3e6 (opp sign) — likely FD-blowup wanting skip_indices, confirm not jax-0.10.2 AD regression vs 0.9.2; (D) database ×6 fast AssertionError 'Failed to load latent variables' — passes dev even under TEST_MODE=0 → wheel-env dep issue (SQLAlchemy2.0.51/dill0.4.1/numpy2.4.6) in latent-var deserialization; repro needs wheel-env. STILL TBD: C viz_jit×3 (real-search viz timing/wheels), E aggregator×2, F chaining/slam, G interferometer, H minimal_output. WORKTREE: ~/Code/PyAutoLabs-wt/release-validation-tail-burndown (autolens_workspace_test d1d3cfe + PyAutoHeart c19c948, LOCAL not pushed). Run remaining as register_and_iterate; file B+D as own bug prompts. 3 blocker bugs DONE—don't reopen. Inventory: active/release_validation_tail_burndown_2026_07.md.
- question: https://github.com/PyAutoLabs/PyAutoHeart/issues/72#issuecomment-4966720654 (mge-drift-investigate optional; else continue)
- autonomy: supervised (--auto launched 2026-07-14 "continue and start --auto"; test cap; no heart-ack; ship parks for human sign-off)
- ENV NOTE: ~/venv/PyAuto is now jax 0.10.2 (was 0.9.2) — affects concurrent sessions (next-wave gradient optimizers tuned on 0.9.2). Stale jax_cuda12_plugin 0.9.2 (GPU only) + jax-finufft<0.8 conflict (unused). See [[reference_laptop_gpu_jax_setup]].
- repos:
  - autolens_workspace_test: feature/release-validation-tail-burndown


## next-wave-population-optimizers
- issue: https://github.com/PyAutoLabs/autolens_workspace_developer/issues/97
- status: PAUSED for the night 2026-07-13 (user→bed, resume tomorrow). Phase-1 done+committed (aacdac2/197456a, pushed WIP on feature/next-wave-population-optimizers; NOT PR'd — supervised). Result: interacting-population needs BOTH diversity AND gradients. cmaes COLLAPSES (r_E7.999, 0/16); sv_cmaes (Stein repulsion, gradient-free) PREVENTS collapse (r_E2.605, still improving, 0/8, slow); svgd (repulsion+gradient=ideal) CPU-compile-prohibitive → needs GPU. Winner stays multi-start Adam.
- RESUME (PAUSED again by user 2026-07-14 mid-RAL-setup): CORRECTION — RAL IS reachable + agent-authorised (user gave access 2026-07-14): SSH alias `euclid_jump` (→euclid-saas.roe.ac.uk user jnightin, ProxyJump jump_finan, KEY-based no 2FA — works non-interactively). RAL has SLURM `gpu` partition = gpu:A100:4 (a node IDLE), login node reaches GitHub (GITHUB_OK). PyAuto stack /mnt/ral/jnightin/PyAuto on main; autolens_profiling present; autolens_workspace_developer NOT_PRESENT (clone feature branch there). Drive via project hpc/sync `push-submit gpu <script>`/`jobs`/`tail gpu`/`pull` OR direct sbatch. laptop 48-start GPU DID reach truth (+31787.84 by step200 in log) but process killed pre-summary-write (no summary file). NEXT: (a) clone autolens_workspace_developer@feature/next-wave-population-optimizers on RAL; (b) verify RAL GPU venv deps blackjax(need≥1.x)/evosax/optax (my dep-check ssh had a quoting bug — redo); (c) write GPU sbatch (--partition=gpu --gres=gpu:A100:1, source /mnt/ral/jnightin/autolens_profiling/activate.sh) for searches_minimal/{svgd,sv_cmaes,gpu_multi_start_adam}.py; (d) submit+monitor+pull. (opt) multi-start ADABelief/Lion CPU. Full state: searches_minimal/next_wave_findings.md "GPU/HPC status".
- also-pending: PR#96 (task jax-gradient-optimizer-benchmark) awaiting human MERGE; on merge this branch rebases onto main.
- worktree: ~/Code/PyAutoLabs-wt/next-wave-population-optimizers
- autonomy: supervised (--auto continued from #95 session via "go...do next task" 2026-07-13; experiment cap; ship parks for human sign-off)
- note: branch feature/next-wave-population-optimizers STACKED on feature/jax-gradient-optimizer-benchmark (PR#96 unmerged) — reuses _grad_setup.py + multi_start_adam.py; REBASE onto main once #96 merges. Reuses #95 MAP harness. Metric = fraction of starts/particles → truth basin (r_E≈1.6) + wallclock + evals vs multi-start Adam baseline.
- repos:
  - autolens_workspace_developer: feature/next-wave-population-optimizers


## jax-gradient-optimizer-benchmark
- issue: https://github.com/PyAutoLabs/autolens_workspace_developer/issues/95
- status: awaiting-merge — SHIPPED (human sign-off "go, ship" 2026-07-13; committed 6344258, pushed). PR open, workspace-only. Shipped through organism-scoped Heart RED (held release + stale 2026-07-09 run; nothing branch-related). Merge stays human → then move to complete/.
- pr: https://github.com/PyAutoLabs/autolens_workspace_developer/pull/96
- worktree: ~/Code/PyAutoLabs-wt/jax-gradient-optimizer-benchmark
- autonomy: supervised (--auto launched 2026-07-13 in-session; plan approved in-conversation incl. MAP objective via "do MAP, and go --auto"; no heart-ack given)
- result: single cold-start ALL fail wrong-basin (Adam r_E4.89 / ADABelief 5.01 / L-BFGS 4.42 / SVI 3.54±0.07); multi-start Adam 12× WINS (r_E1.600, logL+31788, 2/12 basin) = GIGA-Lens recipe. LM deferred (single-start→same basin; needs residual-vector). Follow-up filed: experiment/workspaces/next_wave_population_gradient_samplers_on_the.md (SVGD/flowMC/GGNS/SMC-HMC + converged Nautilus).
- repos:
  - autolens_workspace_developer: feature/jax-gradient-optimizer-benchmark


## eceb-editorial-revision
- issue: https://github.com/Jammy2211/euclid_assistant/issues/6
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/eceb-editorial-revision
- note: private manuscript companion is /mnt/c/Users/Jammy/Science/euclid/paper on the same feature branch
- repos:
  - euclid_assistant: feature/eceb-editorial-revision


## benchmark-calibration
- issue: https://github.com/PyAutoLabs/autolens_assistant/issues/59
- status: workspace-dev — first calibration campaign: teacher × {sonnet, haiku} + easy × {sonnet} via claude-code-subagent harness, serial (memory); records → benchmarks/runs/, RESULTS.md regen, rubric verdict on issue; PR at end
- autonomy: supervised effective (human-directed launch 2026-07-10 in-conversation, continuing #57 --auto chain; heart-ack: same set as #58 ship, in-session)
- note: judge = claude-fable-5 (this session) for judged rows; operator replies honest/minimal via SendMessage; failures recorded
- worktree: none (in-place: autolens_assistant on feature/benchmark-calibration)
- repos:
  - autolens_assistant: feature/benchmark-calibration


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

## morning-status-release-rehearsal
- issue: https://github.com/PyAutoLabs/PyAutoHeart/issues/39
- session: claude --resume ff9a8b2f-fda0-4bab-8962-1814843aa374
- status: RESOLVED 2026-07-09 (by session 5d58ef6a) — user re-set BOTH May-17 secrets (webhook + CLAUDE_CODE_OAUTH_TOKEN); morning_health dispatched → Slack POST success; digest needed 3 more CI fixes on Mind main (checkout, show_full_output, allowedTools Write; 51e869e/d042289/0b78d5f) → fully green, delivered. Details: issues/39#issuecomment-4924031684. Entry ready to retire to complete.md by its owning session
- prs: PyAutoBuild#119 + PyAutoHeart#40 + PyAutoMind#41 (independent; merge Mind last is tidiest — its morning_health reads the others)
- post-merge: dispatch morning_health.yml on Mind main (Slack POST leg); flip vars.RELEASE_MODE=live on PyAutoBuild when satisfied (human)
- autonomy: human-required effective (release cap; --auto launched 2026-07-08, plan approved in-session; ship sign-off + merge human)
- cleanup 2026-07-09: worktree removed + feature branches (local+remote) deleted via /repo_cleanup — all PRs were merged; remaining leg (webhook secret + morning_health.yml dispatch) is human-only and needs no repo claim

