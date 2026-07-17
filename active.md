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


## autocti-assistant
- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/136
- session: claude (CLI, 2026-07-17)
- status: PHASE 0 MERGED 2026-07-17 — BIRTH UNBLOCKED. PyAutoBrain#137 (8db0c8e) + autolens_assistant#76 (dfa07b1) both merged; branches deleted, worktree removed, claims released (Phase 1 needs neither repo). VERIFIED ON CLEAN MAIN: clone PyAutoCTI --workspace autocti_workspace -> exit 0 / unclassified 0 (was exit 4 / 39); 39-file risk gone from Risks; check_boundary -> 'boundary complete, generic 53 / domain 295 / mixed 93'; 27 clone tests pass. The per-PR guard PROVED ITSELF IN CI: #76's boundary job went fail -> pass the moment #137 landed, and GRADED (not skipped). NEXT = PHASE 1 (birth the seed), BLOCKED ON THE HUMAN REPO-CREATION GATE (name/owner/visibility; default PyAutoLabs/autocti_assistant) — nothing is created before that answer. Then clone --apply --mode lightweight-seed -> born PRIVATE -> Heart legs 1-3 -> flip public -> register repos.yaml + repos_sync.py --write. Dry run confirms Ph1 output: ~146 copied + 388 PENDING, al_->ac_ correct
- autonomy: supervised
- prompt: active/build_autocti_assistant_from_reference_cell.md
- note: 5-phase epic (Ph0 unblock → Ph1 birth seed → Ph2 ac_* skills → Ph3 wiki+profile → Ph4 demos+validation), one PR each per the cti-resurrection phase0..phase5 precedent. Clone mode = lightweight-seed, FORCED not preferred (_clone.py gates --apply on it; exact-clone/differentiated-sibling are v2/unimplemented, exit 5). Repo creation = HUMAN GATE (default PyAutoLabs/autocti_assistant); user answered PUBLIC — but PyAutoBuild/autobuild/clone_seed.py births PRIVATE and flips public only after Heart legs 1-3 (PyAutoHeart/docs/newborn_validation.md); end state IS public, so the privacy seam STAYS IN FORCE: PyAutoMemory wiki/cti consulted for pointers/structure only, NEVER copied. wiki/cti is THIN (1 concept / 2 entities / 8 sources) = bibliography pointer, not a corpus — Ph3 is real research. Intake trap: PyAutoCTI is a CONSUMED DEPENDENCY, not an edit target — epic filed on PyAutoBrain per the pyautoscientist-3b-clone (PyAutoBrain#73) clone-epic precedent. Ground every skill against the 118 validated autocti_workspace/scripts/, never API memory. al_→ac_ prefix falls out of _clone.py's pkg[0]+pkg[4] heuristic (autocti[4]=='c') — verified correct. PHASE 0 FINDINGS (corrections to the approved plan, both recorded on #136): (a) the guard MOVED REPOS — PyAutoBrain has 10+ test files and NO CI that runs pytest at all, so a guard there would never fire; it now runs in autolens_assistant CI where the drift originates. The "PyAutoBrain test suite never runs in CI" gap is UNFILED and worth its own hygiene prompt. (b) .mcp.json is GENERIC not mixed (it only wires autoassistant.mcp, already generic tooling) — the plan guessed mixed; reading it corrected that. (c) docs drift was SIX places not two, incl. skills/clone/SKILL.md whose description ("analysis-only and must not generate files") is what a session reads BEFORE invoking /clone. (d) a newborn INHERITS clone-boundary.yml via .github/* generic → check_boundary skips when the repo has no profile, else every newborn's first CI run would fail.
- library-pr: PyAutoBrain#137 + autolens_assistant#76 — BOTH MERGED 2026-07-17 (Phase 0)
- repos:

## potential-correction-uv-campaign
- issue: https://github.com/PyAutoLabs/PyAutoLens/issues/627
- session: claude (CLI, 2026-07-17)
- status: workspace-dev (research campaign)
- worktree: ~/Code/PyAutoLabs-wt/potential-correction-uv-campaign
- autonomy: supervised
- prompt: active/potential_correction_realistic_uv_campaign.md
- note: Phase A COMPLETE (harness pushed to feature/potential-correction-uv-campaign, NOT PR'd). SDP.81 ABSENT on RAL (prep job 330605 install failed silently - jax-joss resume item) -> ALMA-like synthesis uv instead. LOCAL-TIER RESULTS on #627: one-shot CERTIFIED (corr 0.83 / 0.72 local, peak 0.14 arcsec, 6.2 sigma; evidence max = best recovery at Matern c=2e3); iterative failure mode CHARACTERIZED - the source block absorbs the perturbation (result insensitive to 1000x dpsi-reg sweep, chi2/dof 0.59 over-fit); evidence self-protects (iterative < one-shot in ALL configs). RESUME Phase B (RAL leg): mid/full tiers with --use-jax (uniform joint-coefficient grid RULED OUT locally 2026-07-17 - stiff source breaks the regime gate, evidence collapses; table+verdict on #627; sc=1/c=2e3 one-shot remains evidence max) + engine enhancement candidate = per-iteration evidence re-optimization of regs (Koopmans/Vegetti). (IterDpsiSrcInvInterferometerAnalysis + search); consider per-iteration reg re-optimization (Koopmans/Vegetti) as an engine enhancement; RAL needs mirror refresh (12 merges today) + nohup/setsid/sentinel + precision-operator cache. Then Phase C = interferometer section in ws guides/advanced/potential_correction.py.
- repos:
  - autolens_workspace_developer: feature/potential-correction-uv-campaign
