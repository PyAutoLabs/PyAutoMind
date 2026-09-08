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
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/interferometer-preload-cpu
- repos:
  - autolens_profiling: feature/interferometer-preload-cpu
- parallel-claim: autolens_profiling also claimed by retire-gpu1-mig-exclusion (awaiting-merge, hpc/MIG files only — disjoint file sets; own worktree approved 2026-09-08)

## delaunay-nn-constant-split-assembly
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/536
- issued: 2026-09-08
- session: claude --resume session_011xsh8KqgiHWTfPGgWEYMQw
- status: library-shipped, awaiting-merge
- library-pr: https://github.com/PyAutoLabs/PyAutoArray/pull/537
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace_test/pull/309
- workspace-pr: https://github.com/PyAutoLabs/autolens_profiling/pull/231
- heart-ack: 2026-09-08 in-session, YELLOW score 70, two reasons "workspace validation not passing (5 failed, 2 timeout, cloud#34099198772: autolens notebooks/multi_dataset/modeling.ipynb, autolens scripts/multi_dataset/modeling.py, autolens_test scripts/imaging/delaunay.py, +4 more)" and "release validation incomplete: no rehearsal for current source" - organism-scope; the cloud smoke run predates this branch and the two delaunay legs it names (jax_grad/delaunay.py, jax_likelihood/delaunay.py, both reg.AdaptSplit through the changed function) were re-run on this branch and both pass
- worktree: ~/Code/PyAutoLabs-wt/delaunay-nn-constant-split-assembly
- repos:
  - PyAutoArray: feature/delaunay-nn-constant-split-assembly
  - autolens_profiling: feature/delaunay-nn-constant-split-assembly
  - autolens_workspace_test: feature/delaunay-nn-constant-split-assembly
- parallel-claim: autolens_profiling also claimed by retire-gpu1-mig-exclusion (awaiting-merge, 88 MIG-exclusion files) and interferometer-preload-cpu (no commits yet, interferometer preload scope); "file sets disjoint (this task adds new hpc/batch_gpu/submit_*assembly* files, results/notes/delaunay_nn_constant_split_assembly.md, new results/breakdown JSON and scripts/misc/delaunay_nn/assembly_bench.py; retire touches 88 existing MIG files of which the only delaunay_nn one is submit_delaunay_nn_benchmark_a100, and interferometer-preload-cpu has no commits); own worktree taken under the same precedent recorded for the two existing claims"
