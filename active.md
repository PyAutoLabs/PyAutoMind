# Active Tasks

## delaunay-edge-ring-zeroed
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/526
- issued: 2026-09-05
- prompt: active/delaunay_edge_ring_never_zeroed.md
- session: claude --resume session_01XCQK1pjQx7YH5e9dtWrX76
- status: workspace-shipped, awaiting-merge (library PR #527 open; workspace PRs euclid #52 + autolens_workspace #535 open behind the library-first gate)
- library-pr: https://github.com/PyAutoLabs/PyAutoArray/pull/527
- workspace-pr: https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/pull/52
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace/pull/535
- pending-release: PyAutoArray@https://github.com/PyAutoLabs/PyAutoArray/pull/527
- release-gate: PyAutoArray
- worktree: ~/Code/PyAutoLabs-wt/delaunay-edge-ring-zeroed
- location: web-session (clones at /home/user/pyautoarray, /home/user/euclid_strong_lens_modeling_pipeline, /home/user/autolens_workspace; no worktree)
- classification: both — library PyAutoArray first, then euclid_strong_lens_modeling_pipeline + autolens_workspace behind the library-first gate
- suggested-branch: claude/delaunay-edge-ring-zeroed-8l4u1z
- epic: euclid-dr1-prep
- repos:
  - PyAutoArray: claude/delaunay-edge-ring-zeroed-8l4u1z
  - euclid_strong_lens_modeling_pipeline: claude/delaunay-edge-ring-zeroed-8l4u1z
  - autolens_workspace: claude/delaunay-edge-ring-zeroed-8l4u1z

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
