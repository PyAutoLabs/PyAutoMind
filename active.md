# Active Tasks

## cortex-pull-declared-output-roots
- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/372
- issued: 2026-09-09
- session: claude --resume session_01FKSwTBuNwcJc2FPNpSCrkp
- status: library-dev
- worktree: ~/Code/PyAutoLabs-wt/cortex-pull-declared-output-roots
- repos:
  - PyAutoBrain: feature/cortex-pull-declared-output-roots
  - euclid_strong_lens_modeling_pipeline: feature/cortex-pull-declared-output-roots
- summary: |
    Each science project's `hpc/sync` hard-codes `PULL_DIRS`, so a run written to
    a custom `PYAUTO_OUTPUT_DIR` is never pulled (166 MB of euclid_dr1_prelim
    ordered-MGE results sat on RAL on 2026-09-09). Plan approved: Cortex derives
    the `output*` roots its tasks declare and passes them via `PYAUTO_PULL_DIRS`,
    which the three active projects' scripts append to their own `PULL_DIRS` —
    extending the env-override convention `hpc/sync.conf` already documents.
    Only `output*` roots are ever passed: a pull rsyncs remote -> local, so
    handing it `scripts/` or `wiki/` would overwrite local source.
    Unblocked 2026-09-09: PyAutoBrain#371 merged (ec354a7), so `_path_tokens` is
    on main and the worktree claim cleared. subhalo_validation and
    slope_hierarchy_scale are PyAutoLabs repos outside `repos.yaml`; they are
    edited in worktrees taken off their science clones, so the live science
    trees never switch branches.

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
