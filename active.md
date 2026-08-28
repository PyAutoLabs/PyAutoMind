# Active Tasks

## science-project-memory
- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/315
- prompt: active/science_project_memory_a_fresh_chat_pointed.md
- issued: 2026-08-28
- status: library-dev
- worktree: ~/Code/PyAutoLabs-wt/science-project-memory
- classification: library (three independent assistant/organ repos; no workspace follow-up)
- repos:
- note: phased — Phase 1 PyAutoBrain `clone sync` lever, Phase 2 autolens_assistant (the
  reference copy, deliverables A-D), Phase 3 propagate to autocti_assistant +
  autogalaxy_assistant via the new sync. autofit_assistant is dry-run only (~343 lines
  diverged) — its report goes on the issue for a human. euclid_assistant is OUT OF SCOPE.

## anonymise-wfc3-ir-hole-regression-target
- issue: https://github.com/PyAutoLabs/PyAutoReduce/issues/73
- prompt: active/anonymise_the_named_science_target_in_the.md
- issued: 2026-08-28
- status: library-dev
- worktree: ~/Code/PyAutoLabs-wt/anonymise-wfc3-ir-hole-regression-target
- classification: library (PyAutoReduce only)
- repos:
- next-skill: start_library (PyAutoReduce) -> implement the rename -> ship_library
- note: comment/test-name/doc rename only, no behaviour change. PyAutoMind history records
  (complete/, condemned.md, autonomy_log.md) are deliberately left untouched.

## nuts-warm-start-driver-and-a100-probe
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/187
- prompt: active/nuts_warm_start_driver_and_a100_probe.md
- issued: 2026-08-28
- status: pr-open
- pr: https://github.com/PyAutoLabs/autolens_profiling/pull/188
- worktree: ~/Code/PyAutoLabs-wt/nuts-warm-start-driver-and-a100-probe
- repos:
  - autolens_profiling: feature/nuts-warm-start-driver-and-a100-probe
- note: registers `af.BlackJAXNUTS` as a first-class `nuts` searches sampler with PR#1522 warm-start,
  adds the imaging/mge/hst leaf + A100 probe submit (cold vs warm), and settles whether the parked
  SMC prototype (wsdev#113 / RAL 331058) can be resubmitted as a research row. RAL is put on this
  feature branch to run the probe and MUST return to main after merge.

## numba-hst-curvature-matrix-phase2
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/507
- prompt: active/numba_cpu_hst_curvature_matrix_phase2.md
- issued: 2026-08-28
- status: library-dev
- worktree: ~/Code/PyAutoLabs-wt/numba-hst-curvature-matrix-phase2
- classification: both (library PyAutoArray + PyAutoGalaxy, workspace autolens_profiling)
- parallel-claim: autolens_profiling is also claimed by `nuts-warm-start-driver-and-a100-probe`; file sets are disjoint (this task: `scripts/imaging/likelihood_breakdown/`, `results/breakdown/imaging/`, `results/notes/`; NUTS: `scripts/misc/searches/`, `scripts/imaging/searches/nuts/`, `results/notes/inference/`). Human approved an own parallel worktree 2026-08-28, same arrangement as phase 1. COMMIT DISCIPLINE: explicit pathspecs only in autolens_profiling, never `git add -A`.
- predecessor: phase 1 shipped and merged 2026-08-28 — `complete/2026/08/numba-hst-curvature-matrix-speedup.md` (PyAutoArray#506 `1b89404b`, autolens_profiling#189 `b3fa632a`); PyAutoArray#505 closed.
- repos:
  - PyAutoArray: feature/numba-hst-curvature-matrix-phase2
  - PyAutoGalaxy: feature/numba-hst-curvature-matrix-phase2
  - autolens_profiling: feature/numba-hst-curvature-matrix-phase2
- next-skill: implementation per the approved plan (step 0 instrument checkpoint first), then ship_library PyAutoArray -> ship_library PyAutoGalaxy -> ship_workspace autolens_profiling
- summary: |
    Successor to #505. Post-#505 the HST rectangular numba evaluation is 0.60 s/eval,
    split mapper×mapper 0.277 s (46%) + MGE operated mapping matrix ~0.22 s (37%).
    Target ≤ ~0.35 s/eval, likelihood unchanged to pin (rtol 1e-6 where summation
    order changes, bit-identical otherwise). Step 0 instruments the MGE row into 3
    sub-rows + records geometry constants (checkpoint); step 1 is a bit-identical
    hoist in `curvature_matrix_via_sparse_operator_from` behind a new oracle test;
    step 2 is the two-stage reformulation (per-data-pixel dense source-space
    accumulator + contiguous AXPYs, est. 1.7–2.5× on the block); step 3 caches the
    `OverSampler.binned_array_2d_from` divisor (PyAutoArray) and adds a
    shared-geometry fast path to `LightProfileLinearObjFuncList` (PyAutoGalaxy —
    the 60 MGE Gaussians share centre/ell_comps, only sigma varies); step 4 is
    paired before/after + pins + pool run + note, then ship library→workspace.
    Planning findings: the MGE lever lives in PyAutoGalaxy (hence it is in Repos),
    and the symmetry + unique-mappings levers are already exploited — the live
    mapper×mapper lever is the two-stage reformulation. `prange` not planned.
