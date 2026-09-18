- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/268
- pr: https://github.com/PyAutoLabs/autolens_profiling/pull/270
- epic: hst-gpu-non-solver-residue (phase 1)
- summary: |
    Phase 1 of the `hst-gpu-non-solver-residue` epic - the first MEASURED decomposition of the fused
    production likelihood on a GPU. New harness `scripts/misc/likelihood_breakdown/xla_attribution.py`
    (compiled-HLO index incl. the stack-frame table, `jax.profiler.ProfileData` trace parser, stage map
    with mixed-fusion / device-idle / host-callback rows, HLO census with innermost-frame predicates; 49
    tests) and cell `scripts/imaging/likelihood_breakdown/fixed_light_trace.py` (S3 certified Delaunay
    call at the PRODUCTION budget 7 with PDIP fallback, fp64; routes b + d; traces 10 steady calls of the
    production `jax.jit`). Five legs: A100 array 343350 x3 (Delaunay relocator on / off, DelaunayNN) and
    RTX 2060 x2. Every kernel joined to source, unjoined 0.000 ms on all legs, reconciliation within 2.6 %,
    route d == b at <= 3.2e-11. Suite 527 tests, all four lint gates green. No library change.
- finding: |
    THE "~13.9 ms MESH / MAPPER / WEIGHTS" BUCKET IS REFUTED. On the A100 those stages total 0.37 ms
    (1.2 %). What the attribution arithmetic had lumped there is the PSF FFT of the (1500,180,180)
    mapping-matrix cube (7.12 ms, 22 %), the A.T A GEMM (4.18 ms, 13 %) and the device sitting IDLE for
    5.44 ms (17 %) while scipy's qhull runs on the host inside `pure_callback`. And THE 25.39 ms HEADLINE
    WAS A PASS-BUDGET-2 NUMBER: at the production budget 7 the Delaunay A100 call is 31.6 ms (route b,
    budget-independent, ties the two runs at 1.8 %). Non-solver residue = 21.7 of 31.9 ms.
- finding-census: |
    NO (n,n) ADD OF F + lambda*H SURVIVES XLA. `abstract.py:371` lowers to one `transpose`; every
    consumer walks back to a single producer, `cublas-lt-matmul.2` (the F GEMM). The JAX/GPU side of
    `draft/bug/autoarray/curvature_reg_matrix_rebuilt_every_access.md` has NO cost to recover - posted on
    #267, whose lever 3 owns the numpy/numba fix and the stale docstring. The two
    `operated_mapping_matrix_list` accesses compile to ONE PSF convolution (CSE). 7 gathers at :613, 0 at
    :397. The border relocator ON is production (autogalaxy packaged config default true; every lensing
    workspace and the Euclid pipeline set it true) and costs 0.10 ms - the issue's premise was backwards.
