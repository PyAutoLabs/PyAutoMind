# HST GPU residue phase 2 — vmap vs jit for the production likelihood, then the batch-aware Delaunay callback

Type: research
Target: autolens_profiling
Repos:
- autolens_profiling
- PyAutoArray
Themes:
- profiling
- pixelization
- hpc-gpu
- inversion
Difficulty: large
Autonomy: supervised
Priority: high
Status: in flight — corrected current-production A100 array 344635 submitted 2026-09-19; resume at harvest and verdict
Scoped: 2026-09-16 start_dev (Fable) issues STEP 1 ONLY (autolens_profiling harness + A100 legs + note + policy); step 2 (PyAutoArray batch-aware callback) is filed as phase 2b via /intake only if step 1's numbers say the callback matters
Epic: hst-gpu-non-solver-residue
Phase: 2
Consequence: judge
Witness: On the A100 (HST, Delaunay, N=1500, fp64, production budget 7) one matched table: the exact
`Fitness._vmap` program over 16 DISTINCT production parameter vectors vs 16 scalar-jitted evaluations of
the same vectors, identical solver and fallback semantics, giving per-lane wall, callback count, host
qhull-vs-table-building time, PDIP iterations and walk steps per lane, and a device timeline — followed
by a written batching policy (keep vmap at batch B / chunk / scalar jit) with the crossover stated from
measurement. If the batch-aware callback is implemented: tables and log likelihood bit-for-bit identical
to the sequential callback on every lane, and the measured per-lane saving stated beside the ~0.7 ms
dispatch-overhead prediction.
Review-minutes: 25
Unattended: needs-slicing
Filed: 2026-09-16
Issued: 2026-09-16

## Current-production correction (2026-09-19)

PyAutoFit#1638 changed `Fitness._vmap` from `jax.vmap(jax.jit(call))` to
`jax.jit(jax.vmap(call))` on 2026-09-17. Array 343376 therefore remains
historical evidence for the retired composition; it cannot set the current
batching policy. The branch now measures the exact current nesting, with each
lane pinned both against scalar `jax.jit(call)` and an independently compiled
library-PDIP reference at 1e-9 relative. The replacement bounded grid is A100
array 344635, submitted from profiling revision `e2a5187` on 2026-09-19.

## Original request (verbatim)

> can you have codex astro review this issue on vmap versus jit, whether we should keep vmap and just
> take the hit on it slowing down the likelihood function or if there is the option of the delaunay JAX
> call just being jit? Dont run code, just have it try and give its opinion on whether there is an
> obvious path forward or we need to do more profiling
>
> ok, update the plan according to the recommendation, but do not begin doing any dev work yet

## Why this phase exists

Phase 1 (#268, `results/notes/hst_gpu_residue_phase1_2026_09.md`) traced the fused SINGLE-CALL jit:
31.6 ms at the production budget, with 5.44 ms of device idle sitting in the qhull `pure_callback`.
Production is now `jax.jit(jax.vmap(call))` (`autofit/non_linear/fitness.py:878`), and
`_jax_delaunay_tables` (`autoarray/inversion/mesh/interpolator/delaunay.py:139-171`) is declared
`vmap_method="sequential"`: one serial host round-trip per lane. Nobody has traced the vmap program.

The Codex review on #268 (2026-09-16) settled the framing: an inner `jit` cannot shield the callback
from an enclosing `vmap`, so "Delaunay just jit" means either a batch-aware callback (local) or hoisting
the triangulation out of the vmapped region (invasive: fitness → `AnalysisImaging.fit_from` →
`TracerToInversion.mapper_galaxy_dict` → PyAutoGalaxy `mapper_from` → the interpolator). It also
corrected two pieces of our evidence — see the campaign map's "Revision after phase 1".

## Step 1 — the one measurement (autolens_profiling, harness only)

Extend `scripts/imaging/likelihood_breakdown/fixed_light_trace.py` (or a sibling `fixed_light_vmap.py`
reusing `xla_attribution.py`) with a `--vmap-batch B` mode that wraps the route-d likelihood exactly as
`Fitness._vmap` does — `jax.jit(jax.vmap(fn))` — over B DISTINCT parameter
vectors drawn as the phase-3 graded draws were (`fixed_light_draws.py`), never B copies of the fiducial
(identical lanes hide straggler costs). Time, on the A100, fp64, HST Delaunay N=1500, budget 7:

- route d scalar jit × B (sequential) vs vmap-B, per completed likelihood; B = 4, 8, 16;
- `use_jax_jit=True` semantics for the scalar arm (trap: `Nautilus(use_jax_vmap=False)` is UNJITTED);
- the certified path with a cond-free fixed budget AND with the `lax.cond` PDIP fallback (both branches
  run under vmap), so the fallback's batched cost is a row, not a footnote;
- trace both programs: per-lane callback count and host span split into qhull vs table building
  (instrument `scipy_delaunay_tri_only` on the host), PDIP iterations and walk `while_loop` steps per
  lane (max-over-lanes cost), device idle per lane;
- pins: every lane's log likelihood equal between arms and against the independent library-PDIP
  reference to <= 1e-9 relative.

Deliverable: a note `results/notes/hst_gpu_residue_phase2_vmap_2026_09.md` with the matched table, the
crossover (if any) in B and N, and a written batching policy. If the policy is "chunk"/"scalar", file a
PyAutoFit prompt for `fitness.py` / Nautilus `search.py` (decoupling device batch from proposal batch,
`use_jax_jit` wiring) — that is not this phase's edit.

## Step 2 — the batch-aware callback (PyAutoArray, only if step 1 says the callback matters)

`autoarray/inversion/mesh/interpolator/delaunay.py:90-171`: `vmap_method="expand_dims"` with a host
body that accepts `(..., N, 2)`, triangulates each lane separately and returns stacked `(B,2N,3)`,
`(B,2N,3)`, `(B,N)` int32 tables with the existing -1 padding; scalar shapes unchanged. Never
triangulate all lanes as one point cloud. Optional: bounded host workers for the per-lane qhull calls
(check the installed SciPy/qhull thread behaviour; RAL CPU allocation; no persistent geometry cache).
Keep the `stop_gradient` boundaries exactly where they are. Pins: tables bit-identical to the
sequential body per lane; log likelihood <= 1e-9. A100 row before/after under the production vmap.

## Also carried

- Fold the phase-1 note errata into the phase-2 PR: idle is the largest ROW but the PSF convolution is
  the largest COMPUTATION; 4.73 ms is the whole table-building function, not qhull; overlap with the
  data-grid ray trace is blocked by border relocation (`border_relocator.py:454`); the callback fails to
  amortise over B — it does not "get worse with N"; the second Cholesky is not pure duplication.
- Follow-ups to /intake (not here): `check_submits.py` cell-coverage regex blind to `python3 -u`;
  WALL-BASIS prose parsed as rows.

## Out of scope

Hoisting the triangulation out of the vmapped region (only if step 2 needs host parallelism it cannot
get locally — file separately); device triangulation; the PSF-cube and log-det levers (phases 3-4);
rectangular; Euclid; sparse; JWST. Numba CPU is #267's.
