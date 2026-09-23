# HST GPU residue phase 3 — the PSF convolution of the mapping-matrix cube (7.12 ms, 22 %)

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
Status: draft
Epic: hst-gpu-non-solver-residue
Phase: 3
Consequence: judge
Witness: On the A100 (HST, Delaunay, N=1500, fp64, production budget 7, border relocator on) one
matched table of the whole fused `AnalysisImaging.log_likelihood_function` jit — the production
control beside every convolution candidate — giving per row the whole-call ms (10 steady calls,
same `timing.jit_profile` basis as phases 1-2), the traced `psf_convolution_mapping_matrix` stage
row and `input_scatter_fusion` row (`xla_attribution.py`, table reconciling to the wall within 5 %,
zero unjoined time), compile time, peak device memory, and the log-likelihood pin against the
unmodified library answer at <= 1e-9 relative. A written verdict per candidate (lever / no lever /
diagnostic-only) and, only if a candidate beats the control by >= 1.5 ms whole-call at the pin, a
PyAutoArray prompt filed via /intake naming the exact `convolver.py` change.
Review-minutes: 25
Unattended: needs-slicing
Filed: 2026-09-23

## Why this phase exists

Phase 1 (#268, `results/notes/hst_gpu_residue_phase1_2026_09.md`) traced the fused single-call
production jit on the A100: 31.64 ms at budget 7. Its largest *computation* is the PSF convolution
of the mapping-matrix cube — **7.12 ms, 22.3 %**: `input_scatter_fusion` 1.99 ms building the
`(180, 180, 1500)` native cube from the slim mapping matrix, plus three `fft` instructions
(3.7 ms — one `rfft2` at `convolver.py` and an `irfft2` XLA splits in two) over a 389 MB fp64
cube. The HLO census settled that it is compiled ONCE (the two `operated_mapping_matrix_list`
accesses are CSE'd), so the lever is the cube itself, not duplicated work.

Phase 2 (#273, PR #294) measured the production `jax.jit(jax.vmap(fn))` composition and returned
an inconclusive batching verdict at the numerical gate; the batching and callback levers are
parked behind a separately-intaken reproducibility study. The convolution lever is independent
of batching (it is per-lane device compute, and amortises nothing over B), so it is the next
term the campaign map ranks: lever 2 in the "Levers, re-ranked" list of
`draft/research/autolens_profiling/hst_gpu_non_solver_residue_programme.md`.

## The candidates — every one is a harness experiment first

All candidates are injected at the harness level (monkeypatch `Convolver.convolved_mapping_matrix_from`
or the `ConvolverState` it consumes, the same way `library_solver_injection.py` injects the solver),
inside the SAME fused whole-call jit the control runs. **No PyAutoArray edit in this phase.**

1. **The FFT frame (`fft_shape`).** `ConvolverState` pads to `scipy.fft.next_fast_len(..., real=True)`
   of the linear frame; for HST (180 grid, 21x21 PSF) that is 200 = 2^3 * 5^2, already cuFFT-friendly
   (the docstring's "even sizes are incremented to odd" note is STALE — the code does not do it; record
   that as an erratum, do not chase it). Rows: the shipped frame (control), the next power of two (256),
   and the frame the cell's actual mask produces (record `fft_shape` from the state). Expect no lever;
   it is one cheap row and it bounds the frame question. Any frame change alters the compiled program,
   so compile time is a column, not a footnote.
2. **Cube layout for the batched FFT.** The cube is `(ny, nx, n_src)` with the transforms over
   `axes=(0, 1)` — a strided batched transform with the batch axis LAST. Row: transpose to
   `(n_src, ny, nx)` (batch leading, contiguous planes) before the `rfft2`, and the matching layout on
   the way out; the scatter that builds the cube may fuse differently, so the scatter row is reported
   beside the fft rows.
3. **Real-space convolution for a compact PSF.** The library already carries a non-FFT JAX path
   (`use_fft=False` → `convolved_mapping_matrix_via_real_space_from`). Rows: that path as shipped, and a
   `jax.lax.conv_general_dilated` over the cube with `n_src` as the batch axis (cuDNN), at the HST PSF
   size actually configured for the cell (record the kernel shape). State explicitly which pixels the
   real-space path blurs (blurring-mask semantics) so the pin is like-for-like.
4. **Precision on the mapping path — DIAGNOSTIC ONLY.** fp32 cube / complex64 forward FFT with the
   complex128 kernel multiply retained (what `use_mixed_precision` already does on the image path),
   and full complex64. `convolver.py:1195-1205` documents why the kernel multiply stays complex128
   (K >> 40 columns drift the figure of merit by O(1)); expect the 1e-9 pin to fail. Report the error
   in nats and the ms saved; these rows can never be promoted to a lever under this campaign's fp64
   constraint, and the note must say so.
5. **Avoiding the cube — comparison row only, if free.** The w-tilde ("sparse") route builds
   `F = M^T W M` without a blurred mapping matrix. If the fixed-light cell already exposes `--sparse`
   on the A100, run it as ONE comparison row against the control; do not build anything new for it.
   Phase 1 did not measure the sparse operator and this phase does not adopt it.

Screen candidates locally on the RTX 2060 (fp64; the 389 MB cube fits the 6 GB card, the whole
fixed-light cell already runs there — phase 1's RTX legs) with a standalone convolution microbenchmark
AND the whole-call jit, then submit the survivors plus the control to the A100 in one bounded array.
**Judge only on A100 whole-call rows with the trace beside them** — a microbenchmark win that the
fused program does not show is not a lever (fusion moves the scatter; phase 1's warning about
`--split-setup` prefix rows applies to every isolated FFT timing).

## Constraints — inherited from the campaign map, not negotiable here

- fp64, Delaunay, production budget 7, PDIP fallback on, positivity never dropped, border relocator on
  (production's default). The certified solver stays a harness injection.
- Every candidate carries the <= 1e-9 relative pin against the UNMODIFIED library log likelihood, asserted
  on every fp64 leg, on the same seeded distinct parameter vectors phase 2 drew (`seed=0`), not only the
  fiducial. The threshold is declared here and is not relaxed after seeing the data.
- HST and the A100 first; Euclid follows only once a lever lands.
- Per candidate the note states: harness experiment or real PyAutoArray change, and what the library
  change would be. No silent library edit.
- Sessions end at their deliverable: the A100 submit -> wait -> harvest step is a human resume point.

## Known traps

- `xla_attribution.py` `StageRule` line ranges for `convolver.py` are pinned to source lines and drift with
  PyAutoArray; the real-space path (`convolved_mapping_matrix_via_real_space_from`, ~line 1348+) is NOT
  covered by the current `psf_convolution_mapping_matrix` rules. Re-pin against the installed revision
  and add rules for every candidate's code path, or its kernels land in `other` and the 5 % gate fails.
- The mapping-matrix path deliberately keeps the kernel multiply in complex128 (`convolver.py:1195-1205`).
- A non-uniform over-sample map triples jit compile time; do not touch over-sampling.
- `reg_adapt` cannot jit on the Delaunay family; `adapt_split` is the cell's shipped regularization.
- Phase 2's `activate.sh` ERR trap ate the submit footer on non-zero cell exits; the phase-2 submit shows
  the temporary remove/restore pattern to copy.
- `hpc/sync` never pushes: code reaches RAL by `git pull` on the login node; `HPCPullPyAuto` refreshes
  the library checkouts. Record the five library revisions in the job sidecar as phase 2 did.
- Config names must fall outside `CONFIG_TAGGED_RE` so nothing reaches the dashboard headline table;
  `build_readme.py --check` and `check_submits.py` are lint gates.

## Deliverables

- `scripts/imaging/likelihood_breakdown/fixed_light_psf_cube.py` (or a `--psf-candidate` mode on
  `fixed_light_trace.py`, whichever reuses more of `fixed_light_system` / `library_solver_injection` /
  `timing` / `xla_attribution`), the convolution injection helper under
  `scripts/misc/likelihood_breakdown/`, focused tests under `scripts/misc/test/`.
- `hpc/batch_gpu/submit_breakdown_imaging_fixed_light_psf_cube_delaunay_a100_hst_fp64` with the
  bounded candidate grid and the provenance footer.
- Artifacts `results/breakdown/imaging/fixed_light_psf_cube_*.{json,png}`, a job sidecar
  `results/notes/hst_gpu_residue_phase3_job<ID>.json`.
- `results/notes/hst_gpu_residue_phase3_psf_2026_09.md` — the matched table, the per-candidate verdicts,
  provenance and gate table in the format the phase-1/2 notes set; `profiling_campaign_status_2026_09.md`
  and the campaign map's "Levers, re-ranked" list updated; READMEs regenerated.
- If a candidate wins: a PyAutoArray prompt via /intake (not this phase's edit).

## Out of scope

Batching / the Delaunay callback (phase 2b, parked behind the reproducibility study); the second
Cholesky (phase 4); the `A.T A` GEMM; rectangular and DelaunayNN; Euclid; JWST; numba CPU
(#267's); any PyAutoArray, PyAutoLens or PyAutoFit source change.
