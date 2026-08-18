# JAX-native posterior sampler wave — ranked shortlist from the 2026-07-16 deep-research session — SUPERSEDED 2026-08-18

> **SUPERSEDED / SHELVED 2026-08-18.** Removed from the registry (was
> `parked.md :: blackjax-smc-gradient-kernel`, issue
> [autolens_workspace_developer#113](https://github.com/PyAutoLabs/autolens_workspace_developer/issues/113))
> — the wave as scoped here is superseded by the 2026-08-17 human-approved
> inference programme (`active/inference_programme_ledger.md`, autolens_profiling#134),
> which owns sampler direction going forward. Stage (a) shipped its findings;
> stages (b) ChEES-HMC, (c) MCLMC+harmonic, (d) flowMC, (e) jaxns were never
> issued and are not carried forward as-is.
>
> **Preserved parked context (from the deleted `parked.md` entry):** stage (a)
> POSITIVE — warm-started gradient SMC SAMPLES (acc 0.80->0.17 across tempering,
> `einstein_radius` 1.5998 vs truth 1.6, max logL ~31781 vs Prodigy MLE
> 31787.93). Parked 2026-07-24 to clear the deck for the autolens_profiling
> refactor. All work PRESERVED on pushed branch
> `feature/blackjax-smc-gradient-kernel` (origin autolens_workspace_developer,
> tip `6867762`); local worktree removed. Full write-up:
> `searches_minimal/smc_gradient_findings.md` on that branch. Science memory:
> `project_gradient_smc_warm_start_sampler_wave`. Gradient path certified
> OK_HMC_VIABLE (`probe_grad.py`); baseline `nss_grad` row = logZ -31.47. Open
> resume threads at park time: RAL job 331058
> (`/mnt/ral/jnightin/smc_grad_logs/smc_warm_ok-331058.out`, 3 warm arms @128p);
> logZ (~31690-31798) vs Nautilus comparison row; A100 rep-timing;
> `warm_start.json` is a regenerable cache (re-`--refresh` if it predates the
> `cov` field). MGE only; pix deferred.


Type: research
Target: autolens_workspace_developer
Repos:
- autolens_workspace_developer
Difficulty: large
Autonomy: supervised
Priority: normal
Status: formalised

Research: JAX-native posterior sampler wave — implement and benchmark the ranked sampler shortlist from the 2026-07-16 deep-research session on the standard searches_minimal problem in @autolens_workspace_developer, via the sampler_pipeline ingest-prototype-profile-promote flow. Ranked stages: (a) blackjax adaptive tempered SMC upgraded to a gradient inner kernel (MALA/HMC + inner_kernel_tuning; extends the existing blackjax_smc.py RWM smoke script; gives logZ from tempering increments), (b) ChEES-HMC many-chain adaptation (cheapest first-class addition; vmap-friendly fixed-length trajectories vs NUTS variable-length trees), (c) MCLMC + adjusted MCLMC warm-started from the multi-start Adam basin, paired with harmonic (learned harmonic mean) for evidence, (d) flowMC (normalizing-flow global jumps; multimodality insurance), (e) jaxns cameo (independent GPU-native nested-sampling cross-check vs Nautilus; inversion-heavy vmap OOM caution applies, NSS history). Constraints from prior campaigns: reverse-mode-only gradients, NaN-gradient degenerate points need masking, vmap fan-out needs lax.map batch_size tiling (Fit#1374 lever), RAL A100 float32. Deliverable per stage: findings doc + benchmark vs Nautilus baseline. Issue stages one at a time as predecessors ship — do not bulk-issue.

<!-- formalised by the Intake (Conception) Agent on 2026-07-16 from user-intake -->
