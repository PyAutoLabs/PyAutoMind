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

## point-source-smoke-runtime-regression
- issue: https://github.com/PyAutoLabs/autolens_workspace/issues/537
- issued: 2026-09-07
- session: claude --resume session_01UUjCh13UJ62sgM3wN6XNuZ
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/point-source-smoke-runtime-regression
- repos:
  - autolens_workspace: feature/point-source-smoke-runtime-regression
- corrective-red: PyAutoHeart is RED; this task is a corrective fix for the reason(s) below and may not commit, push or open a PR until a human authorisation comment lands on the issue (PyAutoBrain/AUTONOMY.md corrective-PR exception).
    reason: "workspace validation not passing (5 failed, 2 timeout, cloud#34099198772: autolens notebooks/multi_dataset/modeling.ipynb, autolens scripts/multi_dataset/modeling.py, autolens_test scripts/imaging/delaunay.py, +4 more)"
    authorization: PENDING — awaiting human comment on the issue
- finding: "untimed urlretrieve stall in CI (run 34099198772 artifact traceback), not a library regression; fix = timeout+retry in autolens_workspace"

## jax-delaunay-six-tuple-unpack
- issue: https://github.com/PyAutoLabs/autolens_workspace_test/issues/296
- issued: 2026-09-07
- session: claude --resume session_01UUjCh13UJ62sgM3wN6XNuZ
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/jax-delaunay-six-tuple-unpack
- repos:
  - autolens_workspace_test: feature/jax-delaunay-six-tuple-unpack
- parallel-claim: autolens_workspace_test also claimed by nufft-threshold-subhalo-pin-rebuild, jax-grad-delaunay-constant-folding-guard and mge-group-source-basis-scale; "file sets disjoint per plans.md (T1 scripts/imaging/jax_likelihood/delaunay.py [+ smoke_tests.txt]; T2 scripts/interferometer/nufft.py + scripts/imaging/substructure/subhalo.py; T3 scripts/imaging/jax_grad/delaunay.py + additive-only scripts/misc/util.py; T4 scripts/imaging/jax_likelihood/mge_group.py); merge order T1/T2 before T3 before T4; own worktree taken"
- corrective-red: PyAutoHeart is RED; this task is a corrective fix for the reason(s) below and may not commit, push or open a PR until a human authorisation comment lands on the issue (PyAutoBrain/AUTONOMY.md corrective-PR exception).
    reason: "release validation FAILED (stage integrate)"
    reason: "workspace validation not passing (5 failed, 2 timeout, cloud#34099198772: autolens notebooks/multi_dataset/modeling.ipynb, autolens scripts/multi_dataset/modeling.py, autolens_test scripts/imaging/delaunay.py, +4 more)"
    authorization: PENDING — awaiting human comment on the issue

## nufft-threshold-subhalo-pin-rebuild
- issue: https://github.com/PyAutoLabs/autolens_workspace_test/issues/297
- issued: 2026-09-07
- session: claude --resume session_01UUjCh13UJ62sgM3wN6XNuZ
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/nufft-threshold-subhalo-pin-rebuild
- repos:
  - autolens_workspace_test: feature/nufft-threshold-subhalo-pin-rebuild
