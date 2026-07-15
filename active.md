# Active Tasks


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


## pyautolens-assistant-joss-paper
- issue: https://github.com/PyAutoLabs/autolens_assistant/issues/69
- status: awaiting-merge — PR open, not merged
- workspace-pr: https://github.com/PyAutoLabs/autolens_assistant/pull/71
- worktree: ~/Code/PyAutoLabs-wt/pyautolens-assistant-joss-paper
- autonomy: supervised (docs)
- heart-ack: shipped at Heart YELLOW score 55 (no RED), author-acknowledged 2026-07-15. Acknowledged reasons, verbatim: "workspace validation not passing (3 failed, 2026-07-09T09-48-30Z)"; "58 stale parked script(s)". Both pre-date the branch and are unrelated to this docs-only change; the ack never extends to new reasons.
- note: unblocked 2026-07-15 — the blocking benchmark-calibration task (autolens_assistant#59) is closed. Scaffolds `autolens_assistant/paper/` (paper.md, paper.bib, README.md, .gitignore), mirroring the `PyAutoLens/paper_jax/` sibling. Consolidates the author's four drafted sections out of the prompt file and into the manuscript.
- decisions: benchmark section reframed to "three representative examples" (repo ships 4 prompts incl. hard_group_multi; author chose reframe over adding a 4th paragraph). Author block mirrors the JAX paper (sole corresponding author).
- open: benchmarks/RESULTS.md records ZERO runs for all 4 benchmarks, so benchmark-results prose stays future-tense; report real results before submission.
- repos:
  - autolens_assistant: feature/pyautolens-assistant-joss-paper


