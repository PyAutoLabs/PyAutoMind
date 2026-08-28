# Active Tasks



## bundle-themes
- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/311
- issued: 2026-08-27
- prompt: active/bundle_theme_grouping.md
- status: library-shipped, awaiting-merge
- library-pr: https://github.com/PyAutoLabs/PyAutoBrain/pull/312
- library-pr: https://github.com/PyAutoLabs/PyAutoMind/pull/366
- heart-ack: RED acknowledged 2026-08-27 (release integrate failure, shared_preloads.py timeout, hook-manifest drift, stale PyAutoFit PR — all unrelated)
- worktree: ~/Code/PyAutoLabs-wt/bundle-themes
- repos:
  - PyAutoBrain: feature/bundle-themes
  - PyAutoMind: feature/bundle-themes

## numba-cpu-nnls-iteration-reduction
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/498
- prompt: active/numba_cpu_likelihood_nnls_iteration_reduction.md
- issued: 2026-08-27
- status: library-dev
- worktree: ~/Code/PyAutoLabs-wt/numba-cpu-nnls-iteration-reduction
- repos:
  - PyAutoArray: feature/numba-cpu-nnls-iteration-reduction
  - autolens_profiling: feature/numba-cpu-nnls-iteration-reduction
- note: epic numba-cpu-likelihood phase 3a. Plan on the issue stands. Resumed 2026-08-28: worktree with
  PyAutoArray (/start_library) + autolens_profiling attached (/start_workspace; #183 merged, claim free).
  Library ships first (/ship_library), then the profiling leg (diagnostic script + results + notes) via
  /ship_workspace. Fable session → Opus implements. Measure with AUTOARRAY_NUMBA_OPERATED_MEMO=0 (harness is memo-blind).
  Phase 3b (batched active-set moves) is NOT filed — file it from 3a's diagnostic numbers.

## ell-comps-disk-constraint
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1537
- prompt: active/ell_comps_joint_disk_constraint.md
- issued: 2026-08-27
- status: library-shipped, awaiting-merge
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1538
- library-pr: https://github.com/PyAutoLabs/PyAutoGalaxy/pull/589
- heart-ack: RED acknowledged 2026-08-28 (release validation FAILED (stage integrate) — the known human-authorised override for this task; unrelated to these branches)
- note: merge PyAutoFit#1538 FIRST — PyAutoGalaxy#589 declares geometry the PyAutoFit PR introduces the machinery to read
- worktree: ~/Code/PyAutoLabs-wt/ell-comps-disk-constraint
- repos:
  - PyAutoFit: feature/ell-comps-disk-constraint
  - PyAutoGalaxy: feature/ell-comps-disk-constraint
