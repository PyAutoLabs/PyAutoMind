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
