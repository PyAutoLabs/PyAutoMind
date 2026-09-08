# DelaunayNN ConstantSplit regularization assembly: the 10 ms per call that Phase A left behind

Type: feature
Target: autoarray
Repos:
- PyAutoArray
- autolens_profiling
- autolens_workspace_test
Themes:
- jax-gpu
- delaunay
- profiling
- performance
Difficulty: medium
Autonomy: supervised
Priority: high
Status: active
Consequence: judge
Witness: on the A100 DelaunayNN breakdown (`results/breakdown/imaging/delaunay_nn_hpc_a100_fp64_launch_latency.json` is the post-#533 baseline) the "Regularization matrix (H, ConstantSplit assembly)" row drops from 10.0 ms per call at vmap 16 to under 3 ms and the params→H prefix (`regularization_matrix_prefix_s`) from 16.4 ms per call to under 11 ms, with `EXPECTED_LOG_EVIDENCE_HST = 29144.581944` unchanged (or, if the assembly is reformulated so the fp summation order changes, matching to a stated relative tolerance with the change justified) and the `delaunay_nn.py` jax_assertions passing
Review-minutes: 40
Unattended: ready
Filed: 2026-09-08
Issued: 2026-09-08

Original request (verbatim):

> i agree with your recommendation but its bed soon so once its a good time to stop do that too, but getting some prm done first is good!

(The recommendation agreed to: after DelaunayNN Phase A shipped as PyAutoArray#533, point the
next prompt at the ConstantSplit assembly rather than the cavity early exit.)

## The measurement (A100, post PyAutoArray#533, `results/notes/delaunay_nn_launch_latency.md`)

Phase A cut the DelaunayNN params→H prefix from 143.9 to 28.2 ms unbatched (5.1×), but only
from 24.3 to 16.4 ms per call at vmap 16 (1.48×). The new split-Sibson breakdown stage
(autolens_profiling#227) attributes the remaining per-call cost: the data-side Sibson pass is
~6.4 ms per call, the split-side Sibson ~1 ms, and the **ConstantSplit regularization
assembly ~10.0 ms per call at every chunk size and on the control** — 143× barycentric
Delaunay's equivalent H row (0.07 ms per call) and ~19 % of the 52.6 ms batched whole
likelihood. The assembly is `reg_split_from` fed by `InterpolatorDelaunayNN._mappings_sizes_weights_split`:
6,000 split-cross points, each with a 33-wide (32 neighbours + 1 spare column) Sibson stencil,
scattered into the N×N regularization matrix — ~6.5 M scatter entries per lane versus
~96 k for Delaunay's 4-wide stencil.

The planned "Phase B" cavity early exit targets only the ~6.4 ms Sibson share and is worth
~1.3 ms per call; it is deferred in favour of this.

## Investigation first (one A100 session, then decide)

1. Instrument the assembly: time `reg_split_from` alone under `jax.jit` and `jit(vmap)` at
   batch 16 on the production tables (N = 1500, S = 6000, width 33) and identify whether the
   cost is the scatter-add (`.at[].add` into N×N), the gathers over the padded stencil, or
   the `hstack` spare-column plumbing. Compare against the 4-wide Delaunay call on the same
   inputs to calibrate.
2. Candidate reformulations, measured on the same session:
   - **Dense matmul**: build the split mapping matrix `M_s` (S × N, 33 non-zeros per row) as a
     dense array and form `H = M_sᵀ diag(w) M_s` (or the actual ConstantSplit combination) as
     one GEMM: 6000 × 1500 × 1500 ≈ 13.5 GFLOP per lane, ~0.2 TFLOP at batch 16, i.e. ~10 ms
     fp64 on an A100 — no better unless the split combination lets the GEMM shrink, so measure
     before believing.
   - **Segment-sum over stencil pairs**: sort the (i, j) pairs once per fit (they depend only on
     the frozen tables) and accumulate with `segment_sum` instead of a random scatter into N×N.
   - **Stencil truncation for the regularization only**: keep the 32-wide Sibson stencil for the
     data mapping but regularize the split points with their k largest weights (k = 8–12,
     renormalized). This changes the regularization scheme and the pin; it is a science
     decision to be presented, not taken.
3. Ship the winner that keeps the pin unchanged, or present the pin-changing one with its
   evidence-tolerance argument.

## Contracts

- `EXPECTED_LOG_EVIDENCE_HST` in `scripts/imaging/likelihood_breakdown/delaunay_nn.py` stays
  unchanged for any pure-reformulation change; a pin shift is a bug unless the reformulation
  is explicitly a summation-order change, in which case the note states the tolerance.
- Judge on `regularization_matrix_prefix_s` and the new "ConstantSplit assembly" row.
- Gradient: the assembly is differentiable through the Sibson weights; any `stop_gradient`
  must be justified the way `_jax_delaunay_tables` and the walk do.
- `SIBSON_MAX_NEIGHBORS` / caps unchanged unless the truncation option is chosen.

## Verification on the A100

Same-node control (merge base) vs feature A/B with
`scripts/imaging/likelihood_breakdown/delaunay_nn.py --config-name hpc_a100_fp64 --split-setup
--vmap-batch 16` plus the runtime cell; report all rows unbatched and per call at vmap 16,
against the post-#533 baseline.

Related: `complete/2026/09/delaunay-nn-launch-latency.md` (Phase A record),
`results/notes/delaunay_nn_launch_latency.md` (numbers), the deferred cavity early-exit
(Phase B of the Phase A prompt) which stays unfiled until this lands.
