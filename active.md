# Active Tasks

## pixelized-source-magnification-latent
- issue: https://github.com/PyAutoLabs/PyAutoLens/issues/726
- issued: 2026-09-05
- prompt: active/magnification_latent_zero_for_pixelized_source.md
- session: claude --resume session_011kyfKgDB1rMkcQsn19ow4T
- status: library-dev
- worktree: ~/Code/PyAutoLabs-wt/pixelized-source-magnification-latent
- location: web-session (PyAutoLens shallow clone at /home/user/pyautolens; no worktree yet)
- classification: both — library PyAutoLens first, workspace follow-up euclid_strong_lens_modeling_pipeline behind the library-first gate
- suggested-branch: feature/pixelized-source-magnification-latent
- epic: euclid-dr1-prep (follow-up to phase 8; second of the audit's two defects)
- repos:
  - PyAutoLens: feature/pixelized-source-magnification-latent

## delaunay-nn-breakdown
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/219
- issued: 2026-09-05
- session: claude --resume session_01XQ1gs3WVa2k4721x65wrmr
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/delaunay-nn-breakdown
- repos:
  - autolens_profiling: feature/delaunay-nn-breakdown

## retire-gpu1-mig-exclusion
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/220
- issued: 2026-09-05
- session: claude --resume session_0117cr7VQNhHL2HzkGwQCDun
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/retire-gpu1-mig-exclusion
- repos:
  - autolens_profiling: feature/retire-gpu1-mig-exclusion
- parallel-claim: autolens_profiling also claimed by delaunay-nn-breakdown (#219); "file sets disjoint (hpc/batch_gpu submits, hpc/README.md, activate.sh vs _profile_cli.py + scripts/imaging/likelihood_breakdown/delaunay.py); prompt out-of-scope note says merge order does not matter; own worktree taken under --auto safe"
