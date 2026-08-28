# Active Tasks

## nuts-warm-start-driver-and-a100-probe
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/187
- prompt: active/nuts_warm_start_driver_and_a100_probe.md
- issued: 2026-08-28
- status: pr-open
- pr: https://github.com/PyAutoLabs/autolens_profiling/pull/188
- worktree: ~/Code/PyAutoLabs-wt/nuts-warm-start-driver-and-a100-probe
- repos:
  - autolens_profiling: feature/nuts-warm-start-driver-and-a100-probe
- note: registers `af.BlackJAXNUTS` as a first-class `nuts` searches sampler with PR#1522 warm-start,
  adds the imaging/mge/hst leaf + A100 probe submit (cold vs warm), and settles whether the parked
  SMC prototype (wsdev#113 / RAL 331058) can be resubmitted as a research row. RAL is put on this
  feature branch to run the probe and MUST return to main after merge.

## interferometer-bulge-pixelization-example
- issue: https://github.com/PyAutoLabs/autogalaxy_workspace/issues/228
- issued: 2026-08-28
- prompt: active/interferometer_bulge_pixelization_example.md
- session: claude --resume b766a19b-260c-4b56-8d19-072fa9a34b28
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/interferometer-bulge-pixelization-example
- repos:
  - autogalaxy_workspace: feature/interferometer-bulge-pixelization-example
- note: follow-up to #499/#500 docs sweep; convert canonical interferometer pixelization examples to the linear-bulge hybrid. autolens deliberately excluded (no lens light in its interferometer datasets).
- ral: profiling clone is ON feature/nuts-warm-start-driver-and-a100-probe and MUST return to main
  after merge (`git checkout main && git pull --ff-only && git branch -d feature/...`). PyAutoFit on RAL
  deliberately LEFT at f466dce1a — it already has PR#1522; pulling to 54aa0875b would put PR#1539
  (clipper/bijector compose) under job 341978's pending phase-8B arms.
- jobs: RAL 341981_[0,1] NUTS cold/warm probe (gpu, 45:00); RAL 341983 SMC warm research row (ral CPU, 1:30:00)
