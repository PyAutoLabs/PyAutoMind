# Active Tasks

## delaunay-nn-launch-latency
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/532
- prompt: active/delaunay_nn_launch_latency.md
- issued: 2026-09-07
- session: claude --resume session_01B5HT8dp7sWc9qDhZp6moGr
- status: awaiting-merge
- library-pr: https://github.com/PyAutoLabs/PyAutoArray/pull/533
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace_test/pull/307
- workspace-pr: https://github.com/PyAutoLabs/autolens_profiling/pull/227
- heart-ack: 2026-09-07 in-session, YELLOW score 70 "workspace validation not passing (5 failed, 2 timeout, cloud#34099198772: autolens notebooks/multi_dataset/modeling.ipynb, autolens scripts/multi_dataset/modeling.py, autolens_test scripts/imaging/delaunay.py, +4 more)" plus stale "release validation incomplete: no rehearsal for current source" — organism-scope, same reason set acknowledged for #530; the failing autolens_test delaunay legs were already fixed on autolens_workspace_test main (078e445, 4103234)
- pending-release: PyAutoArray@https://github.com/PyAutoLabs/PyAutoArray/pull/533
- worktree: ~/Code/PyAutoLabs-wt/delaunay-nn-launch-latency
- repos:
  - PyAutoArray: feature/delaunay-nn-launch-latency
  - autolens_workspace_test: feature/delaunay-nn-launch-latency
  - autolens_profiling: feature/delaunay-nn-launch-latency
- parallel-claim: autolens_profiling will also be claimed alongside retire-gpu1-mig-exclusion (#220, awaiting-merge); "file sets disjoint (hpc/batch_gpu submits it deletes, hpc/README.md, activate.sh vs scripts/imaging/likelihood_breakdown/delaunay_nn.py + new submit scripts + results/); merge order does not matter; Phase A + B of the prompt in this task, Phase C filed separately"

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

## numba-interferometer-kernel-levers
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/226
- issued: 2026-09-07
- session: claude --resume session_01JCn8wPWpdiVof6uK6zn56w
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/numba-interferometer-kernel-levers
- repos:
  - autolens_profiling: feature/numba-interferometer-kernel-levers
- parallel-claim: autolens_profiling also claimed by retire-gpu1-mig-exclusion (#220, PR #222 open) and delaunay-walk-early-exit (PyAutoArray#530); "file sets disjoint (hpc/batch_gpu, hpc/README.md, activate.sh and results/breakdown/imaging/ + imaging results/notes/ vs scripts/misc/numba_interferometer/ + scripts/interferometer/likelihood_breakdown/ + results/breakdown/interferometer/ + results/notes/numba_interferometer_verdict.md); regenerated dashboard READMEs are the only shared files and are regenerated on rebase, never hand-merged; merge order does not matter; PyAutoArray read-only and not claimed; phase 2 of 3 of the numba-interferometer-revisit epic"
