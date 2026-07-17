# Active Tasks



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


## potential-correction-interferometer
- issue: https://github.com/PyAutoLabs/PyAutoLens/issues/623
- session: claude (CLI, 2026-07-17)
- status: phases 1+2a SHIPPED — #624 MERGED (sparse-route joint fit), #625 OPEN (iterative LM engine + dpsi_mask arc restriction; awaiting merge). OPEN DEFECT diagnosed (comment on #623): InputPotential nearest-extrapolation outside an arc-restricted dpsi mesh scrambles the iterative re-trace — FIX NEXT: zero-fill extrapolation mode in ag.mp.InputPotential/LinearNDInterpolatorExt, then re-validate the held wst scripts (subhalo_recovery_interferometer.py drafted UNCOMMITTED in worktree; one-shot passes corr 0.35/0.13", iterative blocked on the fix)
- worktree: ~/Code/PyAutoLabs-wt/potential-correction-interferometer
- autonomy: supervised
- prompt: active/potential_correction_interferometer.md
- note: extend al.pc (potential corrections, #618) to Interferometer in visibility space. PRIORITY (user): the SPARSE-OPERATOR / w-tilde route — curvature blocks in real space ((D_s D_psi)^T (T^H C^-1 T) (D_s D_psi)), scales with n_pix not n_vis; dense transform_mapping_matrix route = small-n_vis parity reference only. Then iterative-engine dataset seam + analyses; workspace_test follow-up (jax_likelihood_functions/interferometer + interferometer subhalo_recovery). dense_util xp kernels unchanged. Cite Cao et al. 2025 throughout.
- repos:
  - PyAutoLens: feature/potential-correction-interferometer


## autocti-assistant
- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/136
- session: claude (CLI, 2026-07-17)
- status: library-dev — Phase 0 (unblock the birth) NOT STARTED. BLOCKER: `bin/pyauto-brain clone PyAutoCTI --workspace autocti_workspace --apply` hard-fails exit 4 ("unclassified reference files — fix the boundary before a birth") — 39 tracked files in autolens_assistant match no template-boundary pattern (skills/euclid_*.md + .claude/skills/euclid_*.md + wiki/euclid/**, paper/**, .mcp.json, scripts/*_cosmos_web_ring.py — ALL shipped AFTER the boundary was last written). This blocks EVERY future assistant birth, not just autocti. Phase 0 = classify all 39 in BOTH places that must agree (PyAutoBrain/agents/conductors/clone/_clone.py REFERENCE_PROFILES patterns + autolens_assistant/modes/maintainer.md "Assistant-as-template" prose, which OWNS the boundary) + add the missing guard test to PyAutoBrain/tests/test_clone_conductor.py (none exists today — that absence is why 3 separate features silently re-blocked births) + docs-drift rider (PyAutoBrain/AGENTS.md and agents/conductors/clone/AGENTS.md both still claim "analysis-only v0 … writes nothing"; --apply --mode lightweight-seed IS implemented and hands a plan to Build)
- worktree: ~/Code/PyAutoLabs-wt/autocti-assistant
- autonomy: supervised
- prompt: active/build_autocti_assistant_from_reference_cell.md
- note: 5-phase epic (Ph0 unblock → Ph1 birth seed → Ph2 ac_* skills → Ph3 wiki+profile → Ph4 demos+validation), one PR each per the cti-resurrection phase0..phase5 precedent. Clone mode = lightweight-seed, FORCED not preferred (_clone.py gates --apply on it; exact-clone/differentiated-sibling are v2/unimplemented, exit 5). Repo creation = HUMAN GATE (default PyAutoLabs/autocti_assistant); user answered PUBLIC — but PyAutoBuild/autobuild/clone_seed.py births PRIVATE and flips public only after Heart legs 1-3 (PyAutoHeart/docs/newborn_validation.md); end state IS public, so the privacy seam STAYS IN FORCE: PyAutoMemory wiki/cti consulted for pointers/structure only, NEVER copied. wiki/cti is THIN (1 concept / 2 entities / 8 sources) = bibliography pointer, not a corpus — Ph3 is real research. Intake trap: PyAutoCTI is a CONSUMED DEPENDENCY, not an edit target — epic filed on PyAutoBrain per the pyautoscientist-3b-clone (PyAutoBrain#73) clone-epic precedent. Ground every skill against the 118 validated autocti_workspace/scripts/, never API memory. al_→ac_ prefix falls out of _clone.py's pkg[0]+pkg[4] heuristic (autocti[4]=='c') — verified correct.
- repos:
  - PyAutoBrain: feature/autocti-assistant
  - autolens_assistant: feature/autocti-assistant
