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
- status: library-dev
- worktree: ~/Code/PyAutoLabs-wt/numba-hst-curvature-matrix-speedup
- parallel-claim: autolens_profiling is also claimed by `nuts-warm-start-driver-and-a100-probe`; file sets are disjoint (this task: `scripts/imaging/likelihood_breakdown/`, `results/breakdown/imaging/`, `results/notes/`; NUTS: `scripts/misc/searches/`, `scripts/imaging/searches/nuts/`, `results/notes/inference/`). Human approved an own parallel worktree 2026-08-28. COMMIT DISCIPLINE: explicit pathspecs only in autolens_profiling, never `git add -A`.
- repos:
  - PyAutoArray: feature/numba-hst-curvature-matrix-speedup
  - autolens_profiling: feature/numba-hst-curvature-matrix-speedup
- note: Phase 1 of the F speed-up on the numba CPU path at HST: instrument F's sub-blocks, remove
  redundant passes, FFT the dense mapper×linear-func convolution if the split confirms it; >=2x on F,
  pins unchanged.
