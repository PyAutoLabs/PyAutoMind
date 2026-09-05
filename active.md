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

## offtick-timing-legs-live
- issue: https://github.com/PyAutoLabs/PyAutoHeart/issues/206
- issued: 2026-09-05
- prompt: active/offtick_timing_legs_live.md
- session: claude --resume session_0151gQm9fk3XGLi5f18Urdba
- status: library-dev
- epic: ci-timing-fast-tests (phase 3 of 9)
- worktree: none — cloud session; branch `claude/ci-test-timing-epic-ke2lul` in the PyAutoHeart clone
- repos:
  - PyAutoHeart: claude/ci-test-timing-epic-ke2lul
- summary: |
    Phase 3 of the ci-timing-fast-tests epic: unit_test_timing + import_time go live
    by ingestion — lib-tests.yml (the reusable workflow every library's Tests calls)
    emits junit durations + a fresh-process import time as `unit-timings-<py>`;
    a new Heart check ingests it into the timings/ record and the existing board
    sections; workspace_testmode_timing retired as superseded by the Smoke scripts
    row. Fable plan on the issue; implementation delegated to Opus.
    Next: PR on PyAutoHeart, then /prm; phase 4 (LEGACY snapshot) follows.
