# Active Tasks

## lenscalc-adaptive-hessian-step
- issue: https://github.com/PyAutoLabs/PyAutoGalaxy/issues/591
- prompt: active/lenscalc_numpy_hessian_step_is_too_coarse.md
- issued: 2026-08-29
- status: library-dev
- worktree: ~/Code/PyAutoLabs-wt/lenscalc-adaptive-hessian-step
- classification: library (PyAutoGalaxy fix + tests; PyAutoLens test-only follow-up PR merged after)
- heart-ack: YELLOW acknowledged 2026-08-29 — "workspace validation not passing (0 failed, 1 timeout, cloud#33229145647: autolens_test scripts/multi_dataset/delaunay_mge.py)"; "release validation incomplete: no rehearsal for current source"
- repos:
  - PyAutoGalaxy: feature/lenscalc-adaptive-hessian-step
  - PyAutoLens: feature/lenscalc-adaptive-hessian-step
- next-skill: /ship_library

## multi-galaxy-scaling-zero-intensity
- issue: https://github.com/PyAutoLabs/autolens_workspace/issues/518
- prompt: active/multi_galaxy_scaling_relation_zero_intensity_under_smoke.md
- issued: 2026-08-29
- status: workspace-shipped, awaiting-merge (gate PASSED; park removed)
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace/pull/519
- worktree: ~/Code/PyAutoLabs-wt/multi-galaxy-scaling-zero-intensity
- classification: workspace (autolens_workspace only; simulator geometry + slam guard; un-park on a passing gate)
- heart-ack: YELLOW acknowledged 2026-08-29 — "workspace validation not passing (0 failed, 1 timeout, cloud#33229145647: autolens_test scripts/multi_dataset/delaunay_mge.py)"; "release validation incomplete: no rehearsal for current source"
- repos:
  - autolens_workspace: feature/multi-galaxy-scaling-zero-intensity
- next-skill: /prm

## fitness-log-likelihood-ceiling
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1543
- prompt: active/fitness_log_likelihood_ceiling.md
- issued: 2026-08-29
- status: library-shipped, awaiting-merge
- worktree: ~/Code/PyAutoLabs-wt/fitness-log-likelihood-ceiling
- classification: library (PyAutoFit only; Fitness magnitude guard + NSS closure, wave A1)
- heart-ack: YELLOW acknowledged 2026-08-29 — "workspace validation not passing (0 failed, 1 timeout, cloud#33229145647: autolens_test scripts/multi_dataset/delaunay_mge.py)"; "release validation incomplete: no rehearsal for current source"
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1545
- repos:
  - PyAutoFit: feature/fitness-log-likelihood-ceiling
- next-skill: /prm (library-shipped, awaiting-merge)

## blackjax-smc-search
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1544
- prompt: active/blackjax_smc_search.md
- issued: 2026-08-29
- status: library-dev
- worktree: ~/Code/PyAutoLabs-wt/blackjax-smc-search
- classification: library (PyAutoFit only; af.SMC blackjax adaptive tempered SMC, wave A2)
- repos:
  - PyAutoFit: feature/blackjax-smc-search
- next-skill: /ship_library

## euclid-ci-test-mode
- issue: https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/issues/45
- prompt: active/ci_test_mode_simulated_datasets_latents.md
- issued: 2026-08-29
- session: claude --resume 3ff83ca2-99bf-4ef9-bc56-d22ee835c306
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/euclid-ci-test-mode
- classification: workspace (euclid_strong_lens_modeling_pipeline only; PyAutoLens read-only reference)
- epic: euclid-dr1-prep (phase 2 of 10; gates nothing hard, strongly preferred before phase 4)
- repos:
  - euclid_strong_lens_modeling_pipeline: feature/euclid-ci-test-mode
- next-skill: /ship_workspace (stages A → B → C → D in flight)

## adapt-linear-regularization
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/511
- prompt: active/adapt_linear_regularization.md
- issued: 2026-08-29
- status: library-dev
- worktree: ~/Code/PyAutoLabs-wt/adapt-linear-regularization
- classification: library (PyAutoArray classes/util/tests; PyAutoGalaxy + PyAutoLens prior configs, docs, composition tests)
- parallel-claim: PyAutoGalaxy + PyAutoLens are also claimed by 'lenscalc-adaptive-hessian-step'. File sets are disjoint (lenscalc: autogalaxy/operate/lens_calc.py, test_autogalaxy/operate/test_deflections.py, test_autolens/lens/test_multi_plane_cross_validation.py; this task: config/priors/regularization/*.yaml, docs/api/pixelization.rst, new inversion tests). Own worktree + own branch taken deliberately, not a fold.
- repos:
  - PyAutoArray: feature/adapt-linear-regularization
  - PyAutoGalaxy: feature/adapt-linear-regularization
  - PyAutoLens: feature/adapt-linear-regularization
- next-skill: /start_library
