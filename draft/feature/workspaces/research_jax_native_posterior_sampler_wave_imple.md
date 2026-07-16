# Research: JAX-native posterior sampler wave — implement and benchmark the

Type: feature
Target: workspaces
Repos:
- autolens_workspace_developer
Difficulty: large
Autonomy: supervised
Priority: normal
Status: formalised

Research: JAX-native posterior sampler wave — implement and benchmark the ranked sampler shortlist from the 2026-07-16 deep-research session on the standard searches_minimal problem in @autolens_workspace_developer, via the sampler_pipeline ingest-prototype-profile-promote flow. Ranked stages: (a) blackjax adaptive tempered SMC upgraded to a gradient inner kernel (MALA/HMC + inner_kernel_tuning; extends the existing blackjax_smc.py RWM smoke script; gives logZ from tempering increments), (b) ChEES-HMC many-chain adaptation (cheapest first-class addition; vmap-friendly fixed-length trajectories vs NUTS variable-length trees), (c) MCLMC + adjusted MCLMC warm-started from the multi-start Adam basin, paired with harmonic (learned harmonic mean) for evidence, (d) flowMC (normalizing-flow global jumps; multimodality insurance), (e) jaxns cameo (independent GPU-native nested-sampling cross-check vs Nautilus; inversion-heavy vmap OOM caution applies, NSS history). Constraints from prior campaigns: reverse-mode-only gradients, NaN-gradient degenerate points need masking, vmap fan-out needs lax.map batch_size tiling (Fit#1374 lever), RAL A100 float32. Deliverable per stage: findings doc + benchmark vs Nautilus baseline. Issue stages one at a time as predecessors ship — do not bulk-issue.

<!-- formalised by the Intake (Conception) Agent on 2026-07-16 from user-intake -->
