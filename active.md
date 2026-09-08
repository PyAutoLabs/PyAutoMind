# Active Tasks

## order-lens-mge-bases-and-seed
- issue: https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/issues/57
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1586
- library-pr: https://github.com/PyAutoLabs/PyAutoGalaxy/pull/611
- workspace-pr: https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/pull/58
- pending-release: PyAutoFit@https://github.com/PyAutoLabs/PyAutoFit/pull/1586
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
  - PyAutoFit: feature/order-lens-mge-bases-and-seed
  - PyAutoGalaxy: feature/order-lens-mge-bases-and-seed
  - euclid_strong_lens_modeling_pipeline: feature/order-lens-mge-bases-and-seed
- parallel-claim: euclid_strong_lens_modeling_pipeline was also claimed by profiling-production-representative (#235, workspace-dev) — merged and closed 2026-09-08, claim released; "file sets disjoint except util.py: #235 changes a 2-line over-sampling hunk in scripts/lens_model_waveband.py, scripts/mge_lens_only.py, scripts/sersic_lens_model.py and util.py; this task edits scripts/initial_lens_model.py, util.py parse_fit_args (different hunk), docs/mge_label_degeneracy.md and tests/; merge order does not matter, whichever lands second rebases; own worktree under the approved plan"

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

## interferometer-numba-cpu-direct-conv
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/543
- prompt: active/interferometer_numba_cpu_direct_conv.md
- issued: 2026-09-08
- session: claude --resume session_018hLF3ZAcz5MmaSJBEcLkvF
- status: library-dev
- worktree: ~/Code/PyAutoLabs-wt/interferometer-numba-cpu-direct-conv
- repos:
  - PyAutoArray: feature/interferometer-numba-cpu-direct-conv
- stacked-on: interferometer-sparse-operator-numpy-cpu-path (#542) — MERGED 2026-09-08 via PR #544; the parallel PyAutoArray claim is released, and this branch's PR opens against `main` (no GitHub retarget, its PR was not open at merge time)
