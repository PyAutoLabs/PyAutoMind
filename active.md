# Active Tasks

## dataset-fits-image-only
- issue: https://github.com/PyAutoLabs/PyAutoGalaxy/issues/608
- heart-ack: 2026-09-08 in-session, two reasons "workspace validation not passing (5 failed, 2 timeout, cloud#34099198772: autolens notebooks/multi_dataset/modeling.ipynb, autolens scripts/multi_dataset/modeling.py, autolens_test scripts/imaging/delaunay.py, +4 more)" and "release validation incomplete: no rehearsal for current source" — organism-scope; this branch touches analysis save_attributes, two plotters, plots.yaml and tests, none in the failing scripts
- prompt: active/dataset_fits_written_twice_files_and_image.md
- issued: 2026-09-08
- session: claude --resume session_01Giskz46AjniG7E9dKxwpTG
- status: awaiting-merge
- worktree: ~/Code/PyAutoLabs-wt/dataset-fits-image-only
- library-pr: https://github.com/PyAutoLabs/PyAutoGalaxy/pull/609
- library-pr: https://github.com/PyAutoLabs/PyAutoLens/pull/731
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace/pull/539
- workspace-pr: https://github.com/PyAutoLabs/autogalaxy_workspace/pull/236
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace_test/pull/310
- workspace-pr: https://github.com/PyAutoLabs/autogalaxy_workspace_test/pull/120
- repos:
  - PyAutoGalaxy: feature/dataset-fits-image-only
  - PyAutoLens: feature/dataset-fits-image-only
  - autolens_workspace: feature/dataset-fits-image-only
  - autogalaxy_workspace: feature/dataset-fits-image-only
  - autolens_workspace_test: feature/dataset-fits-image-only
  - autogalaxy_workspace_test: feature/dataset-fits-image-only

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
- parallel-claim: autolens_profiling also claimed by retire-gpu1-mig-exclusion (#220, awaiting-merge, hpc/MIG files only), interferometer-preload-cpu (#229, MERGED 2026-09-08 via PR #234; was misc/interferometer files only) and delaunay-adapt-split-regularization (#232, MERGED 2026-09-08); "first two disjoint; #232 shares scripts/imaging/likelihood_runtime/delaunay_numba.py and _profile_cli.py — #232 merged 2026-09-08 (PR #233), so the merge-order constraint is satisfied: rebase onto autolens_profiling main before editing those two files; own worktree approved by the human 2026-09-08"
- merge-after: https://github.com/PyAutoLabs/autolens_profiling/issues/232 — satisfied: merged 2026-09-08 via PR #233
- heart-ack: 2026-09-08 in-session, reasons "workspace validation not passing (5 failed, 2 timeout, cloud#34099198772: autolens notebooks/multi_dataset/modeling.ipynb, autolens scripts/multi_dataset/modeling.py, autolens_test scripts/imaging/delaunay.py, +4 more)" and "release validation incomplete: no rehearsal for current source" — neither touches autolens_profiling or the Euclid pipeline
