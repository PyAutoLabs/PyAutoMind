# Active Tasks

## pix-inversion-not-positive-definite
- issue: https://github.com/PyAutoLabs/autogalaxy_workspace/issues/140
- status: workspace-dev — reproduce imaging pix case on clean main (real data) to confirm raise site = reg log-det term, then opt 3 pix scripts into log_det_method="slogdet" (opt-in; default cholesky UNCHANGED per pix-NaN decision). MGE likelihood_function "matrix singular" is DISTINCT (no reg → singular linear solve): characterise separately, config-fix or file bug/autoarray follow-up. Clean 2 stale HowToGalaxy no_run markers (features/ scripts don't exist).
- worktree: ~/Code/PyAutoLabs-wt/pix-inversion-not-positive-definite
- autonomy: supervised
- prompt: active/pixelization_inversion_not_positive_definite.md
- note: tail of pix-NaN lineage (PyAutoArray#391/#392 shipped opt-in slogdet). Scripts use GaussianKernel reg, not Constant/Adapt — reproduction must confirm site. Real surface = 3 pix scripts + 1 MGE + 2 stale-marker deletions, not "6 scripts".
- repos:
  - autogalaxy_workspace
  - HowToGalaxy


## jax-joss-benchmarks
- issue: https://github.com/PyAutoLabs/autolens_workspace/issues/281
- status: PARKED-ON-JOB — #282 MERGED+cleaned; 8/8 runnable A100 rows committed (autolens_jax_joss@64204f6). SDP.81 prep = detached RAL job 330608 (330605 diagnosed: empty extracted/ leftover skipped untar via test-d guard; casatools import needs ~/.casa/data — both fixed; 42GB tarball CACHED, no re-download) (45GB ALMA Band6 download -> casatools venv -> 3-level export -> installs dataset/interferometer/{sdp81,sdp81_mid,sdp81_full} in /mnt/ral/jnightin/autolens_jax_joss). RESUME (short session): (1) check log /mnt/ral/jnightin/sdp81_prep_330608.log — expect 'SDP81 PREP ALL DONE' + per-level visibility counts; failure modes: casatools pip wheel on py3.12 (fallback = monolithic CASA tarball), datacolumn, MS_LIST empty (check find patterns); (2) sbatch interferometry benchmarks on A100: benchmarks/interferometer.py at --nvis default/mid/full + benchmarks/imaging_and_interferometer.py (pattern: /mnt/ral/jnightin/autolens_jax_joss/run_rest.sbatch); (3) scp results/*.json back, regen RESULTS.md, commit (guard: explicit file paths); (4) copy small sdp81/ product locally, rewrite scripts/interferometer/start_here.py on NEW branch (start_workspace; #282 merged) using it — decide hosting (commit few-MB FITS to workspace w/ .gitignore allowlist + git add -f, or Zenodo+SDP81_URL); (5) final issue #281 update. Also pending: cluster-tuning prompt draft/feature/autolens_workspace/joss_cluster_benchmark_tuning.md; weak JAX-viz PyAutoLens#614
- worktree: ~/Code/PyAutoLabs-wt/jax-joss-benchmarks
- autonomy: supervised
- prompt: active/autolens_jax_joss_benchmark_repo.md
- note: 5-phase epic (one-shot attempt per user); new repo autolens_jax_joss (PyAutoLabs, public) born alongside; datasets SDP.81 / RXJ1131 / A2744 user-approved
- repos:
  - autolens_jax_joss: main (born this task)






## build-chain-umbrella
- issue: https://github.com/PyAutoLabs/PyAutoBuild/issues/155
- status: coordinating — Phases 0,1,2,5 + Ph3 steps1-3 + Ph4 task1 DONE (~40 PRs); REMAINING queued as 5 draft prompts indexed in active/build_chain_umbrella.md (pick via /feature): version_skew rework NEXT, then version-consumers, HowTo sim, env-profile steps4-8, guard v1.3
- prompt: active/build_chain_umbrella.md (full decomposition)
- autonomy: supervised
- repos:


## slope-hierarchy
- issue: https://github.com/Jammy2211/slope_hierarchy/issues/1
- status: workspace-dev — ALL 4 GOALS ANSWERED. G1 NUTS ✓ (mean 2.028/sigma 0.143). G3 RAL pipeline ✓. G4 diagnostics ✓✓ (caught+fixed real projection bug, PR PyAutoFit#1383 MERGED). G2 = characterised partial parity: EP recovers parent MEAN (2.051, agrees NUTS) but converged SCATTER ~4× low (0.026 vs truth 0.1/NUTS 0.143), errors ~1000× too tight — documented EP scale-hyperparameter shrinkage (max_steps=5 snapshot 0.004 was under-converged; job 330639 max_steps=12 converged to 0.026, plateaued). NEXT (optional): N=25-50 scale-up (NUTS headline, EP cautionary) OR write-up. Not blocked.
- worktree: /mnt/c/Users/Jammy/Science/slope_hierarchy (external science project on its own main — no PyAutoLabs worktree; ic50_workspace-style non-standard)
- autonomy: supervised
- prompt: active/ep_hierarchical_power_law_slopes.md
- next: goal-2 fully answered; remaining is scale-up (N=25-50: edit simulator N + submit_* --array, rm output/<sample>/* before refits, force-sync truth files, verify RAL PyAutoFit mirror commit) or a methods write-up. NOTE repo now on autonerves (autoconf renamed, PRs #2/#3 landed 2026-07-18).
- note: hierarchical power-law slope recovery from N simulated imaging lenses — BlackJAX-NUTS joint fit vs EP parity (values AND errors), RAL scale-up, and end-to-end exercise of the 2026-07 EP diagnostics (PyAutoFit#1330 wave). PyAutoFit is exercised NOT edited: EP defects file as new bug prompts via intake. No PyAutoLabs repo claimed.
- repos:


## pix-gradient-slogdet-revalidation
- issue: https://github.com/PyAutoLabs/autolens_workspace_developer/issues/112
- status: workspace-dev — A100 JOB QUEUED-BUT-GPU-STARVED (330921, submitted 2026-07-20, still PENDING(Priority) after 2h+). BLOCKER: gpu partition has 2 A100 nodes but ONE is down* ("Not responding", indefinite) and the live node's 4 A100s are all held by user c4072114's multi-day jobs (2-3d TIME_LEFT, end 2026-07-23/24). SLURM est. my START ~2026-07-23 19:53 (~3 days). Not mine, cannot cancel; short-walltime backfill won't help (no gap frees for days). Job will run whenever a GPU frees — no action needed to keep it queued. RESUME (poll): Toggle committed (a5b53a6) + A/B sbatch (6461935) on feature/pix-gradient-slogdet-revalidation (local-only, NOT pushed). RAL PyAutoArray synced to PR#392 (had to repair a corrupt origin/main ref: rm .git locks + git update-ref -d refs/remotes/origin/main + fetch --prune; PR392=7 now). Harness scp'd to /mnt/ral/jnightin/autolens_workspace_developer/searches_minimal/. RESUME: (1) `ssh -o IdentitiesOnly=yes euclid_jump "sacct -j 330921 --format=JobID,State,Elapsed -X; tail -80 /mnt/ral/jnightin/pixgrad_logs/pix_slogdet_ab-330921.out"`; (2) A/B verdict = compare the two arms' "Collected X/N starts (from T draws)" (step-0 acceptance) + per-start "died after step N" reports — cholesky baseline died ~25-50, slogdet should survive to step 299; (3) verdict into searches_minimal/pix_nonfinite_findings.md → ship_workspace. Launch env: activate.sh BASE=/mnt/ral/jnightin/PyAuto, al.Settings=aa.Settings so PyAutoArray sync alone suffices.
- worktree: ~/Code/PyAutoLabs-wt/pix-gradient-slogdet-revalidation
- autonomy: supervised
- prompt: active/pix_gradient_landscape_revalidation.md
- note: verification tail of the pix-NaN lineage — localisation (#104/PR#105) + fix (PyAutoArray#392) + fitness-guard contract (PyAutoFit#1391) all shipped 2026-07-17. Toggle is env var PIX_LOGDET=slogdet threaded via al.Settings into build_analysis (one edit covers both pix_multi_start + pix_lr_free). Repro is A100-only (10.9 GiB/point OOMs laptop).
- repos:
  - autolens_workspace_developer: feature/pix-gradient-slogdet-revalidation (worktree live; commit a5b53a6 local-only)


## slam-adapt-inversion-cascade
- issue: https://github.com/PyAutoLabs/autolens_workspace/issues/300
- session: claude --resume 37395538-a051-4b8d-8eeb-aa3f8df67454
- status: workspace-dev — REPRODUCED on clean main (TEST_MODE=2). Two DISTINCT root causes (not one cluster): (1) double_einstein_ring imaging+group → adapt_data=None AttributeError at PyAutoArray inversion/mappers/abstract.py:476, phase source_pix[1]_source_1 (SAME both scripts); CONFIRMED real (not test-mode): reg_init=al.reg.Adapt but source_1 pixelized with NO adapt image possible (never had an LP phase, unlike source_0). FIX (approved): SEED source_1 an adapt image from current tracer lensed source model (NOT Constant-reg bootstrap). (2) imaging/features/pixelization/slam → DIAGNOSED (not test-mode, NOT the pix-not-PD cluster): script pairs RectangularAdaptImage mesh + al.reg.AdaptSplit (lines 482-483), but AdaptSplit/*Split reg is ONLY valid on irregular Delaunay/Voronoi meshes — sibling group/features/pixelization/slam.py:23,280 documents this rule explicitly. Mechanism: rectangular.py:310 _mappings_sizes_weights_split is a STUB returning non-split mappings; AdaptSplit.regularization_matrix_from derives pixels=len/4 assuming a real 4pt split-cross → wrong-sized reg matrix (210 vs 786 curvature) → TypeError add incompatible shapes at inversion/abstract.py:366. FIX (DECIDED by user): rectangular mesh → NO split, so swap reg al.reg.AdaptSplit → al.reg.Adapt in pixelization/slam.py (lines ~482-483 + docstrings @16,24,184 which claim "AdaptSplit instead of Adapt"). RULE: Delaunay-file → Split; rectangular → no-split. (Do NOT convert to Delaunay.) Optional lib follow-up (bug/autoarray): *Split reg should fail LOUDLY on non-splittable meshes, not produce a cryptic broadcast TypeError. Multi-wavelength SersicCore alpha=0 SPLIT OUT to draft/bug/autogalaxy/sersic_core_alpha_zero_division.md.
- worktree: ~/Code/PyAutoLabs-wt/slam-adapt-inversion-cascade
- autonomy: supervised
- prompt: active/slam_advanced_fitexception_cascade.md
- note: pixelization/slam mismatch is NOT the pix-inversion-not-positive-definite cluster (autogalaxy_workspace#140) — ruled out; it is a mesh+reg incompatibility (rectangular+AdaptSplit). HowToLens paths in orig prompt are STALE (no features/ layout — uses chapter_N; find real pixelization tutorial in phase 1).
- folded-in: Delaunay NEEDS_FIX cleanup (was #301, closed 2026-07-21). Verified GREEN on clean main — `imaging/features/pixelization/delaunay.py` (exit 0, FitException gone) + `interferometer/features/pixelization/delaunay.py` (exit 0, (2,2)v(1032,1032) broadcast gone) + HowToLens `chapter_4/tutorial_7` (exit 0). No PyAutoArray change. This task's PR set also: remove both delaunay entries from autolens_workspace no_run.yaml, remove the 2 dead delaunay entries from HowToLens no_run.yaml, add both delaunay scripts to autolens_workspace smoke_tests.txt. Details in prompt "Folded in" section.
- repos:
  - autolens_workspace: feature/slam-adapt-inversion-cascade
  - HowToLens: feature/slam-adapt-inversion-cascade






## interpolator-aggregator-test-mode
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1401
- status: library-dev — Phase 1 of the workspaces API-drift umbrella. Reproduced on clean main: interpolate.py:265 aggregator/DB section crashes IndexError "no instances" ONLY under test mode — searches write output/test_mode/<prefix> but Aggregator.from_directory reads hardcoded output/<prefix> → 0 results → empty LinearInterpolator. Fix (Option A, approved): make Aggregator.from_directory (autofit/aggregator/aggregator.py) test-mode-aware by reusing _test_mode_segment() (autofit/non_linear/paths/abstract.py) — fall through to the test_mode sibling only when the plain dir has no metadata and the sibling exists. Unit test under test_autofit/aggregator/. Then validate autofit_workspace interpolate.py under PYAUTO_TEST_MODE=1 + regen notebook. Ship library-first.
- worktree: ~/Code/PyAutoLabs-wt/interpolator-aggregator-test-mode
- autonomy: supervised
- prompt: draft/bug/workspaces/api_drift_callsite_fixes.md (INTERPOLATOR ITEM ONLY — umbrella stays in draft/; do NOT move to active/ or complete/ on ship; other 5 items become follow-up tasks)
- note: interpolate.py:213 in-memory interpolation WORKS; only the DB/aggregator section fails, only under test mode (real user runs fine). HowToFit tutorial_5 was paired in the umbrella but does NOT use interpolator/aggregator — EXCLUDED. interpolate.py not in smoke set; umbrella NEEDS_FIX markers no longer literally in files (curated list).
- repos:
  - PyAutoFit: feature/interpolator-aggregator-test-mode
  - autofit_workspace: (deferred — claimed for the ship_workspace follow-up after library merges)


## blackjax-smc-gradient-kernel
- issue: https://github.com/PyAutoLabs/autolens_workspace_developer/issues/113
- status: workspace-dev — stage (a) of the 5-stage JAX-native posterior sampler wave. Upgrade blackjax_smc.py from RWM (cube-space, pure_callback) to a GRADIENT inner kernel sampling in PHYSICAL space (differentiable; probe_grad.py form). MALA first, HMC behind a flag; blackjax.adaptive_tempered_smc + inner_kernel_tuning; JAX-native physical-space log_prior (Gaussian/Uniform/LogUniform); preserve SMC logZ. Deliverable = searches_minimal/blackjax_smc_grad.py + smc_gradient_findings.md + comparison.txt row. MGE parametric ONLY; pixelized deferred.
- worktree: ~/Code/PyAutoLabs-wt/blackjax-smc-gradient-kernel
- autonomy: supervised
- prompt: active/jax_native_posterior_sampler_wave.md
- note: WAVE TRACKER — stages (b) ChEES-HMC, (c) MCLMC+harmonic, (d) flowMC, (e) jaxns remain. Do NOT move prompt to complete/ on stage-(a) ship; issue next stage only as this one nears shipping (no bulk-issue). Concurrent worktree alongside parked pix-gradient-slogdet-revalidation claim (different files). Gradient path certified OK_HMC_VIABLE (probe_grad.py); baseline nss_grad row = logZ -31.47.
- repos:
  - autolens_workspace_developer
