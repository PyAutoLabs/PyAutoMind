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
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/multi-galaxy-scaling-zero-intensity
- classification: workspace (autolens_workspace only; simulator geometry + slam guard; un-park on a passing gate)
- heart-ack: YELLOW acknowledged 2026-08-29 — "workspace validation not passing (0 failed, 1 timeout, cloud#33229145647: autolens_test scripts/multi_dataset/delaunay_mge.py)"; "release validation incomplete: no rehearsal for current source"
- repos:
  - autolens_workspace: feature/multi-galaxy-scaling-zero-intensity
- next-skill: /ship_workspace

## fitness-log-likelihood-ceiling
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1543
- prompt: active/fitness_log_likelihood_ceiling.md
- issued: 2026-08-29
- status: library-dev
- worktree: ~/Code/PyAutoLabs-wt/fitness-log-likelihood-ceiling
- classification: library (PyAutoFit only; Fitness magnitude guard + NSS closure, wave A1)
- repos:
  - PyAutoFit: feature/fitness-log-likelihood-ceiling
- next-skill: /ship_library
