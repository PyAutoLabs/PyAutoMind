# Active Tasks

## slope-hierarchy-scale-birth
- issue: https://github.com/PyAutoLabs/PyAutoCortex/issues/24
- library-pr: https://github.com/PyAutoLabs/PyAutoCortex/pull/25
- issued: 2026-09-08
- session: claude --resume session_01JcyWRpcbRiAAYFqgFJarEr
- status: awaiting-merge
- worktree: ~/Code/PyAutoLabs-wt/slope-hierarchy-scale-birth
- repos:
  - PyAutoCortex: feature/slope-hierarchy-scale-birth

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

## interferometer-preload-cpu
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/229
- issued: 2026-09-08
- session: claude --resume session_018hLF3ZAcz5MmaSJBEcLkvF
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/interferometer-preload-cpu
- repos:
  - autolens_profiling: feature/interferometer-preload-cpu
- parallel-claim: autolens_profiling also claimed by retire-gpu1-mig-exclusion (awaiting-merge, hpc/MIG files only — disjoint file sets; own worktree approved 2026-09-08)

## delaunay-adapt-split-regularization
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/232
- issued: 2026-09-08
- session: claude --resume session_011xsh8KqgiHWTfPGgWEYMQw
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/delaunay-adapt-split-regularization
- repos:
  - autolens_profiling: feature/delaunay-adapt-split-regularization
- parallel-claim: autolens_profiling also claimed by retire-gpu1-mig-exclusion (#220, awaiting-merge) and interferometer-preload-cpu (#229, workspace-dev); "file sets verified disjoint 2026-09-08: retire touches existing hpc/batch_gpu submits + activate.sh + hpc/README.md (MIG exclusion block only), interferometer-preload-cpu touches scripts/misc/numba_interferometer, scripts/interferometer, results/breakdown/interferometer, results/notes/numba_interferometer_verdict.md and .gitignore and does NOT touch _profile_cli.py; ours is _profile_cli.py + five Delaunay cells + new adapt_split/constant_split submits + a new results note, so merge order does not matter provided the new submits omit the retired --exclude=euclid-ral-gpu-1 block; own worktree taken under supervised autonomy with an approved plan"
