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

## legacy-baseline-timing-round
- issue: https://github.com/PyAutoLabs/PyAutoHeart/issues/208
- issued: 2026-09-05
- prompt: active/legacy_baseline_timing_round.md
- session: claude --resume session_0151gQm9fk3XGLi5f18Urdba
- status: library-shipped, awaiting-merge
- library-pr: https://github.com/PyAutoLabs/PyAutoHeart/pull/209
- epic: ci-timing-fast-tests (phase 4 of 9)
- worktree: none — cloud session; branch `claude/ci-test-timing-epic-ke2lul` in the PyAutoHeart clone
- repos:
  - PyAutoHeart: claude/ci-test-timing-epic-ke2lul
- summary: |
    Phase 4 of the ci-timing-fast-tests epic: the labeled LEGACY epoch in the
    timings/ record (epochs.jsonl + epoch-aware readers + board line) and the
    pre-rebuild digest (docs/pyautoheart/legacy_timing_round_2026-09.md). The record
    was seeded by a hand-dispatched heart-health run on 2026-09-05: 494 scripts
    across all 11 smoke-gated repos, 0 unavailable — the cross-repo artifact 403
    risk did not materialise. Unit/import rows fill on the next library CI run.
    PyAutoHeart#209 open (864 tests green): epochs.jsonl live (`legacy @ 2026-09-05`),
    readers compare within the current epoch, digest at PyAutoHeart
    `timings/legacy_round_2026-09.md`. Next: /prm; then phase 7 (CI caches) per the
    review's order, before the rebuild waves.
