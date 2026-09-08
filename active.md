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

## interferometer-preload-cpu
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/229
- issued: 2026-09-08
- session: claude --resume session_018hLF3ZAcz5MmaSJBEcLkvF
- status: awaiting-merge
- worktree: ~/Code/PyAutoLabs-wt/interferometer-preload-cpu
- repos:
  - autolens_profiling: feature/interferometer-preload-cpu
- workspace-pr: https://github.com/PyAutoLabs/autolens_profiling/pull/234
- heart-ack: 2026-09-08 in-session, YELLOW score 70, no red reasons, two reasons "workspace validation not passing (5 failed, 2 timeout, cloud#34099198772: autolens notebooks/multi_dataset/modeling.ipynb, autolens scripts/multi_dataset/modeling.py, autolens_test scripts/imaging/delaunay.py, +4 more)" and "release validation incomplete: no rehearsal for current source" - organism-scope; neither names autolens_profiling and nothing in this branch is in the release chain
- parallel-claim: autolens_profiling also claimed by retire-gpu1-mig-exclusion (awaiting-merge, hpc/MIG files only — disjoint file sets; own worktree approved 2026-09-08)

## delaunay-adapt-split-regularization
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/232
- issued: 2026-09-08
- session: claude --resume session_011xsh8KqgiHWTfPGgWEYMQw
- status: awaiting-merge
- workspace-pr: https://github.com/PyAutoLabs/autolens_profiling/pull/233
- heart-ack: 2026-09-08 in-session, YELLOW — "workspace validation not passing (5 failed, 2 timeout, cloud#34099198772: autolens notebooks/multi_dataset/modeling.ipynb, autolens scripts/multi_dataset/modeling.py, autolens_test scripts/imaging/delaunay.py, +4 more); release validation incomplete: no rehearsal for current source — both organism-scope, neither names autolens_profiling"
- worktree: ~/Code/PyAutoLabs-wt/delaunay-adapt-split-regularization
- repos:
  - autolens_profiling: feature/delaunay-adapt-split-regularization
- summary: |
    Five Delaunay cells default to AdaptSplit(0.1/10.0/0.1) behind --regularization
    {adapt_split,constant_split}; per-scheme pins + regularization provenance in every
    result JSON. A100 A/B (342340-342347, one node/window): all 8 pins PASSED; DelaunayNN
    params->H prefix 7.250 (const) vs 7.277 ms (adapt) at vmap 16 so PyAutoArray #537's
    compaction survives; whole likelihood 40.92 -> 45.76 ms/call DelaunayNN (+11.8%) and
    39.68 -> 42.47 Delaunay (+7.0%), the cost in the NNLS interior-point reconstruction,
    not in H. No library change (dependency PyAutoArray #537 already merged), so the
    library-first gate is trivially satisfied. PR open; merge stays human.
- parallel-claim: autolens_profiling also claimed by retire-gpu1-mig-exclusion (#220, awaiting-merge) and interferometer-preload-cpu (#229, workspace-dev); "file sets verified disjoint 2026-09-08: retire touches existing hpc/batch_gpu submits + activate.sh + hpc/README.md (MIG exclusion block only), interferometer-preload-cpu touches scripts/misc/numba_interferometer, scripts/interferometer, results/breakdown/interferometer, results/notes/numba_interferometer_verdict.md and .gitignore and does NOT touch _profile_cli.py; ours is _profile_cli.py + five Delaunay cells + new adapt_split/constant_split submits + a new results note, so merge order does not matter provided the new submits omit the retired --exclude=euclid-ral-gpu-1 block; own worktree taken under supervised autonomy with an approved plan"

## profiling-production-representative
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/235
- prompt: active/profiling_run_times_representative_of_production.md
- issued: 2026-09-08
- session: claude --resume session_01QUtSqZHfdCceS4Sxproayn
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/profiling-production-representative
- repos:
  - autolens_profiling: feature/profiling-production-representative
  - euclid_strong_lens_modeling_pipeline: feature/profiling-production-representative
- parallel-claim: autolens_profiling also claimed by retire-gpu1-mig-exclusion (#220, awaiting-merge, hpc/MIG files only), interferometer-preload-cpu (#229, misc/interferometer files only) and delaunay-adapt-split-regularization (#232, workspace-dev); "first two disjoint; #232 shares scripts/imaging/likelihood_runtime/delaunay_numba.py and _profile_cli.py — those two files are edited last after #232 merges and this branch rebases onto it; merge order: #232 first; own worktree approved by the human 2026-09-08"
- merge-after: https://github.com/PyAutoLabs/autolens_profiling/issues/232
