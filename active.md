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


## env-scrubbed-baseline
- issue: https://github.com/PyAutoLabs/PyAutoBuild/issues/161 (migration step 3; epic #155)
- status: library-dev — scrubbed base env (deny managed keys, not allowlist — safer deviation from doc §5)
- worktree: ~/Code/PyAutoLabs-wt/env-scrubbed-baseline
- autonomy: supervised
- repos:
  - PyAutoBuild: feature/env-scrubbed-baseline

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
- status: ALL 4 PHASES MERGED (autocti_assistant#4=1337a68); EPIC SUBSTANTIVELY COMPLETE, awaiting only the HUMAN PUBLIC-FLIP decision — repo confirmed still PRIVATE — PyAutoLabs/autocti_assistant PRIVATE. Ph0-3 MERGED. PHASE 4 = 4 runnable demonstrations in scripts/demonstrations/, ALL RAN FOR REAL against live stack + RECOVER input traps: demo1 1D calibrate (density 0.13→0.1323, release 1.25→1.261), demo2 2D charge-injection (0.13→0.1334, 1.25→1.312), demo3 correct (trail 3.9x suppressed), demo4 aggregator round-trip. COLD SMOKE (leg4 proxy) PASSES: install Q → ac_setup_environment arcticpy recipe, calibration Q → ac_fit_cti_model+wiki; de-lensed llms.txt front door (was 'strong-lens science'/'explain lensing'). All 5 audit checks green. DEMO TRAPS: (a) factor-graph fits store results PER-FACTOR — aggregator max_log_likelihood_instance is None, use samples.max_log_likelihood()[0].cti (CTIAgg assumes single-analysis layout); (b) demo2 first version 2 noisy levels recovered density but NOT release timescale (1.25→2.90) — fixed the DATA (3 clean levels + n_live 60), not the assertion. REMAINING LEAK: scripts/AGENTS.md still lensing SLaM content (needs CTI-pipeline rewrite; flagged on #136 with the systemic boundary finding). PUBLISH: legs 1-4 substantively done; FINAL PUBLIC FLIP LEFT FOR EXPLICIT HUMAN APPROVAL (not done). NEXT = merge #4, then human decides on flip public + repo visibility
- autonomy: supervised
- prompt: active/build_autocti_assistant_from_reference_cell.md
- note: 5-phase epic (Ph0 unblock → Ph1 birth seed → Ph2 ac_* skills → Ph3 wiki+profile → Ph4 demos+validation), one PR each per the cti-resurrection phase0..phase5 precedent. Clone mode = lightweight-seed, FORCED not preferred (_clone.py gates --apply on it; exact-clone/differentiated-sibling are v2/unimplemented, exit 5). Repo creation = HUMAN GATE (default PyAutoLabs/autocti_assistant); user answered PUBLIC — but PyAutoBuild/autobuild/clone_seed.py births PRIVATE and flips public only after Heart legs 1-3 (PyAutoHeart/docs/newborn_validation.md); end state IS public, so the privacy seam STAYS IN FORCE: PyAutoMemory wiki/cti consulted for pointers/structure only, NEVER copied. wiki/cti is THIN (1 concept / 2 entities / 8 sources) = bibliography pointer, not a corpus — Ph3 is real research. Intake trap: PyAutoCTI is a CONSUMED DEPENDENCY, not an edit target — epic filed on PyAutoBrain per the pyautoscientist-3b-clone (PyAutoBrain#73) clone-epic precedent. Ground every skill against the 118 validated autocti_workspace/scripts/, never API memory. al_→ac_ prefix falls out of _clone.py's pkg[0]+pkg[4] heuristic (autocti[4]=='c') — verified correct. PHASE 0 FINDINGS (corrections to the approved plan, both recorded on #136): (a) the guard MOVED REPOS — PyAutoBrain has 10+ test files and NO CI that runs pytest at all, so a guard there would never fire; it now runs in autolens_assistant CI where the drift originates. The "PyAutoBrain test suite never runs in CI" gap is UNFILED and worth its own hygiene prompt. (b) .mcp.json is GENERIC not mixed (it only wires autoassistant.mcp, already generic tooling) — the plan guessed mixed; reading it corrected that. (c) docs drift was SIX places not two, incl. skills/clone/SKILL.md whose description ("analysis-only and must not generate files") is what a session reads BEFORE invoking /clone. (d) a newborn INHERITS clone-boundary.yml via .github/* generic → check_boundary skips when the repo has no profile, else every newborn's first CI run would fail.
- library-pr: PyAutoBrain#137 + autolens_assistant#76 — BOTH MERGED 2026-07-17 (Phase 0)
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
