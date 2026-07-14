# Active Tasks


## pyautolens-jax-joss-paper
- issue: https://github.com/PyAutoLabs/PyAutoLens/issues/608
- session: codex
- status: blocked-heart-red — manuscript scaffold complete and structurally validated; uncommitted in worktree; ship_library blocked by unrelated Heart RED reasons
- worktree: ~/Code/PyAutoLabs-wt/pyautolens-jax-joss-paper
- repos:
  - PyAutoLens: feature/pyautolens-jax-joss-paper

## multi-start-gradient-search
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1369
- status: blocked-heart-red — implementation COMPLETE + verified on branch (uncommitted in worktree); autonomous ship blocked by Heart RED (organism-scope, not this branch). Core search + samples/result + 3 rule-classes (af.MultiStartAdam/MultiStartADABelief/MultiStartLion) done; JAX e2e validation in autofit_workspace_test (library-first gate) still pending. Phases 2 (config/defaults) + 3 (workspace examples) not yet issued.
- worktree: ~/Code/PyAutoLabs-wt/multi-start-gradient-search
- autonomy: supervised (--auto launched 2026-07-14; plan approved in-session; no heart-ack)
- heart-red-block:
  - launched --auto 2026-07-14; effective level supervised (min of header=supervised, feature-large cap=supervised)
  - Heart RED at ship (score 0): PyAutoGalaxy 1 behind origin; PyAutoLens 1 behind origin; release validation FAILED (stage integrate). All pre-existing release-tail reasons, unrelated to this feature.
  - Contract: Heart RED forbids commit/push/PR-open at every autonomy level; --auto never acknowledges RED. Corrective-PR exception N/A (feature repairs no named RED reason). Nothing shipped; no code modified to pass a leg.
  - resume: when Heart clears to GREEN/STALE (or YELLOW human-acked), run ship_library to commit/push/PR on PyAutoFit#1369; branch legs 1-3 are green (see issue).
