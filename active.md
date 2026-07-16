# Active Tasks


## delete-pyautoheart-shim
- issue: https://github.com/PyAutoLabs/PyAutoHeart/issues/80
- library-pr: https://github.com/PyAutoLabs/PyAutoHeart/pull/81 (pending-release)
- status: library-shipped, awaiting-merge
- heart-ack: PyAutoLens: 1 uncommitted source change(s); workspace validation not passing (3 failed, 2026-07-09T09-48-30Z); 58 stale parked script(s); install verification not run; release validation stale: source moved since rehearsal (PyAutoConf, PyAutoFit, PyAutoArray, PyAutoGalaxy, PyAutoLens)
- worktree: ~/Code/PyAutoLabs-wt/delete-pyautoheart-shim
- autonomy: supervised
- prompt: active/delete_pyautoheart_shim.md
- note: human overrode the heart-state-clobber repo-claim block ("go"); moot anyway — its PR #79 merged before this branch was cut from origin/main (0319c1a includes it). No file overlap (heart/checks/ vs pyautoheart/+pyproject.toml).
- repos:
  - PyAutoHeart: feature/delete-pyautoheart-shim

## coolest-standard-support
- issue: https://github.com/PyAutoLabs/PyAutoLens/issues/612
- session: claude --resume 5c96151b-044f-49e4-aa35-e01ceb863124
- status: library-dev
- worktree: ~/Code/PyAutoLabs-wt/coolest-standard-support
- autonomy: supervised
- prompt: active/coolest_standard_support.md
- note: follow-up prompt draft/feature/autolens/coolest_powerlaw_herculens_parity.md stays in draft until this ships
- repos:
  - PyAutoGalaxy: feature/coolest-standard-support
  - PyAutoLens: feature/coolest-standard-support

