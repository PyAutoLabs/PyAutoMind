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
