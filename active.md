# Active Tasks


## fitness-nan-guard-contract
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1391
- session: claude (CLI, 2026-07-17)
- status: ALL 3 PRs OPEN, awaiting-merge — LIBRARY-FIRST GATE: merge PyAutoFit#1392 BEFORE autofit_workspace_test#53 and autolens_workspace_developer#106
- workspace-prs: https://github.com/PyAutoLabs/autofit_workspace_test/pull/53 (the 6-assertion contract script; all pass on CPU in seconds) + https://github.com/PyAutoLabs/autolens_workspace_developer/pull/106 (corrects the 2 disproved claims that shipped in #105)
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1392 (pending-release, MERGEABLE; docstring+comment only, NO behaviour change, NO API change; pytest 1499 passed/1 skipped = no delta; Heart RED acked contemporaneously — same 5 pre-existing unrelated reasons as #105, RED verbatim "PyAutoLens: 1 uncommitted source change(s)")
- worktree: ~/Code/PyAutoLabs-wt/fitness-nan-guard-contract
- autonomy: supervised
- prompt: active/fitness_where_guard_nan_gradient.md
- note: Fallout from the #104 pix-NaN localisation. Fitness.call:238-240's xp.where NaN guard repairs the VALUE (#104 rejects report loss=inf not nan) but NOT the gradient (0*NaN=NaN). Human decision 2026-07-17: CONTRACT + TEST, NO CODE FIX — because the investigation PROVED Fitness.call is structurally incapable of fixing it (see below). 3 repos: PyAutoFit (docstring only, no behaviour change) + autofit_workspace_test (scripts/jax_assertions/fitness_nan_gradient_contract.py, mirror the sibling fitness_dispatch.py) + autolens_workspace_developer (correct searches_minimal/pix_nonfinite_findings.md, which shipped in #105 carrying 2 disproved claims).
- established: (1) The trap is NARROWER than "guard never protects gradients" — it fires only when the masked branch's DERIVATIVE is non-finite. sqrt(x<0) and cholesky(non-PD) NaN their derivative => fires. log(x<0) is NaN in value but d/dx=1/x stays finite => 0*-1=0, NO trap. (2) An OUTPUT-side double-where DOES NOT FIX IT (measured: current grad=nan, output-side double-where grad=nan, input-side safe-x grad=0.0) — by the time Fitness.call sees log_likelihood the NaN derivative is ALREADY ON THE TAPE. (3) => the fix CANNOT live in Fitness.call; it belongs at each NaN source (for pix: draft/bug/autoarray/reg_matrix_logdet_nonfinite_fix.md). Repro is ~20 lines of CPU JAX — NO A100 (an earlier draft of the prompt wrongly demanded the #104 probe, ~11 GiB).
- out-of-scope: search-level gradient sanitiser where(isfinite(g),g,0) — fabricates a zero gradient at invalid points; #101 showed apply_if_finite latches. Restart/resample is the principled response (draft/feature/autofit/multistart_resurrection_and_contrib_rules.md).
- repos:
  - PyAutoFit: feature/fitness-nan-guard-contract
  - autofit_workspace_test: feature/fitness-nan-guard-contract
  - autolens_workspace_developer: feature/fitness-nan-guard-contract

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

