## cluster-small-datasets
- issue: https://github.com/PyAutoLabs/autolens_workspace/issues/249 (closed)
- completed: 2026-07-09
- prs: autolens_workspace#250 + PyAutoBuild#123 (merged)
- notes: cluster scripts UN-PARKED from no_run.yaml — 24s/26s from clean regen under the sweep
  env (the parking predated the library small-mode hooks; fix was wiring). should_simulate
  guards canonical; lenstool data.py mosaic gated; lenstool modeling.py search behind
  LENSTOOL_EXAMPLE_RUN_FIT only (TEST_MODE had put the 72-param factor graph into
  reduced-iterations mode). GOTCHA: always `source activate.sh` in evidence shells — one run
  against canonical measured a phantom 7% parity drift that was really the missing worktree env.
