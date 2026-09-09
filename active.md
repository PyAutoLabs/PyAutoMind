# Active Tasks

## cortex-scorer-where-paths
- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/370
- issued: 2026-09-09
- session: claude --resume session_01FKSwTBuNwcJc2FPNpSCrkp
- status: library-dev
- worktree: ~/Code/PyAutoLabs-wt/cortex-scorer-where-paths
- repos:
  - PyAutoBrain: feature/cortex-scorer-where-paths
- summary: |
    Cortex check-in scorer: `where_paths` keeps only absolute `## Where to look`
    bullets and reads only each bullet's first token, so every real (relative,
    label-prefixed) bullet is dropped and `run_artifacts` falls back to the
    newest run under `output/` — scoring a task against an unrelated run and
    reporting a confident FAIL. Fix resolves relative bullets against the
    project roots, scans the whole bullet for path-like tokens, and refuses to
    fall back when a task declares roots that yield no run (UNOBSERVABLE, not
    FAIL); any fallback that does happen is marked as one in the readout.

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
