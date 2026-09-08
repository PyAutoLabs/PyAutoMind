# Active Tasks

## order-lens-mge-bases-and-seed
- issue: https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/issues/57
- library-pr: https://github.com/PyAutoLabs/PyAutoGalaxy/pull/611
- workspace-pr: https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/pull/58
- pending-release: PyAutoGalaxy@https://github.com/PyAutoLabs/PyAutoGalaxy/pull/611
- heart-ack: 2026-09-08 in-session (same two reasons the human acknowledged for mge-label-degeneracy this session) "workspace validation not passing (5 failed, 2 timeout, cloud#34099198772: autolens notebooks/multi_dataset/modeling.ipynb, autolens scripts/multi_dataset/modeling.py, autolens_test scripts/imaging/delaunay.py, +4 more)" and "release validation incomplete: no rehearsal for current source" — organism-scope; neither names mge_model_from or this pipeline
- library-issue: https://github.com/PyAutoLabs/PyAutoGalaxy/issues/610
- library-prompt: draft/feature/autogalaxy/mge_model_from_order_bases.md
- prompt: active/order_lens_mge_bases_and_seed_vis_lp.md
- issued: 2026-09-08
- session: claude --resume session_015RALRY9yekWDTtbVfok64a
- status: awaiting-merge
- worktree: ~/Code/PyAutoLabs-wt/order-lens-mge-bases-and-seed
- repos:
  - PyAutoGalaxy: feature/order-lens-mge-bases-and-seed
  - euclid_strong_lens_modeling_pipeline: feature/order-lens-mge-bases-and-seed
- parallel-claim: euclid_strong_lens_modeling_pipeline also claimed by profiling-production-representative (#235, workspace-dev); "file sets disjoint except util.py: #235 changes a 2-line over-sampling hunk in scripts/lens_model_waveband.py, scripts/mge_lens_only.py, scripts/sersic_lens_model.py and util.py; this task edits scripts/initial_lens_model.py, util.py parse_fit_args (different hunk), docs/mge_label_degeneracy.md and tests/; merge order does not matter, whichever lands second rebases; own worktree under the approved plan"

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
- workspace-pr: https://github.com/PyAutoLabs/autolens_profiling/pull/236
- workspace-pr: https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/pull/56
- status: awaiting-merge
- worktree: ~/Code/PyAutoLabs-wt/profiling-production-representative
- repos:
  - autolens_profiling: feature/profiling-production-representative
  - euclid_strong_lens_modeling_pipeline: feature/profiling-production-representative
- parallel-claim: autolens_profiling also claimed by retire-gpu1-mig-exclusion (#220, awaiting-merge, hpc/MIG files only), interferometer-preload-cpu (#229, MERGED 2026-09-08 via PR #234; was misc/interferometer files only) and delaunay-adapt-split-regularization (#232, MERGED 2026-09-08); "first two disjoint; #232 shares scripts/imaging/likelihood_runtime/delaunay_numba.py and _profile_cli.py — #232 merged 2026-09-08 (PR #233), so the merge-order constraint is satisfied: rebase onto autolens_profiling main before editing those two files; own worktree approved by the human 2026-09-08"
- merge-after: https://github.com/PyAutoLabs/autolens_profiling/issues/232 — satisfied: merged 2026-09-08 via PR #233
- heart-ack: 2026-09-08 in-session, reasons "workspace validation not passing (5 failed, 2 timeout, cloud#34099198772: autolens notebooks/multi_dataset/modeling.ipynb, autolens scripts/multi_dataset/modeling.py, autolens_test scripts/imaging/delaunay.py, +4 more)" and "release validation incomplete: no rehearsal for current source" — neither touches autolens_profiling or the Euclid pipeline

## interferometer-numba-cpu-direct-conv
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/543
- prompt: active/interferometer_numba_cpu_direct_conv.md
- issued: 2026-09-08
- session: claude --resume session_018hLF3ZAcz5MmaSJBEcLkvF
- library-pr: https://github.com/PyAutoLabs/PyAutoArray/pull/545
- pending-release: PyAutoArray@https://github.com/PyAutoLabs/PyAutoArray/pull/545
- status: awaiting-merge
- worktree: ~/Code/PyAutoLabs-wt/interferometer-numba-cpu-direct-conv
- repos:
  - PyAutoArray: feature/interferometer-numba-cpu-direct-conv
- stacked-on: interferometer-sparse-operator-numpy-cpu-path (#542) — MERGED 2026-09-08 via PR #544; the parallel PyAutoArray claim is released, and this branch's PR opens against `main` (no GitHub retarget, its PR was not open at merge time)
- heart-ack: 2026-09-08 in-session, reasons "workspace validation not passing (5 failed, 2 timeout, cloud#34099198772: autolens notebooks/multi_dataset/modeling.ipynb, autolens scripts/multi_dataset/modeling.py, autolens_test scripts/imaging/delaunay.py, +4 more)" and "release validation incomplete: no rehearsal for current source" — organism-scope; neither names the interferometer inversion path or PyAutoArray
