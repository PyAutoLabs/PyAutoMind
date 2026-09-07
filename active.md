# Active Tasks

## delaunay-walk-early-exit
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/530
- prompt: active/delaunay_walk_early_exit_unchunked.md
- issued: 2026-09-07
- session: claude --resume session_01B5HT8dp7sWc9qDhZp6moGr
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/delaunay-walk-early-exit
- library-pr: https://github.com/PyAutoLabs/PyAutoArray/pull/531
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace_test/pull/306
- pending-release: PyAutoArray@https://github.com/PyAutoLabs/PyAutoArray/pull/531
- heart-ack: 2026-09-07 in-session, YELLOW "workspace validation not passing (5 failed, 2 timeout, cloud#34099198772: autolens notebooks/multi_dataset/modeling.ipynb, autolens scripts/multi_dataset/modeling.py, autolens_test scripts/imaging/delaunay.py, +4 more)" plus stale "release validation incomplete: no rehearsal for current source" — organism-scope; the failing autolens_test delaunay legs do not exercise the walk and were already fixed on autolens_workspace_test main today (078e445, 4103234); this branch touches only autoarray/inversion/mesh/interpolator/ and its tests
- repos:
  - PyAutoArray: feature/delaunay-walk-early-exit
  - autolens_workspace_test: feature/delaunay-walk-early-exit
  - autolens_profiling: feature/delaunay-walk-early-exit
- parallel-claim: autolens_profiling also claimed by retire-gpu1-mig-exclusion (#220, awaiting-merge); "file sets disjoint (hpc/batch_gpu submits, hpc/README.md, activate.sh vs results/breakdown/imaging/ + results/notes/); merge order does not matter; Phase 1 of the prompt only, Phase 2 filed separately after the A100 re-measure"

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

## ep-stale-tracking-per-variable
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1575
- issued: 2026-09-07
- session: claude --resume session_01Gu4YysuvpQ4k6zkQjiwabd
- status: awaiting-merge
- worktree: ~/Code/PyAutoLabs-wt/ep-stale-tracking-per-variable
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1576
- workspace-pr: https://github.com/PyAutoLabs/autofit_workspace_test/pull/98
- pending-release: PyAutoFit@https://github.com/PyAutoLabs/PyAutoFit/pull/1576
- pending-release: autofit_workspace_test@https://github.com/PyAutoLabs/autofit_workspace_test/pull/98
- release-gate: PyAutoFit
- heart-ack: 2026-09-07 in-session, YELLOW "workspace validation not passing (5 failed, 2 timeout, cloud#34099198772: autolens notebooks/multi_dataset/modeling.ipynb, autolens scripts/multi_dataset/modeling.py, autolens_test scripts/imaging/delaunay.py, +4 more)" plus stale "release validation incomplete: no rehearsal for current source" — organism-scope; this branch touches only autofit/graphical/ and its tests
- repos:
  - PyAutoFit: feature/ep-stale-tracking-per-variable
  - autofit_workspace_test: feature/ep-stale-tracking-per-variable

## numba-interferometer-pack
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/223
- issued: 2026-09-07
- session: claude --resume session_01JCn8wPWpdiVof6uK6zn56w
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/numba-interferometer-pack
- repos:
  - autolens_profiling: feature/numba-interferometer-pack
- parallel-claim: autolens_profiling also claimed by retire-gpu1-mig-exclusion (#220, awaiting-merge); "file sets disjoint (hpc/batch_gpu submits, hpc/README.md, activate.sh vs scripts/misc/numba_interferometer/ + scripts/interferometer/likelihood_breakdown/*_numba.py + results/breakdown/interferometer/); merge order does not matter; PyAutoArray read-only and not claimed; phase 1 of 3 of the numba-interferometer-revisit epic"
