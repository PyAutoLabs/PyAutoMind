# Active Tasks


## gradient-safe-logdet
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/391
- session: claude (CLI, 2026-07-17)
- status: library-dev
- worktree: ~/Code/PyAutoLabs-wt/gradient-safe-logdet
- autonomy: supervised
- prompt: active/gradient_safe_logdet_settings_option.md
- note: The ONLY endorsed change from the reg-logdet adversarial-review verdict (do NOT change the default; C4 = current lam-dependence correct to machine precision). Add Settings.log_det_method (Optional->conf fallback, like use_positive_only_solver): default "cholesky" byte-identical; opt-in "slogdet" = finite where Cholesky NaNs, identical where PD, general incl. Adapt. Applies to BOTH log-det terms (reg AND curvature-reg) per human decision. Config key log_det_method:cholesky in autoarray/config/general.yaml + mirror into workspace configs. RELEASE GATE = byte-identical figure_of_merit at default. slogdet-finite-where-cholesky-NaN validated at #104 seed-0 draw 12/35 via the 30s LOCAL spectrum script (NOT the A100 — 10.9GiB was value_and_grad). JAX grad-finiteness assertion -> autogalaxy_workspace_test at ship (autolens_wst is claimed by dpie-lenstool-default).
- repos:

## jax-joss-benchmarks
- issue: https://github.com/PyAutoLabs/autolens_workspace/issues/281
- status: PARKED-ON-JOB — #282 MERGED+cleaned; 8/8 runnable A100 rows committed (autolens_jax_joss@64204f6). SDP.81 prep = detached RAL job 330608 (330605 diagnosed: empty extracted/ leftover skipped untar via test-d guard; casatools import needs ~/.casa/data — both fixed; 42GB tarball CACHED, no re-download) (45GB ALMA Band6 download -> casatools venv -> 3-level export -> installs dataset/interferometer/{sdp81,sdp81_mid,sdp81_full} in /mnt/ral/jnightin/autolens_jax_joss). RESUME (short session): (1) check log /mnt/ral/jnightin/sdp81_prep_330608.log — expect 'SDP81 PREP ALL DONE' + per-level visibility counts; failure modes: casatools pip wheel on py3.12 (fallback = monolithic CASA tarball), datacolumn, MS_LIST empty (check find patterns); (2) sbatch interferometry benchmarks on A100: benchmarks/interferometer.py at --nvis default/mid/full + benchmarks/imaging_and_interferometer.py (pattern: /mnt/ral/jnightin/autolens_jax_joss/run_rest.sbatch); (3) scp results/*.json back, regen RESULTS.md, commit (guard: explicit file paths); (4) copy small sdp81/ product locally, rewrite scripts/interferometer/start_here.py on NEW branch (start_workspace; #282 merged) using it — decide hosting (commit few-MB FITS to workspace w/ .gitignore allowlist + git add -f, or Zenodo+SDP81_URL); (5) final issue #281 update. Also pending: cluster-tuning prompt draft/feature/autolens_workspace/joss_cluster_benchmark_tuning.md; weak JAX-viz PyAutoLens#614
- worktree: ~/Code/PyAutoLabs-wt/jax-joss-benchmarks
- autonomy: supervised
- prompt: active/autolens_jax_joss_benchmark_repo.md
- note: 5-phase epic (one-shot attempt per user); new repo autolens_jax_joss (PyAutoLabs, public) born alongside; datasets SDP.81 / RXJ1131 / A2744 user-approved
- repos:
  - autolens_jax_joss: main (born this task)



## api-gate-clause-scope
- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/130 (Phase 5 item — F5 API-gate false positive)
- status: library-dev — clause-scope the API gate so a .py in a non-python clause isn't scanned
- worktree: ~/Code/PyAutoLabs-wt/api-gate-clause-scope
- autonomy: supervised
- repos:
  - autolens_assistant: feature/api-gate-clause-scope

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


## dpie-lenstool-default
- issue: https://github.com/PyAutoLabs/PyAutoGalaxy/issues/506
- session: claude (CLI, 2026-07-17)
- status: shipped, awaiting-merge — library PyAutoGalaxy#509 + workspace autolens_workspace#287 + autolens_workspace_test#179 (all pending-release; merge order library-first; Heart RED acked twice — 6 pre-existing unrelated reasons)
- library-pr: https://github.com/PyAutoLabs/PyAutoGalaxy/pull/509 (pending-release; 1003 tests passed; Heart RED acked — 6 pre-existing unrelated reasons)
- worktree: ~/Code/PyAutoLabs-wt/dpie-lenstool-default
- autonomy: supervised
- prompt: active/dpie_lenstool_default_parameterization.md
- audit: paper/convention audit COMPLETE 2026-07-17 (on #506 — conventions verified vs Eliasdottir07 App A / Bergamini19 / 6-leg parity script; swap is pure re-parameterization)
- note: swap dPIEMass/dPIEMassSph default to Lenstool-native parameterization (approved: internal variant → dPIEMassB0/dPIEMassB0Sph + from_b0 classmethod); workspace follow-up (autolens_workspace + autolens_workspace_test) absorbs lenstool-scaling-slam (SLaM PR3 of autolens_workspace#265)
- repos:
  - PyAutoGalaxy: feature/dpie-lenstool-default
  - autolens_workspace: feature/dpie-lenstool-default
  - autolens_workspace_test: feature/dpie-lenstool-default
