# Active Tasks

## pixelization-fit-cpu-users-docs
- issue: https://github.com/PyAutoLabs/autolens_workspace/issues/506
- prompt: active/pixelization_fit_cpu_users_paragraph.md
- issued: 2026-08-28
- status: library-dev
- worktree: ~/Code/PyAutoLabs-wt/pixelization-fit-cpu-users-docs
- repos:
  - PyAutoArray: feature/pixelization-fit-cpu-users-docs
  - autolens_workspace: feature/pixelization-fit-cpu-users-docs
  - HowToLens: feature/pixelization-fit-cpu-users-docs
- note: docs sweep fallout from the numba-cpu-likelihood epic close-out (three comment/prose fixes, no
  behaviour change). Combined workflow: PyAutoArray comment leg via /start_library + /ship_library, then
  autolens_workspace + HowToLens via /start_workspace + /ship_workspace, then /prm. Fable session → Opus.

## nuts-warm-start-driver-and-a100-probe
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/187
- prompt: active/nuts_warm_start_driver_and_a100_probe.md
- issued: 2026-08-28
- status: library-dev
- worktree: ~/Code/PyAutoLabs-wt/nuts-warm-start-driver-and-a100-probe
- repos:
  - autolens_profiling: feature/nuts-warm-start-driver-and-a100-probe
- note: registers `af.BlackJAXNUTS` as a first-class `nuts` searches sampler with PR#1522 warm-start,
  adds the imaging/mge/hst leaf + A100 probe submit (cold vs warm), and settles whether the parked
  SMC prototype (wsdev#113 / RAL 331058) can be resubmitted as a research row. RAL is put on this
  feature branch to run the probe and MUST return to main after merge.

## sparse-interferometer-docs-sweep
- issue: https://github.com/PyAutoLabs/autolens_workspace/issues/508
- issued: 2026-08-28
- prompt: active/sparse_interferometer_docs_sweep.md
- session: claude --resume b766a19b-260c-4b56-8d19-072fa9a34b28
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/sparse-interferometer-docs-sweep
- repos:
  - autolens_workspace: feature/sparse-interferometer-docs-sweep
  - autogalaxy_workspace: feature/sparse-interferometer-docs-sweep
- note: prose-only follow-up to #499/#500 (user: no new scripts). Sweep table in session scratchpad docs_sweep_brief.md.
