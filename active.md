# Active Tasks

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

## numba-hst-curvature-matrix-speedup
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/505
- prompt: active/numba_cpu_hst_curvature_matrix_speedup.md
- issued: 2026-08-28
- session: claude --resume session_01SqrSVGPrFcUB1vvDsoTw3n
- status: library-shipped, workspace-pending
- library-pr: https://github.com/PyAutoLabs/PyAutoArray/pull/506
- heart-ack: Heart graded RED score 45 at ship time (`pyauto-heart readiness` ts 2026-08-28T15:02:11Z). Human authorisation 2026-08-28, verbatim: "I authorize things to override the heart RED." Scope: push + PR-open for this task ONLY; merge and release stay human; does not extend to any other task. This is a PLAIN HUMAN OVERRIDE, not the corrective-PR exception — the diff repairs none of the named reasons. Reasons quoted verbatim from `pyauto-heart readiness --json`: RED "release validation FAILED (stage integrate)"; YELLOW "workspace validation not passing (2 failed, cloud#33179766004: autolens_test scripts/imaging/rectangular_mge.py, autolens_test scripts/imaging/rectangular_mge_rtu.py)"; YELLOW "manifest drift: session-start hooks (generated) — 32 mismatch(es) vs PyAutoMind/repos.yaml". RED is pre-existing on main and unrelated: all failing scripts are on the JAX likelihood path or in autofit, in other repos; this branch touches only the numba imaging-inversion path plus an additive-only convolver.py.
- worktree: ~/Code/PyAutoLabs-wt/numba-hst-curvature-matrix-speedup
- parallel-claim: autolens_profiling is also claimed by `nuts-warm-start-driver-and-a100-probe`; file sets are disjoint (this task: `scripts/imaging/likelihood_breakdown/`, `results/breakdown/imaging/`, `results/notes/`; NUTS: `scripts/misc/searches/`, `scripts/imaging/searches/nuts/`, `results/notes/inference/`). Human approved an own parallel worktree 2026-08-28. COMMIT DISCIPLINE: explicit pathspecs only in autolens_profiling, never `git add -A`.
- repos:
  - PyAutoArray: feature/numba-hst-curvature-matrix-speedup
  - autolens_profiling: feature/numba-hst-curvature-matrix-speedup
- note: Phase 1 of the F speed-up on the numba CPU path at HST: instrument F's sub-blocks, remove
  redundant passes, FFT the dense mapper×linear-func convolution if the split confirms it; >=2x on F,
  pins unchanged.
