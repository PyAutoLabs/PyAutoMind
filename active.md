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

## physical-fast-rebuild-autogalaxy
- issue: https://github.com/PyAutoLabs/autogalaxy_workspace_test/issues/116
- issued: 2026-09-06
- prompt: active/physical_fast_rebuild_autogalaxy.md
- session: claude --resume session_0151gQm9fk3XGLi5f18Urdba
- status: workspace-shipped, awaiting-merge
- workspace-pr: https://github.com/PyAutoLabs/autogalaxy_workspace_test/pull/117
- epic: ci-timing-fast-tests (phase 5 of 9)
- worktree: none — cloud session; branch `claude/ci-test-timing-epic-ke2lul` in the autogalaxy_workspace_test clone
- repos:
  - autogalaxy_workspace_test: claude/ci-test-timing-epic-ke2lul
- summary: |
    Phase 5 of the ci-timing-fast-tests epic: the physical + fast rebuild of the
    autogalaxy_workspace_test smoke gate (39 entries, 537 s legacy). Coarser shared
    datasets (imaging 100x100@0.3", interferometer 128x128@0.2", multi 80x80@0.2"),
    a `_group` dataset per family so the mge_group models fit simulated extra
    galaxies, over-sampling/MGE/batch levers; no absolute pins in this repo (the
    prompt's pin wave is phase 6's). Fable plan on the issue; implementation +
    local before/after timing delegated to Opus with the source stack installed
    in the container. autogalaxy_workspace_test#117 open: 39/39 green locally,
    515 s -> 438 s cold (-15%; the ~230 s import floor is untouched, compile is the
    CI cache's). Follow-up filed: draft/bug/autoarray/mixed_precision_inversion_jax_numpy_gap_small_data.md.
    Next: /prm; then phase 6 (autolens_workspace_test).
