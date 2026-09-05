# Active Tasks

## retire-gpu1-mig-exclusion
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/220
- pr: https://github.com/PyAutoLabs/autolens_profiling/pull/222
- heart-ack: 2026-09-05 in-session, single reason "release validation FAILED (stage integrate)" — organism-scope (PyAutoHeart Release Integrate run 33951278577); nothing in this branch is in the release chain
- issued: 2026-09-05
- session: claude --resume session_0117cr7VQNhHL2HzkGwQCDun
- status: awaiting-merge
- worktree: ~/Code/PyAutoLabs-wt/retire-gpu1-mig-exclusion
- repos:
  - autolens_profiling: feature/retire-gpu1-mig-exclusion
- parallel-claim: autolens_profiling also claimed by delaunay-nn-breakdown (#219); "file sets disjoint (hpc/batch_gpu submits, hpc/README.md, activate.sh vs _profile_cli.py + scripts/imaging/likelihood_breakdown/delaunay.py); prompt out-of-scope note says merge order does not matter; own worktree taken under --auto safe"

## smoke-timings-ingester
- issue: https://github.com/PyAutoLabs/PyAutoHeart/issues/202
- issued: 2026-09-05
- prompt: active/smoke_timings_ingester_per_script_board.md
- session: claude --resume session_0151gQm9fk3XGLi5f18Urdba
- status: library-dev
- epic: ci-timing-fast-tests (phase 1 of 9)
- worktree: none — cloud session; branch `claude/ci-test-timing-epic-ke2lul` in the PyAutoHeart clone
- repos:
  - PyAutoHeart: claude/ci-test-timing-epic-ke2lul
- summary: |
    Phase 1 of the ci-timing-fast-tests epic: the smoke-timings ingester (per-script
    CI timing rows on the Heart ⏱ board). Fable-reviewed plan on the issue;
    implementation delegated to an Opus subagent per the Brain's delegation
    ladder. Next: PR on PyAutoHeart, then /prm; phase 2 (durable history) follows.
