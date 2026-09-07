# Active Tasks

## jax-grad-delaunay-fd-sweep-repin
- issue: https://github.com/PyAutoLabs/autolens_workspace_test/issues/304
- issued: 2026-09-07
- session: claude --resume session_012jnkrN39jLrJgWWNf8tMcz
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/jax-grad-delaunay-fd-sweep-repin
- corrective-red: "release validation FAILED (stage integrate)" — authorisation https://github.com/PyAutoLabs/autolens_workspace_test/issues/304#issuecomment-5575042508 (live, 2026-09-07); Release Integrate run 34148543011 sole failure scripts/imaging/jax_grad/delaunay.py; permitted = commit, push, one pending-release PR; merge/close/release stay human
- repos:

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
