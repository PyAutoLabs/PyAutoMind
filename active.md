# Active Tasks

## natural-language-first-docs
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1587
- issued: 2026-09-09
- session: claude --resume session_015LXave3uvSeLEq7S68NjXk
- status: library-dev
- worktree: ~/Code/PyAutoLabs-wt/natural-language-first-docs
- repos:
  - PyAutoFit: feature/natural-language-first-docs
- summary: |
    PyAutoFit docs-only reorder: natural_language.md becomes the main overview
    page, the_basics.md is renamed python_api.md ("The Python API") and moves
    fourth, and docs/index.md is reframed natural-language first. The human's
    uncommitted natural_language.md + backup.md deletion are carried onto the
    branch as the first commit. Brain classified `combined` off an
    @autofit_workspace out-of-scope mention; overridden to library-only.

## retire-gpu1-mig-exclusion
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/220
- workspace-pr: https://github.com/PyAutoLabs/autolens_profiling/pull/222
- heart-ack: 2026-09-05 in-session, single reason "release validation FAILED (stage integrate)" — organism-scope (PyAutoHeart Release Integrate run 33951278577); nothing in this branch is in the release chain
- issued: 2026-09-05
- session: claude --resume session_0117cr7VQNhHL2HzkGwQCDun
- status: awaiting-merge
- worktree: ~/Code/PyAutoLabs-wt/retire-gpu1-mig-exclusion
- repos:
  - autolens_profiling: feature/retire-gpu1-mig-exclusion
- parallel-claim: autolens_profiling also claimed by delaunay-nn-breakdown (#219); "file sets disjoint (hpc/batch_gpu submits, hpc/README.md, activate.sh vs _profile_cli.py + scripts/imaging/likelihood_breakdown/delaunay.py); prompt out-of-scope note says merge order does not matter; own worktree taken under --auto safe"
