# Active Tasks


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
- status: library-dev
- worktree: ~/Code/PyAutoLabs-wt/memory-structure-cleanup
- autonomy: supervised
- prompt: active/pyautomemory_structure_cleanup.md
- note: PyAutoBrain leg (memory-faculty glob) is a small parallel PR from main — repo claimed by workspace-agent, parallel PR user-approved 2026-07-16 (no file overlap); PyAutoBrain deliberately NOT claimed here
- repos:
  - PyAutoMemory: feature/memory-structure-cleanup
  - PyAutoMind: feature/memory-structure-cleanup

## build-chain-umbrella
- issue: https://github.com/PyAutoLabs/PyAutoBuild/issues/155
- status: coordinating — epic over 6 phases; Phase 0a (heart-state-clobber) in flight, Phase 0b blocked (PyAutoBrain claimed ×2), Phases 1-5 issued sequentially as predecessors ship
- prompt: active/build_chain_umbrella.md (full decomposition)
- autonomy: supervised
- repos:

## heart-state-clobber
- issue: https://github.com/PyAutoLabs/PyAutoHeart/issues/78
- status: library-dev
- worktree: ~/Code/PyAutoLabs-wt/heart-state-clobber
- autonomy: supervised
- parent: build-chain-umbrella (Phase 0a)
- repos:
  - PyAutoHeart: feature/heart-state-clobber

## workspace-agent
- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/116
- status: library-dev
- worktree: ~/Code/PyAutoLabs-wt/workspace-agent
- autonomy: supervised
- repos:
  - PyAutoBrain: feature/workspace-agent

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