- note: PyAutoFit softly claimed by database-latent-wheel-load (#1368 merged, corrective-validation only) — human-approved parallel worktree, no source collision. autofit_workspace_test worktree deferred to post-library-merge (library-first gate).
- repos:
  - PyAutoFit: feature/multi-start-gradient-search

## interferometer-analysis-fitexception
- issue: https://github.com/PyAutoLabs/PyAutoLens/issues/606
- status: merged-awaiting-corrective-validation — fresh wheels, release-integration rerun, and a new Heart verdict remain; issue kept open
- pr: https://github.com/PyAutoLabs/PyAutoLens/pull/607
- merge: 5250d80a51f77513adf462290d5319e2ea85aed1 — squash-merged by explicit human direction 2026-07-14; issue #606 remains open
- worktree: removed post-merge 2026-07-14 (branch feature/interferometer-analysis-fitexception deleted local+remote; corrective validation runs in CI on main, not the worktree)
- autonomy: supervised (--auto launched 2026-07-14; plan approved in-session; scope B chosen by human → point_source guard added; no heart-ack)
- note: resolves release-validation tail item G (PyAutoHeart#72). NOT jax-0.10.2 drift — interferometer (and point_source) log_likelihood_function lacked the imaging analysis's NumPy-path try/except→FitException guard, so a non-PD inversion (np.linalg.cholesky at abstract.py:743) crashed the search instead of resampling; JAX path masks it via NaN. Fix = mirror imaging/model/analysis.py:132-144. Reproduced on jax 0.10.2 with PYAUTO_DISABLE_JAX=1.
- corrective-red:
  - reason: release validation FAILED (stage integrate)
  - authorization: https://github.com/PyAutoLabs/PyAutoLens/issues/606#issuecomment-4969093660
  - causal-map: Heart integrate failure → #606 NumPy-path unguarded Cholesky log-det crash → two-file try/except→FitException guard mirroring imaging → commit 904cd64e3 → PR #607
  - scope: exception authorized one pending-release PR (two-file analysis guard) only; no merge, issue close, release, or rehearsal; merge stays a separate human act
  - sibling-red: workspace validation 3 failed (2026-07-09); 58 stale parked scripts; PyAutoMind open PR 14d old; install verification not run — all remain, Heart stays RED
  - tests: full test_autolens/ 381 passed (incl. 22 interferometer + 58 point); numpy-path model_fit.py real search now completes (was LinAlgError crash); jax branch unchanged
  - validation: after human merge, build fresh wheels, rerun release integration on main, obtain a new Heart verdict before any release decision
  - review: self-CLEAN — commit 904cd64e3; two files (+20/−5), mirrors imaging pattern, no mixed scope
- repos-merged: PyAutoLens (feature/interferometer-analysis-fitexception → main 5250d80a5; branch deleted; no live worktree claim)


## mass-cse-jax-decompose
- issue: https://github.com/PyAutoLabs/PyAutoGalaxy/issues/499
- status: merged-awaiting-corrective-validation — P1 merged; fresh wheels + release-integration rerun + new Heart verdict remain; issue kept open
- library-pr: https://github.com/PyAutoLabs/PyAutoGalaxy/pull/500
- merge: b8bc0a3e09f57b403cd25b74ec668d01caa745f4 — squash-merged by explicit human direction 2026-07-14; issue #499 kept open until release-validation reruns on wheels
- worktree: removed post-merge 2026-07-14 (branch feature/mass-cse-jax-decompose deleted local+remote; corrective validation runs in CI on main, not the worktree)
- autonomy: supervised (--auto launched 2026-07-14; plan approved in-session; ship sign-off + merge given in-session issuecomment-4969172226; no heart-ack; bug cap)
- note: P1 DONE+MERGED. Fixes release-validation tail item (chaining.py FAIL in run 29279095224) — thread xp through Sersic CSE deflection path; branch-free cse_settings_from static 50/80 counts; jnp.linalg.lstsq on JAX path. Validated: chaining.py green 0-tb, 432 mass tests pass, jit round-trip ~1e-11, numpy-vs-jax ≤2e-5 n∈[1,4], regression mass_via_integral/sersic*.py pass rtol=1e-3. NFW deflects analytically (HK24) so out of scope. P2 DROPPED by human (integration test fixed): n<1 lstsq gap 3e-3 documented, below CSE approx error, not release-gating; profiles_jit.py harness addition not pursued. Real library bug (incomplete CSE JAX port), not jax-0.10.2 regression.
- repos:
  - PyAutoGalaxy: feature/mass-cse-jax-decompose


## jax-grad-param9-autodiff-fd-mismatch
- issue: https://github.com/PyAutoLabs/autolens_workspace_test/issues/164
- status: merged-awaiting-corrective-validation — fresh wheels, release integration rerun, and a new Heart verdict remain
- worktree: ~/Code/PyAutoLabs-wt/jax-grad-param9-mismatch
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace_test/pull/165
- merge: 6c4ff26ae3b0305d92d81f82b926ccb96373c578 — merge commit created by explicit human monitor-and-merge direction on 2026-07-14; issue remains open
- autonomy: supervised (--auto launched 2026-07-14; overlap explicitly acknowledged by human; corrective-PR exception authorized in-session)
- note: parallel autolens_workspace_test claim is accepted because release-validation-tail-burndown changes only jax_likelihood_functions/multi/rectangular*.py; this task changes jax_grad/imaging_pixelization.py
- corrective-red:
  - reason: release validation FAILED (stage integrate)
  - authorization: https://github.com/PyAutoLabs/autolens_workspace_test/issues/164#issuecomment-4968314436
  - causal-map: Heart integrate failure → issue #164 jax_grad parameter-9 diagnosis → parameter-specific documented FD exclusion → PR #165
  - sibling-red: PyAutoFit: 1 commit(s) behind origin (not addressed)
  - scope: the exception authorized one pending-release PR only; merge was separately human-authorized; no issue close, release, or release rehearsal
  - tests: imaging passed on JAX 0.9.2 and 0.10.2; interferometer passed on 0.10.2; 52 smoke checks passed with 3 declared skips; all four PR smoke jobs passed on Python 3.12 and 3.13
  - validation: build fresh wheels, rerun release integration on main, and obtain a new Heart verdict before closing the issue or making a release decision
  - review: CLEAN — reviewed head 540e093de2313e330b179a876399aab3650955fd remained unchanged through merge
- repos:
  - autolens_workspace_test: feature/jax-grad-param9-mismatch


## database-latent-wheel-load
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1367
- status: merged-awaiting-corrective-validation — fresh wheels, release integration rerun, and a new Heart verdict remain
- pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1368
- merge: 4724e20a1 — squash-merged by explicit human direction on 2026-07-14; issue remains open
- worktree: ~/Code/PyAutoLabs-wt/database-latent-wheel-load
- autonomy: supervised (--auto launched 2026-07-14; plan approved in-session; no heart-ack)
- corrective-red:
  - reason: release validation FAILED (stage integrate)
  - authorization: https://github.com/PyAutoLabs/PyAutoFit/issues/1367#issuecomment-4967751375
  - corrective-issue: PyAutoFit#1367
  - causal: release profile PYAUTO_TEST_MODE=0 was treated as enabled by raw string truthiness, routing database output under output/test_mode and causing the stage-integrate database scrapers to find zero searches
  - scope: existing two-file producer fix and regression tests only; one pending-release PR; the exception itself authorized no merge, issue close, release, rehearsal, or unrelated changes; merge was separately human-authorized
  - tests: 14 focused passed; 1475 full-suite passed and 1 skipped; all 6 release-profile database scripts passed on exact wheel dependencies
  - validation: build fresh wheels, rerun release integration validation, and obtain a new Heart verdict before closing the issue or making a release decision
- review: CLEAN — commit 2ff67195c; one causal commit, two files, no mixed or unrelated scope
- prior-blocker: https://github.com/PyAutoLabs/PyAutoFit/issues/1367#issuecomment-4967286690
- repos:
  - PyAutoFit: feature/database-latent-wheel-load


## release-validation-tail-burndown
- issue: https://github.com/PyAutoLabs/PyAutoHeart/issues/72
- status: CLOSING-OUT — all real bugs fixed+merged+verified on release stack (A jax-drift wst#166, B jax_grad-param9 wst#165, C viz+H minimal via D PyAutoFit#1368, D database #1368, E aggregator autolens_workspace#275, F CSE PyAutoGalaxy#500, G interferometer PyAutoLens#607, jax_grad-config wst#167, timeout PyAutoHeart#73, shapelets/delaunay no_run wst#167/agwt#71/agw#131). Tail 18f/5t→ correctness-clean. Heart still RED on integrate due to STRUCTURAL perf-flake tail (shifting slow real-search timeouts run-to-run) + G-family singular/non-PD in more paths. STOPPED the re-validate loop. 2 follow-ups filed: draft/bug/autolens/interferometer_pixelization_singular_resample_guard.md + draft/feature/health_fixes/mode_release_tier_slow_scripts_advisory.md (mode=release advisory-tiering = the real path to yellow). E/F/G/param9/database merged by parallel sessions; retire their entries.
- worktree: ~/Code/PyAutoLabs-wt/release-validation-tail-burndown (autolens_workspace_test on feature/release-validation-tail-burndown)
- resume: MULTI-ROOT-CAUSE (refined #72 comment-4966946018). DONE THIS SESSION: (A) jax-drift FIXED d1d3cfe (autolens_workspace_test multi/rectangular* golden→gross-guard 1e-2 + round-trip); (timeout) PyAutoHeart c19c948 BUILD_SCRIPT_TIMEOUT=1800 on mode=release step only (jax_grad completes 6:38 within it) — stopgap, speedup prompt filed draft/feature/profiling/profiling_agent_jax_compile_time_scope.md; (intake) profiling-scope prompt filed. TWO REAL BUGS uncovered (need own tasks): (B) jax_grad/imaging_pixelization param-idx-9 autodiff-vs-FD mismatch ad=1.5e5 vs fd=-5.3e6 (opp sign) — likely FD-blowup wanting skip_indices, confirm not jax-0.10.2 AD regression vs 0.9.2; (D) database ×6 fast AssertionError 'Failed to load latent variables' — passes dev even under TEST_MODE=0 → wheel-env dep issue (SQLAlchemy2.0.51/dill0.4.1/numpy2.4.6) in latent-var deserialization; repro needs wheel-env. STILL TBD: C viz_jit×3 (real-search viz timing/wheels), E aggregator×2, F chaining/slam, G interferometer, H minimal_output. WORKTREE: ~/Code/PyAutoLabs-wt/release-validation-tail-burndown (autolens_workspace_test d1d3cfe + PyAutoHeart c19c948, LOCAL not pushed). Run remaining as register_and_iterate; file B+D as own bug prompts. 3 blocker bugs DONE—don't reopen. Inventory: active/release_validation_tail_burndown_2026_07.md.
- question: https://github.com/PyAutoLabs/PyAutoHeart/issues/72#issuecomment-4966720654 (mge-drift-investigate optional; else continue)
- autonomy: supervised (--auto launched 2026-07-14 "continue and start --auto"; test cap; no heart-ack; ship parks for human sign-off)
- ENV NOTE: ~/venv/PyAuto is now jax 0.10.2 (was 0.9.2) — affects concurrent sessions (next-wave gradient optimizers tuned on 0.9.2). Stale jax_cuda12_plugin 0.9.2 (GPU only) + jax-finufft<0.8 conflict (unused). See [[reference_laptop_gpu_jax_setup]].
- repos:
  - autolens_workspace_test: feature/release-validation-tail-burndown


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


## aggregator-quick-fit-consolidation
- issue: https://github.com/PyAutoLabs/autolens_workspace/issues/274
- status: merged-awaiting-corrective-validation — fresh wheels + release-integration rerun + new Heart verdict remain; issue kept open
- pr: https://github.com/PyAutoLabs/autolens_workspace/pull/275
- merge: c17ddfa5715d81b60cb3a607af08815f9257588e — squash-merged by explicit human direction 2026-07-14; all CI green (smoke 3.12/3.13, navigator, catalogue); issue #274 kept open
- commit: 62de0068 (feature/aggregator-quick-fit-consolidation)
- worktree: ~/Code/PyAutoLabs-wt/aggregator-quick-fit-consolidation
- autonomy: supervised (--auto launched 2026-07-14; plan approved in-session; no heart-ack)
- corrective-red:
  - reason: release validation FAILED (stage integrate)
  - authorization: https://github.com/PyAutoLabs/autolens_workspace/issues/274#issuecomment-4969425505
  - causal-map: Heart integrate failure → #274 aggregator IndexError (shallow tutorial fits pruned to 2 samples) → consolidate onto _quick_fit's 300-sample fit → PR #275
  - scope: one pending-release PR only; no merge, issue close, release, or rehearsal; merge stays a separate human act
  - sibling-red: PyAutoLens + PyAutoGalaxy behind origin; workspace validation 3 failed (2026-07-09); 58 stale parked scripts; PyAutoMind open PR 14d old; install verification not run — all remain, Heart stays RED
  - tests: n/a (workspace, no pytest); smoke = ordered guides/results under env_vars_release.yaml 14/14 pass (was 2 IndexError); both fits 300 samples, no 2-sample fit; identifier aceb0b5a matches _quick_fit primary; queries.py unique_tag match fixed
  - validation: after human merge, build fresh wheels, rerun release integration on main, obtain a new Heart verdict before any release decision
  - review: self-CLEAN — commit 62de0068; 8 files (+90/−22), 4 scripts + 4 regenerated notebooks; scope-clean
- note: consolidate guides/results tutorials onto one _quick_fit.py. start_here/galaxies_fits/samples each ran their own capped n_like_max=300 fit that prunes to 2 samples (no samples_weight_threshold=None) → deep from_sample_index(-10)/parameter_lists[9] IndexError. Fix = keep inline model but match it to _quick_fit (add shear; samples.py Sersic→MGE) so search.fit() resumes _quick_fit's 300-sample fit (identifier=[search,model,unique_tag], analysis-independent — verified). NOT PyAutoFit#1368 (release unsets PYAUTO_TEST_MODE for guides/results/). Resolves release-validation tail cluster E (PyAutoHeart#72).
- repos:
  - autolens_workspace: feature/aggregator-quick-fit-consolidation

## release-advisory-tier-slow-scripts
- issue: https://github.com/PyAutoLabs/PyAutoHeart/issues/74
- session: claude (start_dev 2026-07-14)
- status: library-dev
- worktree: ~/Code/PyAutoLabs-wt/release-advisory-tier-slow-scripts
- classification: both (Heart+Build mechanism first; *_test workspace advisory.yaml seeds = ship_workspace follow-up)
- branch: feature/release-advisory-tier-slow-scripts
- note: mode=release advisory tier — TIMEOUT_ADVISORY status + advisory.yaml registry so a declared-slow real-search timeout is YELLOW not integrate-RED; non-advisory timeout stays RED. Heart owns policy (validate.py/readiness.py/workspace-validation.yml), Build owns runner (result_collector/build_util/run_python/aggregate_results). The path to a shippable mode=release YELLOW after PyAutoHeart#72's real bugs. Cross-ref PyAutoHeart#72.
- autonomy: supervised (--auto launched 2026-07-14; effective=supervised; implementation approved in-session)
- status: library-shipped, workspace-pending (corrective-red PR-open; merge stays human)
- library-pr:
  - PyAutoHeart#75: https://github.com/PyAutoLabs/PyAutoHeart/pull/75
  - PyAutoBuild#153: https://github.com/PyAutoLabs/PyAutoBuild/pull/153
- status-detail: IMPLEMENTED+VERIFIED+SHIPPED-to-PR. Build: result_collector/build_util/run_python/aggregate_results (+test_advisory_tier) commit 8e502f4. Heart: validate.py/readiness.py/workspace-validation.yml/docs +tests commit eeb41df. Unit green (Build 118p; full Heart 268p); E2E via run_python verified (undeclared timeout→exit1/RED; advisory-only→exit0; aggregate ready True). Pre-existing unrelated Build fail: test_pre_build_skill (admin_jammy/PyAutoBrain manifest drift, fails on clean main).
- workspace-pr:
  - autogalaxy_workspace_test#72: https://github.com/PyAutoLabs/autogalaxy_workspace_test/pull/72
  - autolens_workspace_test#168: https://github.com/PyAutoLabs/autolens_workspace_test/pull/168
  - autolens_workspace#276: https://github.com/PyAutoLabs/autolens_workspace/pull/276
- workspace-seed: 19 advisory.yaml entries across 3 workspaces (autolens_workspace_test 9, autogalaxy_workspace_test 8, autolens_workspace 2), all .py-anchored + verified to match exactly one real script. autolens workspace conflict-claims (aggregator/epic) waived by human ("no conflict"). autofit_test + user autogalaxy skipped (no currently-running flakers; their named scripts already no_run-skipped e.g. agw#131 shapelets).
- corrective-red:
  - reason: release validation FAILED (stage integrate)
  - authorization: in-session human "go --auto" + explicit corrective-PR authorization 2026-07-14
  - scope: PR-open on Heart#75 + Build#153 + 3 workspace seeds only; no merge, no release. Other RED reason (PyAutoArray on feature/ticks-minus-in-math) is unrelated sibling, untouched — Heart stays RED.
- followup: (1) merge library-first (Build#153 → Heart#75 → workspace seeds), rerun mode=release, expect GREEN/YELLOW; (2) consider migrating recently-SLOW-no_run'd real-search entries → advisory to restore coverage (deliberate, tied to Profiling Agent); (3) pre-existing test_pre_build_skill manifest drift (admin_jammy vs PyAutoBrain) — separate hygiene fix.
- repos:
  - PyAutoHeart: feature/release-advisory-tier-slow-scripts
  - PyAutoBuild: feature/release-advisory-tier-slow-scripts
  - autogalaxy_workspace_test: feature/release-advisory-tier-slow-scripts
  - autolens_workspace_test: feature/release-advisory-tier-slow-scripts
  - autolens_workspace: feature/release-advisory-tier-slow-scripts

## inversion-testmode-singular-guard
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/388
- session: claude (start_dev/--auto 2026-07-14)
- status: awaiting-input
- worktree: ~/Code/PyAutoLabs-wt/inversion-testmode-singular-guard
- classification: library (PyAutoArray) — bug, supervised
- autonomy: supervised (--auto launched 2026-07-14; effective=supervised; plan written to issue #388; ship sign-off parks for human)
- question: https://github.com/PyAutoLabs/PyAutoArray/issues/388#issuecomment-4971520767
- local-commit: 48fae1ac on feature/inversion-testmode-singular-guard (implemented + tested, NOT pushed; resume /ship_library on sign-off)
- evidence: 4 raise-sites gated on is_test_mode() (2 inversion_util + 2 abstract log-det); +2 numpy unit tests; test_autoarray/inversion/ 233 passed
- note: test-mode-gate the singular/non-PD inversion crash (release tail FAILs slam.py + cpu_fast_modeling.py). Flaky TEST_MODE tail, NOT deterministic bug — real inference guarded by resample. Gate 4 inversion raise-sites on is_test_mode() to return benign dummies; NO conditioning floor (would perturb real numerics). Cross-ref PyAutoHeart#72, PyAutoLens#607.
- repos:
  - PyAutoArray: feature/inversion-testmode-singular-guard
