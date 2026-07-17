# Active Tasks


## cti-resurrection-phase5
- issue: https://github.com/PyAutoLabs/autocti_workspace_test/issues/1
- session: claude (CLI, 2026-07-17)
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/cti-resurrection-phase5
- autonomy: supervised
- prompt: active/cti_resurrection_phase5_wst_and_release_wiring.md
- note: FINAL phase of the CTI resurrection epic (0-4 merged). workspace_test rebuild (preserve Euclid tvac/temporal heritage as legacy/), curated smoke list (exclude TM2 assertion-tie scripts), Heart+Build registration, notebook regeneration. Release itself stays human/nightly.
- repos:
  - autocti_workspace_test: feature/cti-resurrection-phase5
  - autocti_workspace: feature/cti-resurrection-phase5
  - PyAutoHeart: feature/cti-resurrection-phase5
  - PyAutoBuild: feature/cti-resurrection-phase5

## pix-nonfinite-localisation
- issue: https://github.com/PyAutoLabs/autolens_workspace_developer/issues/104
- session: claude (CLI, 2026-07-17)
- status: awaiting-merge — PHASE 1 SHIPPED. Ship sign-off + both scope questions answered by the human 2026-07-17 (all 3 recommendations taken). Heart RED acked contemporaneously (5 pre-existing unrelated reasons; RED reason verbatim = "PyAutoLens: 1 uncommitted source change(s)" — a stray paper_jax/paper.md edit in the main checkout, untouched by this branch). Merge + issue close remain HUMAN.
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace_developer/pull/105 (pending-release, MERGEABLE; 3 commits, 2 files, +669 additive; tests n/a no test dir, smoke n/a additive searches_minimal/ only)
- question: https://github.com/PyAutoLabs/autolens_workspace_developer/issues/104#issuecomment-5003011602 (ANSWERED)
- follow-ups-filed: draft/bug/autoarray/reg_matrix_logdet_nonfinite_fix.md (phase 2 — MUST open with the reduced-matrix spectrum dump before choosing a fix; science-visible, needs evidence parity) + draft/bug/autofit/fitness_where_guard_nan_gradient.md (the resample guard does not protect gradient consumers — higher leverage, hits every jax.grad consumer of every likelihood). Both are DRAFTS not issues — /start_dev each when ready (no bulk-issuing).
- result: THE SITE = AbstractInversion.log_det_regularization_matrix_term (autoarray/inversion/inversion/abstract.py:734-764), log(diag(cholesky(H))) of the reduced reg matrix — FIRST non-finite in BOTH forward and backward walks, culprit param = the regularization coefficient. EXONERATES the 3 other suspects incl. the prime one (curvature-reg cholesky abstract.py:719 is FINITE 1.69e4 — F+H is better conditioned than bare H), the NNLS Jacobi preconditioner (d in [3.2e-2,1.4e4], no zero diag) and the kernel-CDF weight-map normalise. BOTH death classes (in-basin r_E=1.28 AND out-of-basin r_E=5.93) die at the SAME site => one bug; the in/out-of-basin triage does NOT split the fix and no invalid-space penalty verdict is needed. Evidence: RAL A100 jobs 330609/330611 (261-306s); findings in searches_minimal/pix_nonfinite_findings.md.
- mechanism: H = lam^2*L + 1e-8*I (constant.py:43-58), L = graph Laplacian (PSD, exact constant null mode); the 1e-8 lift is ABSOLUTE not scaled to lam => eig_min pinned at 1e-8, eig_max ~ lam^2*degree, cond ~ lam^2*1e8. Confirmed vs the real library fn (eig_min == 1e-8 across 4 decades; at lam=1e5 eig_min goes NEGATIVE -9.9e-6 -> numpy RAISES, JAX NaNs). OPEN QUESTION for phase 2: synthetic clean grid only fails at lam>=3e4 but the real fit died at lam~6.9e3 — numpy-vs-JAX divergence RULED OUT (tested, they agree exactly), so the real REDUCED matrix is worse-conditioned than a regular grid. Dump its spectrum BEFORE choosing a fix. Candidates: the 20 unregularized MGE amplitudes in the 920x920 reduction; isolated/disconnected mesh pixels adding null modes; unique_indices=True in the scatter at constant.py:55-58.
- second-bug-found: autofit/non_linear/fitness.py:239-240 — xp.where(isnan(ll), resample, ll) repairs the VALUE (rejects report loss=inf not nan) but reverse-mode AD differentiates the masked branch: 0*NaN = NaN. The resample guard does NOT protect gradient consumers AT ALL. Explains #101's silent deaths + apply_if_finite latching. PyAutoFit not PyAutoArray — file separately (double-where / safe-x). Arguably higher leverage than the autoarray fix: hits EVERY jax.grad consumer of ANY likelihood.
- traps: will NOT run locally — one point's value_and_grad needs 10.90 GiB (laptop OOM'd on CPU at 9.3GB RSS and on its 6GB GPU); use the RAL A100 (probe_nonfinite.sbatch, --partition=gpu --mem=64gb). The recorded death points reproduce NOTHING (pix_lr_free.py:206-208 stores LAST-FINITE params); use the seed-0 rejected draws (draws 12 + 35 of 90). The #101 finite-loss/NaN-grad class is NOT yet reproduced (90 draws gave only non-finite-loss rejects) — still open.
- worktree: ~/Code/PyAutoLabs-wt/pix-nonfinite-localisation
- autonomy: supervised (--auto launch; effective = min(header supervised, bug cap supervised))
- prompt: active/pixelized_likelihood_nonfinite_regions.md
- note: Phase 1 = LOCALISE ONLY (diagnosis, no library edits) per the Brain Bug Agent's investigate-first verdict. Stagewise finite-probe over the #101 pixelized objective to name WHICH intermediate goes non-finite. Phase 2 (the PyAutoArray fix) files as its own issue once the site is named. Two planning corrections: (1) pix_lr_free.py records LAST-FINITE params, not the NaN-producing ones — the cheap reproduction is the step-0 broad draws with finite loss + NaN grad that pix_lr_free.py:124-130 silently rejects; (2) 13/16 deaths are at r_E 2.6-6.4 vs truth 1.6 (the "arcs miss the mesh" garbage regime) — only starts 2 (r_E 1.36) and 12 (r_E 1.43) die near the Nautilus mode 1.31, and those in-basin deaths are the real bug candidates. Candidate sites ranked in the issue: abstract.py:719/:754 (JAX cholesky returns NaN not raises), inversion_util.py:333-335 (NNLS Jacobi 1/sqrt(diag)), rectangular_kernel.py:123 (0/0 weight-map normalise). Run local GPU first (~/venv/PyAutoGPU, warm compile cache), RAL A100 only for trajectory replay. PyAutoLens NOT claimed (conflict w/ potential-correction-port; not in the likelihood path anyway).
- repos:
  - autolens_workspace_developer: feature/pix-nonfinite-localisation


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
- status: ALL PHASES COMPLETE 2026-07-16 (16+ merged PRs; 3 refusal mechanisms live incl. guard v1.1; epic #155 = remaining-queue tracker: Ph3 steps 2-8, Ph4 four tasks, Ph2 satellites, Ph5 items 3-6)
- prompt: active/build_chain_umbrella.md (full decomposition)
- autonomy: supervised
- repos:


## slope-hierarchy
- issue: https://github.com/Jammy2211/slope_hierarchy/issues/1
- status: workspace-dev — goals 1/3/4 DELIVERED; goal 2 BLOCKED on upstream fix. EP collapse ROOT-CAUSED 2026-07-17: Result.projected_model feeds LINEAR samples.weight_list into AbstractMessage.project which requires LOG weights (exp(w-max) ≈ uniform ⇒ canonical-space boundary attractor ⇒ cavity poisoned ⇒ honest sigma-collapse; damping irrelevant — δ=0.5 job 330532 collapsed identically; probe 330591 proved fit RIGHT 2.0448 / projection WRONG 2.9875±0.011). Bug prompt: draft/bug/autofit/ep_projection_linear_weights_as_log.md (next action = /start_dev it). After the fix merges: clear output/<sample>/ep on RAL, rerun submit_ep, parity table, then N=25-50 scale-up
- worktree: /mnt/c/Users/Jammy/Science/slope_hierarchy (external science project on its own main — no PyAutoLabs worktree; ic50_workspace-style non-standard)
- autonomy: supervised
- prompt: active/ep_hierarchical_power_law_slopes.md
- resume: (1) read damped-EP job 330532 (submitted 2026-07-16 ~18:00, delta=0.5, 12h limit): `ssh euclid_jump "grep -A3 'Parent recovery' /mnt/ral/jnightin/slope_hierarchy/hpc/batch_gpu/output/output.330532_0.out"` + its ep_diagnostics.results (did damping cure the F10 collapse?); (2) scp results/ep_sample_n5_seed42_delta0.5.json back; (3) build the goal-2 parity table EP-vs-NUTS (NUTS numbers in results/graphical_nuts_sample_n5_seed42.json) and post to issue #1; (4) if parity holds → scale-up sample (N=25-50, new simulate + resubmit chain; remember output-clear + truth-file force-sync traps); if collapse persists → try delta 0.2-0.3 or per-factor sampler optimisers per the F10 hint
- note: hierarchical power-law slope recovery from N simulated imaging lenses — BlackJAX-NUTS joint fit vs EP parity (values AND errors), RAL scale-up, and end-to-end exercise of the 2026-07 EP diagnostics (PyAutoFit#1330 wave). PyAutoFit is exercised NOT edited: EP defects file as new bug prompts via intake. No PyAutoLabs repo claimed.
- repos:

## potential-correction-port
- issue: https://github.com/PyAutoLabs/PyAutoLens/issues/618
- session: claude (CLI, 2026-07-17)
- status: phases 1-4 ALL MERGED 2026-07-17 (Array#390, Galaxy#505, Lens#621+#622); library legs cleaned. NOW: Phase 5 = iterative-bug hunt vs Vegetti Nat.Astron. papers (leads on #618) + Phase 6 = workspace layers (autolens_workspace guide + autolens_workspace_test incl. jax_likelihood_functions tier + golden parity vs tar demo) — ws repos claimed
- worktree: ~/Code/PyAutoLabs-wt/potential-correction-port
- autonomy: supervised
- prompt: active/potential_correction_port.md
- library-pr: ALL MERGED — Array#390 · Galaxy#505 · Lens#621 · Lens#622 (Heart RED acked throughout — 5 pre-existing unrelated reasons)
- note: port caoxiaoyue/lensing_potential_correction (gravitational imaging: joint source+dpsi evidence inversion) into the stack; cite caoxiaoyue/potential_correction_paper (Cao et al. 2025). Phase 1 = PyAutoArray (masked-grid diff operators, curvature/4th-order mask regs, coarse-mesh itp matrix — reuse existing kernel regs). Phases 2 (PyAutoGalaxy Input* mass profiles + GRF) and 3 (autolens/potential_correction subpackage) QUEUED behind slam-resume-fastpath's PyAutoGalaxy+PyAutoLens claims — claim those repos here only after it ships. NumPy/numba only; JAX port is a known follow-up. No GPy/multiprocess/powerbox/numba-scipy deps.
- repos:
  - autolens_workspace: feature/potential-correction-port
  - autolens_workspace_test: feature/potential-correction-port


