# Active Tasks

## traced-assertions-on-jax-path
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1581
- prompt: active/traced_assertions_on_jax_path.md
- issued: 2026-09-08
- session: claude --resume session_015RALRY9yekWDTtbVfok64a
- status: library-dev
- worktree: ~/Code/PyAutoLabs-wt/traced-assertions-on-jax-path
- repos:
  - PyAutoFit: feature/traced-assertions-on-jax-path
  - autofit_workspace_test: feature/traced-assertions-on-jax-path

## mge-label-degeneracy
- issue: https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/issues/54
- workspace-pr: https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/pull/55
- heart-ack: 2026-09-08 in-session, two reasons "workspace validation not passing (5 failed, 2 timeout, cloud#34099198772: autolens notebooks/multi_dataset/modeling.ipynb, autolens scripts/multi_dataset/modeling.py, autolens_test scripts/imaging/delaunay.py, +4 more)" and "release validation incomplete: no rehearsal for current source" — organism-scope; this branch adds one docs file and touches no script in the release chain
- prompt: active/remove_the_two_fold_label_degeneracy_in.md
- issued: 2026-09-08
- session: claude --resume session_015RALRY9yekWDTtbVfok64a
- status: awaiting-merge
- worktree: ~/Code/PyAutoLabs-wt/mge-label-degeneracy
- repos:
  - euclid_strong_lens_modeling_pipeline: feature/mge-label-degeneracy
- parallel-claim: euclid_strong_lens_modeling_pipeline also claimed by profiling-production-representative (#235, workspace-dev); "file sets disjoint: this task adds only docs/mge_label_degeneracy.md (research note, no script edits); #235 reads scripts/initial_lens_model.py vis_pix stage for its audit; merge order does not matter; own worktree taken under the approved plan"

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

## interferometer-apply-operator-rfft2
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/538
- library-pr: https://github.com/PyAutoLabs/PyAutoArray/pull/540
- pending-release: PyAutoArray@https://github.com/PyAutoLabs/PyAutoArray/pull/540
- heart-ack: 2026-09-08 in-session, two reasons "workspace validation not passing (5 failed, 2 timeout, cloud#34099198772: autolens notebooks/multi_dataset/modeling.ipynb, autolens scripts/multi_dataset/modeling.py, autolens_test scripts/imaging/delaunay.py, +4 more)" and "release validation incomplete: no rehearsal for current source" — organism-scope; neither names PyAutoArray or a library test, and this branch changes no API and no numerical result
- prompt: active/interferometer_apply_operator_rfft2.md
- issued: 2026-09-08
- session: claude --resume session_018hLF3ZAcz5MmaSJBEcLkvF
- status: awaiting-merge
- worktree: ~/Code/PyAutoLabs-wt/interferometer-apply-operator-rfft2
- repos:
  - PyAutoArray: feature/interferometer-apply-operator-rfft2

## interferometer-preload-nufft-type1
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/539
- prompt: active/interferometer_preload_nufft_type1.md
- issued: 2026-09-08
- session: claude --resume session_018hLF3ZAcz5MmaSJBEcLkvF
- status: library-dev
- worktree: ~/Code/PyAutoLabs-wt/interferometer-preload-nufft-type1
- repos:
  - PyAutoArray: feature/interferometer-preload-nufft-type1
- stacked-on: interferometer-apply-operator-rfft2 (#538)
- parallel-claim: PyAutoArray also claimed by interferometer-apply-operator-rfft2 (task 2 is stacked on task 1's branch; same file, disjoint functions; approved 2026-09-08)

## aggregator-search-json-sentinel
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1582
- prompt: active/replace_metadata_sentinel_with_search_json.md
- issued: 2026-09-08
- session: claude --resume session_01GkELVxsdpNKyegTu4bFJTR
- status: library-dev
- worktree: ~/Code/PyAutoLabs-wt/aggregator-search-json-sentinel
- parallel-claim: "PyAutoFit and autofit_workspace_test also claimed by traced-assertions-on-jax-path (#1581); file sets disjoint (aggregator/, paths/directory.py, profiling/aggregator vs mapper/prior, fitness.py); own worktree approved 2026-09-08"
- repos:
