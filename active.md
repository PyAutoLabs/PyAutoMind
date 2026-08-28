# Active Tasks

## science-project-memory
- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/315
- prompt: active/science_project_memory_a_fresh_chat_pointed.md
- issued: 2026-08-28
- status: library-dev
- worktree: ~/Code/PyAutoLabs-wt/science-project-memory
- classification: library (three independent assistant/organ repos; no workspace follow-up)
- repos:
  - PyAutoBrain: feature/science-project-memory
  - autolens_assistant: feature/science-project-memory
  - autocti_assistant: feature/science-project-memory
  - autogalaxy_assistant: feature/science-project-memory
- note: phased — Phase 1 PyAutoBrain `clone sync` lever, Phase 2 autolens_assistant (the
  reference copy, deliverables A-D), Phase 3 propagate to autocti_assistant +
  autogalaxy_assistant via the new sync. autofit_assistant is dry-run only (~343 lines
  diverged) — its report goes on the issue for a human. euclid_assistant is OUT OF SCOPE.

## anonymise-wfc3-ir-hole-regression-target
- issue: https://github.com/PyAutoLabs/PyAutoReduce/issues/73
- prompt: active/anonymise_the_named_science_target_in_the.md
- issued: 2026-08-28
- status: library-dev, branch-pushed, pr-blocked-heart-red
- worktree: ~/Code/PyAutoLabs-wt/anonymise-wfc3-ir-hole-regression-target
- classification: library (PyAutoReduce only)
- repos:
  - PyAutoReduce: feature/anonymise-wfc3-ir-hole-regression-target
- commit: b4ee3697097fe91fe332b12d61c8479a6756a3fb
- tests: 299 passed, 3 skipped (test_autoreduce/, 2026-08-28)
- next-skill: ship_library step 4 (open the PR) once Heart clears; PR body is drafted verbatim
  on the issue comment https://github.com/PyAutoLabs/PyAutoReduce/issues/73#issuecomment-5458441602
- blocked-by: Heart readiness RED 2026-08-28T21:34:42Z - red_reasons: "release validation FAILED
  (stage integrate)". None of the RED/YELLOW reasons touch PyAutoReduce; needs a human to clear
  the RED or authorise the AUTONOMY.md corrective-PR exception.
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
- status: shipped, awaiting-merge (all three PRs open, CI watched; merge is human)
- worktree: ~/Code/PyAutoLabs-wt/numba-hst-curvature-matrix-phase2
- classification: both (library PyAutoArray + PyAutoGalaxy, workspace autolens_profiling)
- library-pr: https://github.com/PyAutoLabs/PyAutoArray/pull/508 (steps 1, 2, 3a)
- library-pr: https://github.com/PyAutoLabs/PyAutoGalaxy/pull/590 (step 3b)
- workspace-pr: https://github.com/PyAutoLabs/autolens_profiling/pull/190 (steps 0 and 4)
- merge-order: PyAutoArray#508 -> PyAutoGalaxy#590 -> autolens_profiling#190. PyAutoGalaxy CI clones PyAutoArray from source and checks out the same-named branch when it exists, so #590 tests against the PyAutoArray branch until #508 merges and that branch is deleted; no PyAutoGalaxy test depends on the new `OverSampler` behaviour, so #590 is green either way.
- heart-ack: shipped over a pre-existing Heart RED (`pyauto-heart readiness --json` 2026-08-28T21:34:42Z, score 45; red_reasons `"release validation FAILED (stage integrate)"`; yellow_reasons `"workspace validation not passing (2 failed, cloud#33179766004: autolens_test scripts/imaging/rectangular_mge.py, autolens_test scripts/imaging/rectangular_mge_rtu.py)"` and `"manifest drift: session-start hooks (generated) — 32 mismatch(es) vs PyAutoMind/repos.yaml"`). Human authorisation 2026-08-28, verbatim: "prm and then kick off phase 2, I authorize the heart RED thing". Quoted verbatim in all three PR bodies.
- result: goal met. HST rectangular 0.6214 -> 0.3334 s step total (1.86x), 0.6184 -> 0.3013 s directly timed (2.05x), target was ~0.35 s. F mapper x mapper 3.13x, MGE total 2.33x. euclid 1.57x, hst Delaunay 1.30x. All three pinned log likelihoods unchanged to every digit at rtol 1e-6; `curvature_matrix` bit-identical for step 3 alone and `allclose(rtol=1e-12)` across the phase. Pool ratio 2.05x -> 2.14x on 8 cores (no oversubscription). test_autoarray 1326 passed, test_autogalaxy 1149 passed.
- parallel-claim: autolens_profiling is also claimed by `nuts-warm-start-driver-and-a100-probe`; file sets are disjoint (this task: `scripts/imaging/likelihood_breakdown/`, `results/breakdown/imaging/`, `results/notes/`; NUTS: `scripts/misc/searches/`, `scripts/imaging/searches/nuts/`, `results/notes/inference/`). Human approved an own parallel worktree 2026-08-28, same arrangement as phase 1. COMMIT DISCIPLINE: explicit pathspecs only in autolens_profiling, never `git add -A`.
- predecessor: phase 1 shipped and merged 2026-08-28 — `complete/2026/08/numba-hst-curvature-matrix-speedup.md` (PyAutoArray#506 `1b89404b`, autolens_profiling#189 `b3fa632a`); PyAutoArray#505 closed.
- repos:
  - PyAutoArray: feature/numba-hst-curvature-matrix-phase2
  - PyAutoGalaxy: feature/numba-hst-curvature-matrix-phase2
  - autolens_profiling: feature/numba-hst-curvature-matrix-phase2
- next-skill: /prm on PyAutoArray#508 once CI is green, then PyAutoGalaxy#590, then autolens_profiling#190 (library-first gate), then the completion record and worktree removal
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
