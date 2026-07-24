# Parked tasks

Tasks that were started or scoped but are not currently in flight. Listed
here so they remain visible across machines instead of disappearing into
unindexed worktrees or stashes. Move an entry back to `active.md` (or to
`planned.md` if re-scoping is needed) when work resumes; on shipping,
write the dated `complete/<YYYY>/<MM>/<slug>.md` record instead.

## interferometer-delaunay-flaky-fitexception
- issue: https://github.com/PyAutoLabs/PyAutoLens/issues/640
- status: PHASE 1 COMPLETE (merged) — Phase 1a PyAutoFit#1408 MERGED (TEST_MODE=2 bypass tolerates single-eval FitException = resample-to-reject sentinel -1e99, mirrors fitness.py:256; +2 tests) + Phase 1b autolens_workspace#311 MERGED (un-park interferometer Delaunay + add to smoke; CI green 3.12+3.13). User-facing flake RESOLVED (now tolerated). Worktree removed, branches deleted. REMAINING = Phase 2 ONLY (not claimed): fix the underlying NaN/non-PD producer in PyAutoArray so the fit is CORRECT not merely tolerated — candidates: fnnls.py:134 divide-by-zero (45/250 local draws hit it) and/or degenerate Hilbert-mesh vertices in source_pix_2 (the failing stage). HARD: flake is CI-thread-dependent, not locally reproducible (250 Overlay-stage draws clean); needs source_pix_2 Hilbert-stage repro. NON-URGENT (Phase 1 made it non-fatal).
- worktree: none (Phase 1 shipped+cleaned; Phase 2 will claim PyAutoArray fresh)
- autonomy: supervised
- prompt: active/interferometer_delaunay_intermittent_qhull_nan.md
- note: follow-up to Delaunay cleanup #301/#307 (imaging Delaunay shipped green + smoke-gated; interferometer parked). Consolidates closed autolens_workspace#300/#308/#309. Phase 1 test-mode tolerance helps ALL FitException-prone pixelization scripts, not just this one. Complements PyAutoLens#639 raise_fit_exception (preserves cause).
- repos:
  - PyAutoFit: feature/interferometer-delaunay-flaky-fitexception (Phase 1a SHIPPED #1408)
  - autolens_workspace: feature/interferometer-delaunay-flaky-fitexception (Phase 1b pending)
  - PyAutoLens (not claimed — re-scoped out; issue #640 lives here)
  - PyAutoArray (Phase 2, not yet claimed)

## blackjax-smc-gradient-kernel
- issue: https://github.com/PyAutoLabs/autolens_workspace_developer/issues/113
- status: PARKED 2026-07-24 — stage (a) POSITIVE: warm-started gradient SMC SAMPLES (acc 0.80->0.17 across tempering, einstein_radius 1.5998 vs truth 1.6, max logL ~31781 vs Prodigy MLE 31787.93). Parked to clear the deck for the autolens_profiling refactor (scripts live in autolens_workspace_developer/searches_minimal/, which the refactor churns). All work PRESERVED on pushed branch feature/blackjax-smc-gradient-kernel (origin autolens_workspace_developer, tip 6867762); local worktree removed. Full write-up: searches_minimal/smc_gradient_findings.md on that branch. Science memory: project_gradient_smc_warm_start_sampler_wave. RESUME AFTER REFACTOR: (1) check RAL job 331058 (/mnt/ral/jnightin/smc_grad_logs/smc_warm_ok-331058.out) — 3 warm arms @128p (MALA auto-step, MALA+--tune, HMC): does --tune HOLD acceptance ~0.57 as lambda->1 (fixed step decays 0.80->0.17)? does HMC beat MALA? (2) compare logZ (~31690-31798) vs Nautilus, write comparison.txt row; (3) A100 rep-timing (GPUs full at park); (4) stage (b) ChEES-HMC reusing _warm_start. warm_start.json is a regenerable cache — re-`--refresh` if it predates the cov field (else silent diagonal fallback). MGE only; pix deferred.
- worktree: none (pushed to origin; local worktree removed 2026-07-24)
- autonomy: supervised
- prompt: active/jax_native_posterior_sampler_wave.md
- note: WAVE TRACKER — this parks the whole JAX-native posterior sampler wave (stages b ChEES-HMC, c MCLMC+harmonic, d flowMC, e jaxns still remain). Do NOT move the prompt to complete/ — stage (a) shipped its findings but the wave continues as a separate run after the refactor. Gradient path certified OK_HMC_VIABLE (probe_grad.py); baseline nss_grad row = logZ -31.47.
- repos:
  - autolens_workspace_developer: feature/blackjax-smc-gradient-kernel (pushed, tip 6867762)

## group4-mge-search-benchmark
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/82
- parked: 2026-07-24 — code + first GPU results MERGED (PR #83); worktree/claim RELEASED
- remaining: gradient-family sweep (prodigy/lion/adabelief/prodigy_autoconv) + Nautilus anchor on laptop GPU (~/venv/PyAutoGPU, JAX_PLATFORM_NAME=cuda JAX_PLATFORMS=cuda,cpu XLA_PYTHON_CLIENT_MEM_FRACTION=0.5, --config-name local_gpu_fp64), then recovery/walltime aggregation. Warm output preserved in main checkout output/searches/.
- note: RESUME FROM NEW PATHS once the scripts/<dataset>/<task>/ restructure lands — group4 cells move to scripts/cluster/ (human taxonomy decision). If compile still too heavy: dial _GROUP4_MGE_TOTAL_GAUSSIANS 10->6 and/or _MULTI_START_N_STARTS 64->32.

