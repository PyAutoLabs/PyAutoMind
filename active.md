# Active Tasks


## pixelized-gradient-experiment
- issue: https://github.com/PyAutoLabs/autolens_workspace_developer/issues/100
- status: in-progress, PAUSED for bedtime 2026-07-14 — feasibility ANSWERED (pix gradients DO work; certified test imaging_pixelization.py passed exit 0). RESUME = build the sampler experiment on the CORRECT config.
- worktree: ~/Code/PyAutoLabs-wt/pixelized-gradient-experiment (autolens_workspace_developer on feature/pixelized-gradient-experiment; probes + pix_gradient_findings.md committed+pushed, NOT PR'd)
- autonomy: supervised (research)
- finding: can af.MultiStartAdam/ADABelief/Lion work for a pixelized source? YES — pix likelihoods are gradient-differentiable. My first probe's "no" was a methodology error (human caught it; certified in autolens_workspace_test/scripts/jax_grad/imaging_pixelization.py, re-run passed). Correct config = kernel-CDF mesh RectangularKernelAdaptDensity(bandwidth=0.1) [os_pix=1] OR adaptive mesh at over_sample_size_pixelization=4; truth-centred GaussianPriors; small FD step sweep near truth.
- resume: (1) rewrite searches_minimal/probe_grad_pix.py to certified recipe (kernel-CDF + truth-centred priors + small-step FD near truth) → confirm OK; (2) build SLaM-pix-1 objective (fixed MGE lens light, free Isothermal+shear, kernel-CDF source) and run af.MultiStartAdam/ADABelief/Lion + af.Nautilus baseline locally; (3) A100 on RAL. REAL question = can multi-start gradient descent from BROAD starts recover the mass basin vs Nautilus (gradient correctness settled=yes). See [[project_pixelized_gradient_sampler_infeasible]] memory.
- repos:
  - autolens_workspace_developer: feature/pixelized-gradient-experiment


