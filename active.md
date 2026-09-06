# Active Tasks

## user-workspace-howto-slow-script-pass
- issue: https://github.com/PyAutoLabs/autolens_workspace/issues/536
- issued: 2026-09-06
- prompt: active/user_workspace_howto_slow_script_pass.md
- session: claude --resume session_0151gQm9fk3XGLi5f18Urdba
- status: workspace-dev
- epic: ci-timing-fast-tests (phase 8 of 9)
- worktree: none — cloud session; branch `claude/ci-test-timing-epic-ke2lul` in each workspace clone touched
- repos:
  - autolens_workspace: claude/ci-test-timing-epic-ke2lul
  - HowToLens: claude/ci-test-timing-epic-ke2lul
  - HowToGalaxy: claude/ci-test-timing-epic-ke2lul
  - autogalaxy_workspace: claude/ci-test-timing-epic-ke2lul
- summary: |
    Phase 8 of the ci-timing-fast-tests epic: the user-workspace + HowTo slow-script
    pass driven by the ingested timings. The surface is import-floor dominated
    (HowToLens 47/50 scripts under 10 s); 14 autolens/autogalaxy-stack scripts are
    at or above 10 s in CI and each gets a diagnosis (import / re-simulation /
    compile / execution / plot-output) and a category fix, shared machinery first,
    never tutorial prose. First task: explain why the pixelization tutorials run
    4-6x slower locally than in CI. autocti_workspace's 61 s start_here is phase 8b
    (own prompt). Fable plan on the issue; execution delegated to Opus. Next: /prm
    per workspace PR.

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