- parallel-claim: autolens_workspace_test also claimed by jax-delaunay-six-tuple-unpack (#296), jax-grad-delaunay-constant-folding-guard and mge-group-source-basis-scale; "worktree_check_conflict exited 1 against jax-delaunay-six-tuple-unpack; overridden because plans.md established the file sets are disjoint (T1 scripts/imaging/jax_likelihood/delaunay.py [+ smoke_tests.txt]; T2 scripts/interferometer/nufft.py + scripts/imaging/substructure/subhalo.py; T3 scripts/imaging/jax_grad/delaunay.py + additive-only scripts/misc/util.py; T4 scripts/imaging/jax_likelihood/mge_group.py); merge order T1/T2 before T3 before T4; own worktree taken"
- corrective-red: PyAutoHeart is RED; this task is a corrective fix for the reason(s) below and may not commit, push or open a PR until a human authorisation comment lands on the issue (PyAutoBrain/AUTONOMY.md corrective-PR exception).
    reason: "release validation FAILED (stage integrate)"
    reason: "workspace validation not passing (5 failed, 2 timeout, cloud#34099198772: autolens notebooks/multi_dataset/modeling.ipynb, autolens scripts/multi_dataset/modeling.py, autolens_test scripts/imaging/delaunay.py, +4 more)"
    authorization: PENDING — awaiting human comment on the issue

## jax-grad-delaunay-constant-folding-guard
- issue: https://github.com/PyAutoLabs/autolens_workspace_test/issues/298
- issued: 2026-09-07
- session: claude --resume session_01UUjCh13UJ62sgM3wN6XNuZ
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/jax-grad-delaunay-constant-folding-guard
- repos:
  - autolens_workspace_test: feature/jax-grad-delaunay-constant-folding-guard
- parallel-claim: autolens_workspace_test also claimed by jax-delaunay-six-tuple-unpack (#296), nufft-threshold-subhalo-pin-rebuild (#297) and mge-group-source-basis-scale; "worktree_check_conflict exited 1 against both of those; overridden because plans.md established the file sets are disjoint (T1 scripts/imaging/jax_likelihood/delaunay.py [+ smoke_tests.txt]; T2 scripts/interferometer/nufft.py + scripts/imaging/substructure/subhalo.py; T3 scripts/imaging/jax_grad/delaunay.py + additive-only scripts/misc/util.py; T4 scripts/imaging/jax_likelihood/mge_group.py); the shared scripts/misc/util.py must be ADDITIVE only or the disjointness claim fails; merge order T1/T2 before T3 before T4; own worktree taken"
- corrective-red: PyAutoHeart is RED; this task is a corrective fix for the reason(s) below and may not commit, push or open a PR until a human authorisation comment lands on the issue (PyAutoBrain/AUTONOMY.md corrective-PR exception).
    reason: "release validation FAILED (stage integrate)"
    reason: "workspace validation not passing (5 failed, 2 timeout, cloud#34099198772: autolens notebooks/multi_dataset/modeling.ipynb, autolens scripts/multi_dataset/modeling.py, autolens_test scripts/imaging/delaunay.py, +4 more)"
    authorization: PENDING — awaiting human comment on the issue

## agwt-multi-delaunay-release-timeout
- issue: https://github.com/PyAutoLabs/autogalaxy_workspace_test/issues/118
- issued: 2026-09-07
- session: claude --resume session_01UUjCh13UJ62sgM3wN6XNuZ
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/agwt-multi-delaunay-release-timeout
- repos:
  - autogalaxy_workspace_test: feature/agwt-multi-delaunay-release-timeout
- corrective-red: PyAutoHeart is RED; this task is a corrective fix for the reason below and may not commit, push or open a PR until a human authorisation comment lands on the issue (PyAutoBrain/AUTONOMY.md corrective-PR exception).
    reason: "release validation FAILED (stage integrate)"
    authorization: PENDING — awaiting human comment on the issue

## mge-group-source-basis-scale
- issue: https://github.com/PyAutoLabs/autolens_workspace_test/issues/299
- issued: 2026-09-07
- session: claude --resume session_01UUjCh13UJ62sgM3wN6XNuZ
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/mge-group-source-basis-scale
- repos:
  - autolens_workspace_test: feature/mge-group-source-basis-scale
- parallel-claim: autolens_workspace_test also claimed by jax-delaunay-six-tuple-unpack (#296), nufft-threshold-subhalo-pin-rebuild (#297) and jax-grad-delaunay-constant-folding-guard (#298); "worktree_check_conflict exited 1 against all three; overridden because plans.md established the file sets are disjoint (T1 scripts/imaging/jax_likelihood/delaunay.py [+ smoke_tests.txt]; T2 scripts/interferometer/nufft.py + scripts/imaging/substructure/subhalo.py; T3 scripts/imaging/jax_grad/delaunay.py + additive-only scripts/misc/util.py; T4 scripts/imaging/jax_likelihood/mge_group.py); merge order T1/T2 before T3 before T4, so this task merges last; own worktree taken"
- corrective-red: PyAutoHeart is RED; this task is a corrective fix for the reason(s) below and may not commit, push or open a PR until a human authorisation comment lands on the issue (PyAutoBrain/AUTONOMY.md corrective-PR exception).
    reason: "release validation FAILED (stage integrate)"
    reason: "workspace validation not passing (5 failed, 2 timeout, cloud#34099198772: autolens notebooks/multi_dataset/modeling.ipynb, autolens scripts/multi_dataset/modeling.py, autolens_test scripts/imaging/delaunay.py, +4 more)"
    authorization: PENDING — awaiting human comment on the issue
- note: PyAutoArray is an escalation candidate for this task (positive-only/NNLS solver branch) and is deliberately NOT claimed; if that branch opens it is filed as its own library issue and ships first under the library-first merge gate.
