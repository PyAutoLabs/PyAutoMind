# Active Tasks

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

## numba-interferometer-pack
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/223
- workspace-pr: https://github.com/PyAutoLabs/autolens_profiling/pull/225
- heart-ack: 2026-09-07 in-session, single reason "workspace validation not passing (5 failed, 2 timeout, cloud#34099198772: autolens notebooks/multi_dataset/modeling.ipynb, autolens scripts/multi_dataset/modeling.py, autolens_test scripts/imaging/delaunay.py, +4 more)" — organism-scope (autolens_workspace JAX scripts); nothing in this branch is in the release chain
- issued: 2026-09-07
- session: claude --resume session_01JCn8wPWpdiVof6uK6zn56w
- status: awaiting-merge
- worktree: ~/Code/PyAutoLabs-wt/numba-interferometer-pack
- repos:
  - autolens_profiling: feature/numba-interferometer-pack
- parallel-claim: autolens_profiling also claimed by retire-gpu1-mig-exclusion (#220, awaiting-merge); "file sets disjoint (hpc/batch_gpu submits, hpc/README.md, activate.sh vs scripts/misc/numba_interferometer/ + scripts/interferometer/likelihood_breakdown/*_numba.py + results/breakdown/interferometer/); merge order does not matter; PyAutoArray read-only and not claimed; phase 1 of 3 of the numba-interferometer-revisit epic"
