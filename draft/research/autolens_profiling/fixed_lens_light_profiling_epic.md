# Fixed lens light — source-only likelihood profiling programme (phase map)

Type: research
Target: autolens_profiling
Repos:
- autolens_profiling
Themes:
- profiling
- pixelization
- hpc-gpu
Difficulty: too-large
Autonomy: human-required
Priority: high
Status: campaign map — the five phases route through /start_dev ONE at a time, in order; this file is never issued itself and nothing here is bulk-issued
Consequence: judge
Review-minutes: 25
Unattended: needs-slicing
Epic: fixed-lens-light-profiling
Filed: 2026-09-13

Filed 2026-09-13 from James's five-task brief at the close of phase 0. This is the
umbrella view; each phase's real content lives in its own prompt file beside this one.
Update the table as phases ship.

## Original request (2026-09-13, verbatim)

"Ok these are the takss to now queue up: 1) Perform profiling of positive-negative solver for completeness albeit S3 certified
active-set seems like the lead forward; 2) Perform the same profiling on CPU (using CPU appropriate methods) and on m laptop GPU as
its important now we are converging on a solutiopn we also optimizze for consumer GPUs; 3) Confirm that S3 certified active-set is
ver fast on solutions which give low likelihoods, as maybe the fast run times here are a result of the model being good and giving
high likelihoods or an easier to solve solution; 4) Provide profiling information over number of source pixels with the new approach
on difernet hardware 5) For all hardware types and likelihood variants (e.g. sparse operator) give an assessment of the overall
likelihood function on JWST (0.03" pixel scale), HST and Euclid data for 500, 1250 and 2500 source pixels. For each take one step
at a time, and try do it all in --auto."

Clarification (same day): "For positive-negative I want you to use a positive negative solve (e..g. np.linalg.solve) but DO NOT include the
MGE in the matrices or solution, so it sould use normal light porfiles which subtract the MGE beforehand. PyAutoGPU is avirtual
enviroment which already exists on this laptop for running GPU JAX so use that. Rest of plan sonds good. Only use HST and Euclid
for now, drop JWST. Skip the sparse operator for now."

## What the programme is

With the lens light FIXED after SLaM light[1] — the MGE (60 linear Gaussians) converted to
regular light profiles at their solved intensities and subtracted beforehand ("S3") — only
source pixels remain in the linear system. Phase 0 showed that this makes a *certified
active-set* positivity solve viable. The programme's job is to turn that one A100 kernel
measurement into a production verdict: which solver, at which precision, on which
hardware, for how many source pixels, on real HST and Euclid data.

## Phases — strictly 1 → 2 → 3 → 4 → 5, "one step at a time"

| # | Phase | Prompt | Gate | State |
|---|-------|--------|------|-------|
| 0 | Fixed lens light, source-only inversion — kernel measurement on the A100 | `active/fixed_lens_light_source_only_inversion.md` (autolens_profiling #248) | — | **DONE 2026-09-13** — note `results/notes/fixed_lens_light_source_only_2026_09.md`. S0 PDIP 37 ms → S3 PDIP 26-28 ms → S3 certified active-set 4.2 ms Delaunay (pass 2) / 11 ms rect (pass 7), same positive solution to 1e-10 nats; S3 unconstrained Cholesky 1.5 ms but +6 nats (Delaunay) / +335 nats (rect). Library calls S0→S3: rect 51.7→38.4 ms, Delaunay 70.4→49.2 ms |
| 1 | Library-path timing of the S3 positive-negative and certified active-set solvers (A100, HST) | `active/fixed_light_unconstrained_library_path.md` (autolens_profiling #251) | phase 0 note landed | **PR open #252, awaiting merge (stacked on #250)** 2026-09-13 — note `results/notes/fixed_lens_light_library_path_2026_09.md`. Whole library likelihood call: S0 PDIP 50.97 / 65.10 / 72.95 ms -> S3 certified active set 25.10 / 25.39 / 36.26 ms (2.03x / 2.56x / 2.01x), identical likelihood to 1e-15..1e-11; S3 PDIP 38.65 / 49.67 / 55.37; positive-negative 21.13 / 27.16 / 35.08 at +334.93 / +6.40 / +8.22 nats (still prohibited); worst-case fallback 41.45 / 51.83 / 58.32, still faster than the library today. Phase 0's projection held. Traps: the library subsets to `solve_ids_to_keep` before calling its solver, and `lax.cond` runs BOTH branches under `vmap`. Merge #250 first |
| 2 | The same profiling on CPU (CPU-appropriate methods) and on the laptop RTX 2060 | `active/fixed_light_cpu_and_consumer_gpu.md` (autolens_profiling #253) | phase 1 library-path rows measured | **PR open #254, awaiting merge (stacked on #252, itself on #250)** 2026-09-13 — note `results/notes/fixed_lens_light_hardware_2026_09.md`. Certified active set wins on every hardware and the prize shrinks with it: a -> d 2.03x/2.56x/2.01x (A100), 1.28x/1.48x/1.46x (RTX 2060 fp64), 1.83x/1.74x/1.35x (8 CPU threads), 1.16-1.22x (1 thread). The GeForce fp64 penalty never bit — mixed precision buys 5-8 % for <= 2.5e-3 nats and 16 % more VRAM, so fp64 stays the consumer path. **Memory is the consumer wall**: @vmap 16 needs 11.88 GiB on a 6 GB card, batch 4 OOMs, batch 2 is slower than a single call, and the same shape OOM-killed the 16 GB host — phase 1's fastest row has no consumer counterpart. On the CPU the A100 kernel result does not transfer: the numpy certified active set does not beat the library's own fnnls NNLS, and both are 1.9-3.6x slower at 8 BLAS threads than at 1. Merge #250 then #252 first |
| 3 | Is the certified active-set fast only because the model is good? (graded Δlog L draw set) | `active/fixed_light_certified_low_likelihood_draws.md` (autolens_profiling #255) | phase 2 hardware table exists | **PR open #256, awaiting merge (stacked on #254)** 2026-09-13 — note `results/notes/fixed_lens_light_low_likelihood_draws_2026_09.md`. **The phase-0 budgets do not hold.** Over a seeded 41-model draw set (4 walks × 4 Δlog L targets + 24 random draws at 5σ), Delaunay's pass-2 budget falls back on **67.5 %** of the set (95.8 % of the random draws) and rectangular's pass-7 on **27.5 %**; smallest zero-fallback budgets **7 (Delaunay) / 11 (rectangular)**. The meshes fail oppositely: passes grow with model error on Delaunay (ρ +0.698) and fall on rectangular (ρ −0.535, because a worse model's bigger active set is already mostly found by the 152-pixel edge-zero seed). The lever survives at ~half its fiducial headline (median 2.6× / 5.4× over PDIP, A100) and PDIP's cost barely moves (15→17, 17→21 it), so budget-plus-fallback is a bounded worst case. Pass counts identical on A100 and CPU. A2 error grows to +4.07e4 / +6339 nats — no case for dropping positivity anywhere. Merge #250, #252, #254 first |
| 4 | Source-pixel scaling of the new approach across hardware | `draft/research/autolens_profiling/fixed_light_source_pixel_scaling.md` | phase 3 pass-count-vs-Δlog L answered — **satisfied 2026-09-13**: sweep the certified scheme at budgets **7 (Delaunay) / 11 (rectangular)** with the PDIP fallback, not at the fiducial budgets | filed, unblocked once #256 merges |
| 5 | Whole-likelihood assessment on HST + Euclid at 500 / 1250 / 2500 source pixels — the verdict | `draft/research/autolens_profiling/fixed_light_likelihood_assessment_hst_euclid.md` | phase 4 ms-vs-N curves exist | filed |

The order is the human's instruction, not a convenience: each phase's grid is chosen from
the previous phase's answer (phase 4 sweeps the solvers phase 3 certified as safe; phase 5
assesses only the configurations phase 4 shows can afford the pixel counts).

## Hardware legend

- **A100** — RAL `gpu-2` partition, fp64. Legs go out through
  `autolens_profiling/hpc/batch_gpu/submit_breakdown_imaging_fixed_light_*` +
  `submit_fixed_light.sh`. Every A100 phase has a submit → wait → harvest step: that is a
  **human resume point**, not a park, and not a reason to arm a timer.
- **CPU** — local, CPU-appropriate methods: numpy/scipy `cho_factor`/`cho_solve`, scipy
  NNLS or the library's CPU NNLS path, JAX-CPU for the jit/library rows. Record thread count.
- **RTX 2060 (6 GB, consumer)** — the laptop GPU through the existing `PyAutoGPU` venv at
  `/home/jammy/venv/PyAutoGPU` (JAX 0.10.2 + jax-cuda12-plugin). Traps: the session shell
  exports `JAX_PLATFORMS=cpu` and `JAX_PLATFORM_NAME=cpu` which MUST be unset;
  `XLA_PYTHON_CLIENT_PREALLOCATE=false` is required at 6 GB. GeForce fp64 runs at 1/32
  rate, so fp64 **and** fp32/mixed-precision legs are both required, with pins re-derived
  per precision.

## Code and data

- Cell: `@autolens_profiling/scripts/imaging/likelihood_breakdown/fixed_light.py`
  (`--mesh`, `--source-pixels`, `--pass-budget-max`, `--vmap-batch`, `--library-row`).
- Kernels: `@autolens_profiling/scripts/misc/likelihood_breakdown/active_set_steps.py`.
- Datasets: `autolens_profiling/dataset/imaging/hst` (0.05") and `.../euclid` (0.1").

## Out of scope for the whole epic

- **The sparse operator.** The human's phase-5 text named it as a likelihood variant, then
  dropped it: "Skip the sparse operator for now." It is blocked on the PyAutoArray weight-map
  bug, filed as `draft/bug/autoarray/sparse_inversion_ignores_profile_subtracted_image.md`.
- **JWST (0.03").** Named in the original text, dropped in the clarification: HST and Euclid
  only.
- Dense inversion only, throughout.