- traps: |
    (1) CUDA command buffers make every kernel report `hlo_op=command_buffer_N`; the traced executable is
    compiled from the SAME lowering with `xla_gpu_enable_command_buffer=""` and both walls recorded
    (+0.4/+0.8 % A100 Delaunay, +17 % DelaunayNN - that leg's idle row is caveated). (2) jax 0.10.2 emits
    `stack_frame_id`, not `source_file=`; the table is HloModuleProto field 17, read with a 70-line wire
    parser (no xprof; do not import TF beside a live JAX GPU backend). (3) A census predicate that scans
    the whole stack for `:371` reports 15 false adds - both arguments of the one-line `_xp.add` are
    lazily evaluated AT that line; key on the innermost frame (regression test). (4) Harness-injected
    solver kernels walk out to the library call site without their own stage rule; `inversion/mesh/` is a
    prefix of `border_relocator.py` - order rules most-specific first. (5) `check_submits.py`'s
    cell-coverage regex cannot see `python3 -u`, so the rule passes vacuously on all 94 submits, and prose
    inside a `# WALL-BASIS:` block parses as row data - both to /intake. (6) RTX 2060 Max-Q absolute ms
    are SESSION-SCOPED: 1063 vs 622 ms for the same leg two hours apart, ~1 % within a session, stage
    shares shift; never rank from it. (7) A100 stage rows carry ~9 % profiler inflation (shares unaffected).
- levers: |
    Ranked for phase 2 (A100 Delaunay, production 31.6 ms): (1) qhull `pure_callback` host round-trip
    5.44 ms / 17 % (PyAutoArray; `pure_callback` non-differentiability is load-bearing; one round-trip per
    evaluation regardless of N; under production `vmap` with `vmap_method="sequential"` it is one host
    call PER LANE and is the one term that does not amortise - measure the vmap program before ranking
    finally); (2) PSF convolution cube 7.12 ms / 22 % (harness experiment first: fft_shape, real-space,
    complex64); (3) second Cholesky of F+lambda*H for the log det 0.89 ms (harness). Not levers: mesh /
    mapper / weights, border relocator, mixed fusion. Settled: matrix-free log-det (#247), reg_adapt cannot
    jit on Delaunay, non-uniform over-sample map triples compile. Solver-side (out of this campaign's
    scope but the largest item): the certified solve is 10.2 ms at fixed budget 7 while the fiducial
    certifies in 1-2 passes; an early exit helps single-call only - under `vmap` a batched `while_loop`
    runs to the max lane count.
- open: |
    Phase 1 traced the SINGLE-CALL jit. Production Nautilus runs `jax.vmap(jax.jit(call))`; the vmap
    program was not traced (the cell has no `--vmap-batch`), so per-lane amortisation and the sequential
    qhull callback's share under vmap are unmeasured - the first thing phase 2 should add. Rectangular,
    Euclid, sparse operator, JWST not measured.
- note: |
    results/notes/hst_gpu_residue_phase1_2026_09.md.
- worktree: |
    ~/Code/PyAutoLabs-wt/hst-gpu-residue-p1 (own worktree beside #267's on the same repo, disjoint
    files; parallel-claim recorded). RAL worktree /mnt/ral/jnightin/autolens_profiling_wt/hst-gpu-residue-p1
    at 6b60d30 left in place for phase 2.

## Original prompt

# HST GPU residue phase 1 — a trace-based, one-process decomposition of the certified Delaunay call on the A100 and the RTX 2060

Type: research
Target: autolens_profiling
Repos:
- autolens_profiling
Themes:
- profiling
- pixelization
- hpc-gpu
- inversion
Difficulty: large
Autonomy: supervised
Priority: high
Status: formalised
Epic: hst-gpu-non-solver-residue
Phase: 1
Consequence: judge
Witness: On the A100 (fp64, HST, Delaunay, N=1500, certified budget 7 + PDIP fallback) and on the
RTX 2060 (same configuration), a per-stage table measured from the XLA device timeline of the
PRODUCTION jit — one program, one process — whose rows plus a measured device-idle row sum to the
whole-call wall time within 5 %; every route still returns the library's own log likelihood to
<= 1e-9 relative; the optimized HLO census states how many (n,n) `add`s of `F + lambda*H` survive
XLA (the JAX verdict on `draft/bug/autoarray/curvature_reg_matrix_rebuilt_every_access.md`); no
PyAutoArray change.
Review-minutes: 20
Unattended: needs-slicing
Filed: 2026-09-16
Issued: 2026-09-16
Issue: https://github.com/PyAutoLabs/autolens_profiling/issues/268

## Original request (verbatim)

> After seeing significant speed up in the linear solver on a100s / gpus by fixing the len slight,
> we filed an issue to begin speeding up other aspects of the likelihood function now this was not
> a bottle neck (e.g. 4.2 ms on A100). This is a related issue but not the main one: /start_dev
> draft/bug/autoarray/curvature_reg_matrix_rebuilt_every_access.md . Can we begin doing this
> optimization process of the likelihood function (E..g everything int he breakdown which isnt
> fnnls). I have a separate claude chat doing the numba CPU sparar speed up, so focus exlusively on
> the JAX GPU A100 and RTX run times

## Why phase 1 is a measurement

The campaign map (`hst_gpu_non_solver_residue_programme.md`) says ~21 of the 25.4 ms certified
Delaunay A100 call is not the solver, and that the largest term — "~13.9 ms mesh / mapper / weights /
imaging / blurring" — is **attribution arithmetic** (`fixed_lens_light_library_path_2026_09.md:174-190`:
phase-0 kernel rows from another cell subtracted from the phase-1 whole call). Every JAX
decomposition this repo owns (`--split-setup`) is ~11 *separately compiled* programs whose
prefix-differences move work across boundaries (PyAutoArray#531 made the H row negative). Nobody
has ever measured where the fused production program spends its device time.

## The mechanism (harness only, no library edit)

Production is ONE `jax.jit` (`autofit/non_linear/fitness.py:879`, `Fitness._jit = jax.jit(self.call)`),
and `fixed_light_library.py`'s `_likelihood_fn` sits on exactly that boundary. Decompose *that*
program from its own execution:

1. `jax.profiler.trace(...)` around K steady calls of the compiled route-d likelihood → device
   timeline of every XLA kernel (fusions, cuBLAS GEMMs, cuSOLVER Cholesky, FFTs, gathers, the
   `while_loop` bodies of the walk and PDIP, the qhull `pure_callback` host round-trip). Parse with
   `jax.profiler.ProfileData` (xplane, no extra deps) or the perfetto JSON (`create_perfetto_trace`).
2. `jax.jit(fn).lower(tree).compile().as_text()` → the optimized HLO. Every instruction carries
   `metadata={op_name=..., source_file=..., source_line=...}` from tracing, so each kernel joins to a
   library source location **without `jax.named_scope`** (which would be a PyAutoArray edit).
3. A stage map (ordered regexes over `source_file` / function) buckets kernels: instance build ·
   ray-trace data grid · ray-trace mesh grid · lens light + PSF · border relocator · qhull
   callback · locate + walk · interpolator weights / dual areas · mapping matrix · PSF convolution
   of the mapping matrix · D · F · H (adapt_split) · F+λH · edge subset · PDIP solve · log det
   (F+λH) · log det (H) · mapped reconstruction + χ² + evidence · other. Fusions whose constituents
   span stages land in an explicit **mixed-fusion** row rather than being guessed. Device-idle
   (timeline gaps: launch latency + host work) is a **measured** row, so the table sums to the
   wall time by construction and the 5 % witness is about the join being complete, not about a
   residual.
4. HLO census from the same text: the number of (n,n) `add` instructions sourced at
   `abstract.py:371` (`curvature_reg_matrix`, reached twice per evaluation: `:613` and `:894→:388/:397`),
   the two `[ids][:, ids]` gathers, and the number of PSF FFT convolutions of the mapping-matrix
   cube (`operated_mapping_matrix_list` is a plain property reached twice). That is the JAX-side
   verdict on the curvature-draft bug and a free check of the doubled-convolution candidate.

Step 0 is a 30-minute feasibility spike on the RTX: confirm the trace events carry HLO op names
joinable to the compiled text. If they do not, the fallback is stated, not silent: anchor prefix
jits on the three hard boundaries that cannot fuse (the `pure_callback`, the walk `while_loop`,
the PDIP `while_loop`) and report the trace totals beside them.

## Legs

| Leg | Where | Config | Notes |
|---|---|---|---|
| Delaunay, N=1500, budget 7, fp64 | RTX 2060 (local `PyAutoGPU` venv) | `local_rtx2060_fp64_fixed_light_trace` | JAX_PLATFORMS unset, prealloc off |
| Delaunay, N=1500, budget 7, fp64 | A100 `euclid-ral-gpu-2` | `hpc_a100_fp64_fixed_light_trace` | fresh `JAX_COMPILATION_CACHE_DIR`, RAL worktree of the feature branch, one ssh batch |
| same, border relocator at the **library default (off)** | both | `…_border_off` | the cells force it on; production does not — state both |
| DelaunayNN, N=1500, budget 7 | A100 | optional extra array task | the 69 % residue quoted by the map |

Whole-call wall time is measured exactly as phase 5 did (`jit_profile`, 10 steady calls) so the
25.39 ms row reconciles; the trace runs on separate steady calls and must not perturb it (report
traced vs untraced wall time).

## Deliverables

- `scripts/misc/likelihood_breakdown/xla_attribution.py` (HLO index, trace parser, stage map,
  attribution, census) + tests under `scripts/misc/test/`.
- `scripts/imaging/likelihood_breakdown/fixed_light_trace.py` (reuses `fixed_light_system`,
  `library_solver_injection`, `timing`; flags `--mesh`, `--border-relocator {cell,library}`,
  `--trace-calls K`, `--source-pixels`, `--routes b,d`).
- `hpc/batch_gpu/submit_breakdown_imaging_fixed_light_trace_delaunay_a100_hst_fp64` with its
  `# WALL-BASIS:` block; JSON + PNG under `results/breakdown/imaging/`; regenerated READMEs.
- `results/notes/hst_gpu_residue_phase1_2026_09.md`: per-hardware table, reconciliation, the
  curvature-draft JAX verdict, and the **ranked lever list for phase 2** with measured ms each.

## Scope and coordination

- No PyAutoArray edit. Candidates the trace surfaces are filed as their own prompts under this
  epic, one lever per phase, after this note ranks them.
- **Numba CPU is another session's** (`fixed-lens-light-numba-cpu`, autolens_profiling#267). That
  issue pairs its CPU levers (split-reg assembly, sparse log det H, shared Cholesky) with A100
  *measurement* rows and folds the CPU fix + docstring of the curvature draft into its lever 3.
  This phase supplies the GPU-side determination of that draft and does not issue it separately.
- Supersedes the GPU columns of `draft/research/autolens_profiling/post_certified_solver_likelihood_breakdown.md`
  (its CPU columns are the numba campaign's); cross-reference, do not delete.
- Inherits the GPU verdict: fp64, Delaunay budget 7, PDIP fallback, positivity never dropped,
  route d == route b at <= 1e-9 asserted on every fp64 leg.
- Out of scope: rectangular (one `--mesh` flag away, not run), Euclid, sparse operator, JWST,
  batching, any optimisation.
