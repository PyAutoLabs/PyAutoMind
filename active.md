# Active Tasks

## replace-promise-no-op-graph-walk
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1563
- issued: 2026-09-06
- prompt: active/replace_promise_no_op_graph_walk.md
- session: claude --resume session_0151gQm9fk3XGLi5f18Urdba
- status: library-shipped, awaiting-merge
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1564
- epic: ci-timing-fast-tests (phase 8c, library leg)
- worktree: none — cloud session; branch `claude/ci-test-timing-epic-ke2lul` in the library clones
- repos:
  - PyAutoFit: claude/ci-test-timing-epic-ke2lul
- summary: |
    Phase 8c of the ci-timing-fast-tests epic (PyAutoFit): a shared-machinery finding from
    the phase-8 user-workspace diagnosis, with the measured diff on the issue. One PR per
    library on the epic branch; library-first order PyAutoNerves#159 -> PyAutoArray#528,
    PyAutoFit#1563 independent. Validation: unit tests + both _test smoke gates with the
    branch installed. Execution delegated to Opus. Next: /prm per library PR.

## small-datasets-cap-stamp-stops-resimulation
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/528
- issued: 2026-09-06
- prompt: active/small_datasets_cap_stamp_stops_resimulation.md
- session: claude --resume session_0151gQm9fk3XGLi5f18Urdba
- status: library-shipped, awaiting-merge
- library-pr: https://github.com/PyAutoLabs/PyAutoNerves/pull/160
- library-pr-2: https://github.com/PyAutoLabs/PyAutoArray/pull/529
- epic: ci-timing-fast-tests (phase 8c, library leg)
- worktree: none — cloud session; branch `claude/ci-test-timing-epic-ke2lul` in the library clones
- repos:
  - PyAutoNerves: claude/ci-test-timing-epic-ke2lul
  - PyAutoArray: claude/ci-test-timing-epic-ke2lul
- summary: |
    Phase 8c of the ci-timing-fast-tests epic (PyAutoNerves + PyAutoArray (PyAutoNerves#159 first)): a shared-machinery finding from
    the phase-8 user-workspace diagnosis, with the measured diff on the issue. One PR per
    library on the epic branch; library-first order PyAutoNerves#159 -> PyAutoArray#528,
    PyAutoFit#1563 independent. Validation: unit tests + both _test smoke gates with the
    branch installed. Execution delegated to Opus. Next: /prm per library PR.

## sparse-operator-ignores-disable-jax
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/528
- issued: 2026-09-06
- prompt: active/sparse_operator_ignores_disable_jax.md
- session: claude --resume session_0151gQm9fk3XGLi5f18Urdba
- status: library-shipped, awaiting-merge
- library-pr: https://github.com/PyAutoLabs/PyAutoNerves/pull/160
- library-pr-2: https://github.com/PyAutoLabs/PyAutoArray/pull/529
- epic: ci-timing-fast-tests (phase 8c, library leg)
- worktree: none — cloud session; branch `claude/ci-test-timing-epic-ke2lul` in the library clones
- repos:
  - PyAutoNerves: claude/ci-test-timing-epic-ke2lul
  - PyAutoArray: claude/ci-test-timing-epic-ke2lul
- summary: |
    Phase 8c of the ci-timing-fast-tests epic (PyAutoNerves + PyAutoArray (PyAutoNerves#159 first)): a shared-machinery finding from
    the phase-8 user-workspace diagnosis, with the measured diff on the issue. One PR per
    library on the epic branch; library-first order PyAutoNerves#159 -> PyAutoArray#528,
    PyAutoFit#1563 independent. Validation: unit tests + both _test smoke gates with the
    branch installed. Execution delegated to Opus. Next: /prm per library PR.

## mesh-shape-honours-small-datasets-cap
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/528
- issued: 2026-09-06
- prompt: active/mesh_shape_honours_small_datasets_cap.md
- session: claude --resume session_0151gQm9fk3XGLi5f18Urdba
- status: library-shipped, awaiting-merge
- library-pr: https://github.com/PyAutoLabs/PyAutoArray/pull/529
- epic: ci-timing-fast-tests (phase 8c, library leg)
- worktree: none — cloud session; branch `claude/ci-test-timing-epic-ke2lul` in the library clones
- repos:
  - PyAutoArray: claude/ci-test-timing-epic-ke2lul
- summary: |
    Phase 8c of the ci-timing-fast-tests epic (PyAutoArray): a shared-machinery finding from
    the phase-8 user-workspace diagnosis, with the measured diff on the issue. One PR per
    library on the epic branch; library-first order PyAutoNerves#159 -> PyAutoArray#528,
    PyAutoFit#1563 independent. Validation: unit tests + both _test smoke gates with the
    branch installed. Execution delegated to Opus. Next: /prm per library PR.

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
