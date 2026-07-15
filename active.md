# Active Tasks

## wire-verify-install-leg
- issue: https://github.com/PyAutoLabs/PyAutoHeart/issues/76
- status: PR OPEN https://github.com/PyAutoLabs/PyAutoHeart/pull/77 — awaiting human merge (release cap = human-required). 276 tests pass, CI green 3.12+3.13. New tests verified failing on unfixed source; leg proven to flip both directions via the real CI sequence.
- worktree: ~/Code/PyAutoLabs-wt/wire-verify-install-leg (PyAutoHeart on feature/wire-verify-install-leg)
- autonomy: human-required (effective) — launched --auto, but work-type `release` caps at human-required (AUTONOMY.md:56); min(safe, human-required) = human-required, so --auto changed nothing. Plan approved by human 2026-07-15. Run ends at PR-open; merge/close stay human.
- goal: Stage 3 runs verify_install A-E against the TestPyPI wheels and passes, but the result is never ingested, so readiness reports "install verification not run" — one of 3 legs holding Heart at YELLOW 70. Verified on main 2026-07-15: ~/.pyauto-heart/verify_install.json ABSENT; validation_report.json from the real release run ingested fine (integrate pass, 543p/0f) with zero verify_install trace. Discard point = validate.py:563-569, sidecar read ONLY in the fail direction; a PASS contributes nothing.
- design: carry `index` (testpypi|pypi) in the sidecar; embed it in the stage report; `validate --ingest` persists it to HEART_STATE_DIR/verify_install.json (the file readiness already reads); readiness names the index in its reason so a TestPyPI pass never reads as proof a PyPI install works. Human decided 2026-07-15: accept testpypi evidence for this leg, WITH provenance recorded.
- out of scope (prompt says follow-ups, not this task): ops re-run of weekly mode=smoke to refresh the stale test_run leg; hygiene triage of 58 stale parked no_run scripts.
- repos:
  - PyAutoHeart: feature/wire-verify-install-leg


## pixelized-gradient-experiment
- issue: https://github.com/PyAutoLabs/autolens_workspace_developer/issues/100
- status: in-progress, PAUSED for bedtime 2026-07-14 — feasibility ANSWERED (pix gradients DO work; certified test imaging_pixelization.py passed exit 0). RESUME = build the sampler experiment on the CORRECT config.
- worktree: ~/Code/PyAutoLabs-wt/pixelized-gradient-experiment (autolens_workspace_developer on feature/pixelized-gradient-experiment; probes + pix_gradient_findings.md committed+pushed, NOT PR'd)
- autonomy: supervised (research)
- finding: can af.MultiStartAdam/ADABelief/Lion work for a pixelized source? YES — pix likelihoods are gradient-differentiable. My first probe's "no" was a methodology error (human caught it; certified in autolens_workspace_test/scripts/jax_grad/imaging_pixelization.py, re-run passed). Correct config = kernel-CDF mesh RectangularKernelAdaptDensity(bandwidth=0.1) [os_pix=1] OR adaptive mesh at over_sample_size_pixelization=4; truth-centred GaussianPriors; small FD step sweep near truth.
- resume: STEP 1 DONE-ish — searches_minimal/probe_grad_pix.py REWRITTEN to the certified recipe (commit 227c4c0): kernel-CDF mesh, explicit over_sample_size_pixelization, SLaM-pix-1 model (MGE linear light geometry FIXED at truth, free Isothermal+shear, free reg), truth-centred GaussianPriors + small FD step sweep (1e-8..1e-6) near truth. Truth from jax_profiling/simulators/imaging.py: einstein_radius=1.6, centre=(0,0), q=0.9/45deg, shear=(0.05,0.05). BUT NOT YET RUN TO A VERDICT — local CPU is too slow (kernel-CDF pixelized JAX x64 ~10min+ compile then ~40 FD evals); runs were terminated. NEXT: (1) run the probe on GPU/A100 (or shrink mask/mesh) → expect OK; (2) build the sampler experiment on that objective and run af.MultiStartAdam/ADABelief/Lion + af.Nautilus baseline; (3) A100 on RAL. REAL question = can multi-start gradient descent from BROAD starts recover the mass basin vs Nautilus (gradient correctness is settled=yes, certified test passes). See [[project_pixelized_gradient_sampler_infeasible]] memory.
- note: broad multi-starts are the crux — the certified gradients are validated NEAR TRUTH; the samplers deliberately start broad, where the pixelized landscape may be pathological. That tension is the experiment's actual finding to measure.
- repos:
  - autolens_workspace_developer: feature/pixelized-gradient-experiment


