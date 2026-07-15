# Active Tasks


## arxiv-digest-announcement-window
- issue: https://github.com/PyAutoLabs/PyAutoMind/issues/79
- status: awaiting-input — implemented + verified, parked at ship sign-off (supervised cap). Question on the issue: open the PR?, backfill scope (posts to #papers, so needs a go-ahead), band-vs-seen-ID design check.
- commit: 409f746 on feature/arxiv-digest-announcement-window (pushed, NOT PR'd)
- worktree: ~/Code/PyAutoLabs-wt/arxiv-digest-announcement-window (PyAutoMind on feature/arxiv-digest-announcement-window)
- autonomy: supervised (bug cap; prompt header said safe, min() → supervised)
- finding: #papers digest drops papers permanently. `arxiv_fetch.py` filters on `<published>` (v1 submission) within a rolling 24h/72h window, but the arXiv API only indexes papers at *announcement*, 1–3 days later. Confirmed: a 72h re-run returns both papers missed on 2026-07-15 (2607.12129, 2607.12209), so the keyword query is fine. Fix = anchor the window to arXiv's announcement bands (20:00 ET Sun–Thu; 14:00 ET Mon–Fri deadlines), computed via zoneinfo for DST.
- note: worktree used deliberately so PyAutoMind's main checkout stays on main — `prompt_sync_push` does `git add -A` on the current branch, so registry ops must not run from the feature branch.
- backfill: after merge, one `workflow_dispatch` with lookback_hours=168 to recover already-dropped papers.
- repos:
  - PyAutoMind: feature/arxiv-digest-announcement-window

## multistart-adam-release-jax
- issue: https://github.com/PyAutoLabs/autofit_workspace_test/issues/44
- status: awaiting-input — implemented + verified, parked at ship sign-off (supervised cap). Question on the issue.
- worktree: ~/Code/PyAutoLabs-wt/multistart-adam-release-jax (autofit_workspace_test on feature/multistart-adam-release-jax; edits NOT committed)
- autonomy: supervised (bug cap; launched --auto 2026-07-15)
- finding: nightly-release RED 5 nights = one shard, one cause. autofit_workspace_test/config/build/env_vars_release.yaml pins PYAUTO_DISABLE_JAX=1 + PYAUTO_TEST_MODE=0, so MultiStartAdam (JAX-native, hard-guards on analysis._use_jax) really runs and raises. NOT the perf-flake tail. Regression from the #43/PyAutoFit#1370 multi-start promotion.
- fix: 3 `set: {PYAUTO_DISABLE_JAX: "0"}` overrides in env_vars_release.yaml (MultiStartAdam + Dynesty_jax + Nautilus_jax, the latter two were passing VACUOUSLY on the numpy path) + 1 `unset: [PYAUTO_TEST_MODE, PYAUTO_DISABLE_JAX]` in env_vars.yaml (smoke) so the per-PR gate can catch this class at all.
- verified: all 3 scripts exit 0 with JAX on (MultiStartAdam recovers 50.156/25.196/9.858 vs truth 50/25/10); resolver driven over real configs — no substring over-match (Nautilus.py/DynestyStatic stay DISABLE_JAX=1).
- TRAP: two env profiles — env_vars.yaml is the per-PR SMOKE gate, env_vars_release.yaml is mode=release. Reading the wrong one yields a plausible-but-wrong fix. Smoke's TEST_MODE=2 bypasses the sampler before _fit, so smoke could never have caught this.
- repos:
  - autofit_workspace_test: feature/multistart-adam-release-jax


## pixelized-gradient-experiment
- issue: https://github.com/PyAutoLabs/autolens_workspace_developer/issues/100
- status: in-progress, PAUSED for bedtime 2026-07-14 — feasibility ANSWERED (pix gradients DO work; certified test imaging_pixelization.py passed exit 0). RESUME = build the sampler experiment on the CORRECT config.
- worktree: ~/Code/PyAutoLabs-wt/pixelized-gradient-experiment (autolens_workspace_developer on feature/pixelized-gradient-experiment; probes + pix_gradient_findings.md committed+pushed, NOT PR'd)
- autonomy: supervised (research)
- finding: can af.MultiStartAdam/ADABelief/Lion work for a pixelized source? YES — pix likelihoods are gradient-differentiable. My first probe's "no" was a methodology error (human caught it; certified in autolens_workspace_test/scripts/jax_grad/imaging_pixelization.py, re-run passed). Correct config = kernel-CDF mesh RectangularKernelAdaptDensity(bandwidth=0.1) [os_pix=1] OR adaptive mesh at over_sample_size_pixelization=4; truth-centred GaussianPriors; small FD step sweep near truth.
- resume: (1) rewrite searches_minimal/probe_grad_pix.py to certified recipe (kernel-CDF + truth-centred priors + small-step FD near truth) → confirm OK; (2) build SLaM-pix-1 objective (fixed MGE lens light, free Isothermal+shear, kernel-CDF source) and run af.MultiStartAdam/ADABelief/Lion + af.Nautilus baseline locally; (3) A100 on RAL. REAL question = can multi-start gradient descent from BROAD starts recover the mass basin vs Nautilus (gradient correctness settled=yes). See [[project_pixelized_gradient_sampler_infeasible]] memory.
- repos:
  - autolens_workspace_developer: feature/pixelized-gradient-experiment


