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

## transformed-from-mode-coupled-covariance
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1569
- issued: 2026-09-07
- session: claude --resume session_01Gu4YysuvpQ4k6zkQjiwabd
- status: awaiting-merge
- bundle: ep-phase2-review
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1572
- pending-release: PyAutoFit@https://github.com/PyAutoLabs/PyAutoFit/pull/1572
- heart-ack: 2026-09-07 in-session, verdict red score 45; red reason "release validation FAILED (stage integrate)" and yellow reason "workspace validation not passing (5 failed, 2 timeout, cloud#34099198772: autolens notebooks/multi_dataset/modeling.ipynb, autolens scripts/multi_dataset/modeling.py, autolens_test scripts/imaging/delaunay.py, +4 more)" — both organism-scope; nothing in this diff is in the release chain or touched by those workspace scripts
- worktree: ~/Code/PyAutoLabs-wt/ep-phase2-review
- repos:
  - PyAutoFit: feature/transformed-from-mode-coupled-covariance

## ep-laplace-deterministic-hessian
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1570
- issued: 2026-09-07
- session: claude --resume session_01Gu4YysuvpQ4k6zkQjiwabd
- status: awaiting-merge
- bundle: ep-phase2-review
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1573
- pending-release: PyAutoFit@https://github.com/PyAutoLabs/PyAutoFit/pull/1573
- heart-ack: 2026-09-07 in-session, verdict yellow score 70; single reason "workspace validation not passing (5 failed, 2 timeout, cloud#34099198772: autolens notebooks/multi_dataset/modeling.ipynb, autolens scripts/multi_dataset/modeling.py, autolens_test scripts/imaging/delaunay.py, +4 more)" — organism-scope, none of those scripts touch the Laplace deterministic path; the earlier red reason "release validation FAILED (stage integrate)" had cleared by 21:05Z
- worktree: ~/Code/PyAutoLabs-wt/ep-phase2-review
- repos:
  - PyAutoFit: feature/ep-laplace-deterministic-hessian

## ep-full-revert-not-updated
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1571
- issued: 2026-09-07
- session: claude --resume session_01Gu4YysuvpQ4k6zkQjiwabd
- status: awaiting-merge
- bundle: ep-phase2-review
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1574
- pending-release: PyAutoFit@https://github.com/PyAutoLabs/PyAutoFit/pull/1574
- heart-ack: 2026-09-07 in-session, verdict yellow score 70, no red reasons; single reason "workspace validation not passing (5 failed, 2 timeout, cloud#34099198772: autolens notebooks/multi_dataset/modeling.ipynb, autolens scripts/multi_dataset/modeling.py, autolens_test scripts/imaging/delaunay.py, +4 more)" — organism-scope, none of those scripts exercise the EP projection path
- worktree: ~/Code/PyAutoLabs-wt/ep-phase2-review
- repos:
  - PyAutoFit: feature/ep-full-revert-not-updated
