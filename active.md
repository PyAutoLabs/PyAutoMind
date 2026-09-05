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

## permanent-ci-timing-history
- issue: https://github.com/PyAutoLabs/PyAutoHeart/issues/204
- issued: 2026-09-05
- prompt: active/permanent_ci_timing_history.md
- session: claude --resume session_0151gQm9fk3XGLi5f18Urdba
- status: library-dev
- epic: ci-timing-fast-tests (phase 2 of 9)
- worktree: none — cloud session; branch `claude/ci-test-timing-epic-ke2lul` in the PyAutoHeart clone
- repos:
  - PyAutoHeart: claude/ci-test-timing-epic-ke2lul
- summary: |
    Phase 2 of the ci-timing-fast-tests epic: the permanent timing record
    (`timings/gates.jsonl` + `timings/scripts/<repo>.jsonl`, append-only, deduped on
    date / run id) committed daily by heart-health.yml; the checks read their
    baselines from it. Fable plan on the issue; implementation delegated to Opus.
    Next: PR on PyAutoHeart, then /prm; phase 3 (dead timing legs) follows.