## community-voice-agent
- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/119
- status: library-dev
- worktree: ~/Code/PyAutoLabs-wt/community-voice-agent
- autonomy: human-required
- prompt: active/community_communication_agent_listen_and_respond.md
- note: birth the community conductor — alias changed "the Voice"→"the Ears" (workspace-agent #118 shipped as the Voice; Broca=workspace speaks, Wernicke=community hears). Includes /wake_up community sensory leg. Watch: ic50-assistant-seed also claims PyAutoBrain (clone/ only, no expected overlap).
- repos:
  - PyAutoBrain: feature/community-voice-agent


## ic50-assistant-seed
- issue: https://github.com/Jammy2211/ic50_assistant/issues/1
- status: in-progress — Phase 1 (seed) shipped; PRs open; Phases 2-5 pending
- worktree: ~/Code/PyAutoLabs-wt/ic50-assistant-seed
- autonomy: supervised
- prompt: active/build_ic50_assistant_from_autofit_assistant.md
- note: build ic50_assistant (PyAutoFit domain assistant, EP/graphical IC50) seeded from autofit_assistant. Phase 1 generalised the Clone Agent (reference profiles) — PyAutoBrain#120 + autofit_assistant#11 — and birthed PRIVATE Jammy2211/ic50_assistant (birth c3487afc1). PyAutoBrain claimed by workspace-agent; this is a small parallel PR, no file overlap (clone/ only), user-approved. Phases 2-5 (IC50 wiki+papers, ic50_* demo skills, RAL/HPC, validation) checkpoint before start. Downstream: ic50_workspace → closed science-project repo.
- repos:
  - PyAutoBrain: feature/ic50-assistant-seed
  - autofit_assistant: feature/ic50-assistant-seed
  - ic50_assistant: main (born via clone_seed)


## assistant-euclid-mode
- issue: https://github.com/PyAutoLabs/autolens_assistant/issues/73
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/assistant-euclid-mode
- autonomy: supervised
- prompt: active/extend_autolens_assistant_with_a_euclid_mode.md
- note: 3 phases, one PR each — P0 pipeline cleanup (profiling/+skills/ removal), P1 euclid_* skills, P2 wiki/euclid/ literature wiki; euclid_assistant is read-only bib source, NOT claimed
- repos:
  - autolens_assistant: feature/assistant-euclid-mode
  - euclid_strong_lens_modeling_pipeline: feature/assistant-euclid-mode


## viz-render-gallery
- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/117
- session: claude --resume 4a4bf99d-519c-4acc-9ac7-036e2850c56f
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/viz-render-gallery
- autonomy: supervised
- prompt: active/visualization_eyes_agent.md
- parent: eyes-agent epic (#117, Phase 1 of 3; Phase 2 blocked by workspace-agent's PyAutoBrain claim)
- repos:
  - autolens_workspace_test: feature/viz-render-gallery

## memory-structure-cleanup
- issue: https://github.com/PyAutoLabs/PyAutoMemory/issues/24
- status: PRs open, awaiting merge — Memory#25 (restructure) -> Mind#82 (template sync) + Brain#121 (faculty glob, parallel-PR exception); design note posted on #24
- worktree: ~/Code/PyAutoLabs-wt/memory-structure-cleanup
- autonomy: supervised
- prompt: active/pyautomemory_structure_cleanup.md
- note: PyAutoBrain leg (memory-faculty glob) is a small parallel PR from main — repo claimed by workspace-agent, parallel PR user-approved 2026-07-16 (no file overlap); PyAutoBrain deliberately NOT claimed here
- repos:
  - PyAutoMemory: feature/memory-structure-cleanup
  - PyAutoMind: feature/memory-structure-cleanup

## pre-build-audit
- issue: https://github.com/PyAutoLabs/PyAutoBuild/issues/156
- status: library-dev (research — audit + design doc; edits behind plan approval)
- worktree: ~/Code/PyAutoLabs-wt/pre-build-audit
- autonomy: supervised
- prompt: active/pre_build_git_add_failure_audit.md
- parent: build-chain-umbrella (Phase 1, epic PyAutoBuild#155)
- repos:
  - PyAutoBuild: feature/pre-build-audit

## build-chain-umbrella
- issue: https://github.com/PyAutoLabs/PyAutoBuild/issues/155
- status: coordinating — epic over 6 phases; Phase 0a MERGED (PyAutoHeart#79, 2026-07-16), Phase 0b blocked (PyAutoBrain claimed ×2), Phase 1 (pre_build audit) next
- prompt: active/build_chain_umbrella.md (full decomposition)
- autonomy: supervised
- repos:


## slope-hierarchy
- issue: https://github.com/Jammy2211/slope_hierarchy/issues/1
- status: workspace-dev — Phase 1 scaffold DONE (private repo born, commit 1c595ba); next: Phase 1 simulator
- worktree: /mnt/c/Users/Jammy/Science/slope_hierarchy (external science project on its own main — no PyAutoLabs worktree; ic50_workspace-style non-standard)
- autonomy: supervised
- prompt: active/ep_hierarchical_power_law_slopes.md
- note: hierarchical power-law slope recovery from N simulated imaging lenses — BlackJAX-NUTS joint fit vs EP parity (values AND errors), RAL scale-up, and end-to-end exercise of the 2026-07 EP diagnostics (PyAutoFit#1330 wave). PyAutoFit is exercised NOT edited: EP defects file as new bug prompts via intake. No PyAutoLabs repo claimed.
- repos:

## pixelized-gradient-experiment
- issue: https://github.com/PyAutoLabs/autolens_workspace_developer/issues/100
- status: in-progress — A100 pipeline WORKING. Gradient question SETTLED (yes). Search question OPEN. Nautilus baseline job 330379 running on RAL (submitted 2026-07-15, 4h limit).
- worktree: ~/Code/PyAutoLabs-wt/pixelized-gradient-experiment (autolens_workspace_developer on feature/pixelized-gradient-experiment, pushed, NOT PR'd)
- autonomy: supervised (research)
- SETTLED: pix likelihoods ARE gradient-differentiable. A100 FD probe (kernel-CDF RectangularKernelAdaptDensity(bandwidth=0.1), os_pix=1, x64): every mass/shear param FD-matched ~1e-6 (einstein_radius rel=8.8e-7), logL +25537 at a truth-centred point. My earlier "no" was a methodology error (human caught it). NEVER use adaptive meshes at os_pix=1 (certified staircase = dead mass gradient); kernel-CDF is live at os_pix=1, adaptive needs os_pix=4.
- SHIPPED: PyAutoFit#1374 batch_size (merged 7262f832) — unbatched pix multi-start OOMs 80GB A100 (58.13 GiB jvp fusion); batch_size=4 completed a full f64 fit. Do NOT use fp32 (science compromise) or apply_sparse_operator (human: separate question, may slow the likelihood).
- OPEN (the real question): adam ran ONCE — wall 2090s, max logL -39888, einstein_radius 1.4169 (truth 1.6), per-start basin 0/16. "IN TRUTH BASIN: True" is an ARTIFACT of a slack 0.3 tol — do not trust it. logL -39888 vs the probe's +25537 at truth = the optimizer did NOT find the basin. Suspects: n_steps=300 too few from broad starts; lr=1e-2 mis-scaled; my per-start diagnostic indexing may be wrong.
- resume: (1) read Nautilus 330379 result (/mnt/ral/jnightin/pixgrad_logs/samp_pixgrad_nautilus_330379.log) — if Nautilus ALSO misses the basin, the model/priors are at fault, not the gradient optimizer; (2) then debug adam (steps/lr/diagnostics); (3) then adabelief + lion. Only adam has run — no ADABelief/Lion/Nautilus results yet.
- RAL: shared /mnt/ral/jnightin/PyAuto/PyAutoFit left CLEAN on main (human's release version-bumps in README/docs/paper preserved). My isolated PyAutoFit worktree /mnt/ral/jnightin/pixgrad_pyautofit (batch_size branch, now merged to main) is PYTHONPATH-prepended by the sbatch and still used by job 330379 — safe to delete once it finishes, then the shared mirror on main suffices.
- TRAPS: foreground `timeout ssh` does NOT kill the remote side (it severed a git op, leaving a stale index.lock + half-applied checkout in the SHARED mirror) — use nohup+setsid+sentinel. Nautilus on a JAX row MUST set force_x1_cpu=True + use_jax_vmap=True (else fork corrupts JAX state) and n_batch<=16 without the sparse operator (default 100 needs ~100GB).
- intakes filed: draft/feature/autolens_profiling/jax_compile_time_profiling.md (Fable, tomorrow — compile is ~all the wall time; autotune RULED OUT: 2100s vs 2090s identical), draft/refactor/autofit/split_fitness_batch_size_lh_vs_latent.md
- repos:
  - autolens_workspace_developer: feature/pixelized-gradient-experiment

## retire-complete-ledger
- issue: https://github.com/PyAutoLabs/PyAutoMind/issues/81
- session: claude --resume 863c9a43-47ad-4b84-a27a-1a5e47a5bf64
- status: library-dev
- worktree: ~/Code/PyAutoLabs-wt/retire-complete-ledger
- autonomy: supervised
- prompt: active/retire_the_legacy_pyautomind_complete_md_ledger.md
- note: PARALLEL claims user-approved 2026-07-16 (overlap verified before start) — Mind also claimed by memory-structure-cleanup (their Mind diff = scripts/spawn.py only; spawn.py EXCLUDED from this branch, filed as 1-line rider on #81); Brain also claimed by community-voice-agent + ic50-assistant-seed (zero file overlap with this branch's file set); Heart also claimed by delete-pyautoheart-shim (no commits yet; this branch touches only skills/pyauto-status/reference.md there)
- repos:
  - PyAutoMind: feature/retire-complete-ledger
  - PyAutoBrain: feature/retire-complete-ledger
  - PyAutoHeart: feature/retire-complete-ledger
